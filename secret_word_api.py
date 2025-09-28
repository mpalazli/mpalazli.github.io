#!/usr/bin/env python3
"""
Gizli Kelime API - Python Flask Servisi
Her 3 dakikada bir değişen gizli kelime servisi
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import time
import os
from datetime import datetime
import threading
import logging

# Flask uygulaması oluştur
app = Flask(__name__)
CORS(app)  # CORS desteği

# Logging ayarları
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Türkçe gizli kelime havuzu
WORD_POOL = [
    'güvenlik', 'sistem', 'kapı', 'giriş', 'çıkış',
    'merhaba', 'hoşgeldin', 'teşekkür', 'lütfen', 'tamam',
    'başla', 'bitir', 'devam', 'dur', 'bekle',
    'açık', 'kapalı', 'yeşil', 'kırmızı', 'mavi',
    'bir', 'iki', 'üç', 'dört', 'beş',
    'altı', 'yedi', 'sekiz', 'dokuz', 'on',
    'güzel', 'harika', 'mükemmel', 'başarılı', 'doğru',
    'ev', 'ofis', 'masa', 'sandalye', 'pencere',
    'telefon', 'bilgisayar', 'tablet', 'kamera', 'mikrofon',
    'kitap', 'kalem', 'kağıt', 'dosya', 'klasör',
    'su', 'çay', 'kahve', 'ekmek', 'peynir',
    'sabah', 'öğle', 'akşam', 'gece', 'gün'
]

# Rate limiting için basit cache
rate_limit_cache = {}
RATE_LIMIT_SECONDS = 2  # 2 saniyede bir istek
cache_lock = threading.Lock()  # thread güvenliği için lock


def get_current_secret_word():
    """3 dakikalık zaman dilimlerine göre deterministik kelime seç"""
    current_time = int(time.time())
    interval_seconds = 3 * 60  # 3 dakika = 180 saniye

    interval_index = current_time // interval_seconds
    word_index = interval_index % len(WORD_POOL)
    selected_word = WORD_POOL[word_index]

    next_change_time = (interval_index + 1) * interval_seconds
    remaining_seconds = next_change_time - current_time

    return {
        'word': selected_word,
        'interval_index': interval_index,
        'current_time': current_time,
        'next_change_time': next_change_time,
        'remaining_seconds': remaining_seconds
    }


def check_rate_limit(client_ip):
    """Basit rate limiting kontrolü"""
    global rate_limit_cache
    current_time = time.time()

    with cache_lock:  # thread güvenliği
        if client_ip in rate_limit_cache:
            last_request = rate_limit_cache[client_ip]
            if current_time - last_request < RATE_LIMIT_SECONDS:
                return False

        rate_limit_cache[client_ip] = current_time

        # Eski kayıtları temizle
        cutoff_time = current_time - 3600
        rate_limit_cache = {
            ip: req_time for ip, req_time in rate_limit_cache.items()
            if req_time > cutoff_time
        }

    return True


@app.route('/', methods=['GET'])
def get_secret_word():
    """Ana endpoint - gizli kelimeyi döndür"""
    try:
        client_ip = request.environ.get(
            'HTTP_X_FORWARDED_FOR',
            request.environ.get('REMOTE_ADDR', 'unknown')
        )

        if not check_rate_limit(client_ip):
            logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            return jsonify({
                'success': False,
                'error': 'Too many requests',
                'retry_after': RATE_LIMIT_SECONDS
            }), 429, {'Retry-After': str(RATE_LIMIT_SECONDS)}

        word_info = get_current_secret_word()

        response = {
            'success': True,
            'secret_word': word_info['word'],
            'timestamp': word_info['current_time'],
            'interval_info': {
                'interval_index': word_info['interval_index'],
                'next_change_in_seconds': word_info['remaining_seconds'],
                'next_change_time': datetime.fromtimestamp(
                    word_info['next_change_time']
                ).strftime('%Y-%m-%d %H:%M:%S')
            },
            'server_info': {
                'python_version': f"{os.sys.version_info.major}.{os.sys.version_info.minor}.{os.sys.version_info.micro}",
                'server_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'timezone': str(datetime.now().astimezone().tzinfo),
                'word_pool_size': len(WORD_POOL)
            }
        }

        debug = request.args.get('debug', '').lower() in ['1', 'true', 'yes']
        if debug:
            with cache_lock:
                response['debug'] = {
                    'client_ip': client_ip,
                    'user_agent': request.headers.get('User-Agent', 'unknown'),
                    'word_index': word_info['interval_index'] % len(WORD_POOL),
                    'interval_seconds': 180,
                    'rate_limit_cache_size': len(rate_limit_cache)
                }

        logger.info(f"Secret word served: {word_info['word']} to {client_ip}")
        return jsonify(response)

    except Exception as e:
        logger.error(f"Error serving secret word: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'message': str(e)
        }), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Sağlık kontrolü endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': int(time.time()),
        'server_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'uptime': 'running'
    })


@app.route('/stats', methods=['GET'])
def get_stats():
    """İstatistik endpoint"""
    word_info = get_current_secret_word()
    with cache_lock:
        active_ips = len(rate_limit_cache)

    return jsonify({
        'current_word': word_info['word'],
        'word_pool_size': len(WORD_POOL),
        'interval_minutes': 3,
        'next_change_in': word_info['remaining_seconds'],
        'total_intervals_passed': word_info['interval_index'],
        'rate_limit_seconds': RATE_LIMIT_SECONDS,
        'active_ips': active_ips
    })


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found',
        'available_endpoints': [
            '/ - Get secret word',
            '/health - Health check',
            '/stats - Statistics',
            '/?debug=1 - Debug mode'
        ]
    }), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error',
        'message': 'Something went wrong on the server'
    }), 500


def cleanup_task():
    """Eski rate limit kayıtlarını temizle"""
    global rate_limit_cache
    while True:
        try:
            current_time = time.time()
            cutoff_time = current_time - 3600

            with cache_lock:
                old_size = len(rate_limit_cache)
                rate_limit_cache = {
                    ip: req_time for ip, req_time in rate_limit_cache.items()
                    if req_time > cutoff_time
                }
                new_size = len(rate_limit_cache)

            if old_size != new_size:
                logger.info(f"Cleaned up rate limit cache: {old_size} -> {new_size}")

            time.sleep(3600)
        except Exception as e:
            logger.error(f"Cleanup task error: {str(e)}")
            time.sleep(60)


if __name__ == '__main__':
    cleanup_thread = threading.Thread(target=cleanup_task, daemon=True)
    cleanup_thread.start()

    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('DEBUG', 'False').lower() == 'true'

    logger.info(f"Starting Secret Word API server on port {port}")
    logger.info(f"Word pool size: {len(WORD_POOL)}")
    logger.info(f"Update interval: 3 minutes")

    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug_mode,
        threaded=True
    )
