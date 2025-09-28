<?php
/**
 * Gizli Kelime API - Hosting için Index.php Versiyonu
 * Bu dosyayı hosting sağlayıcınızın ana dizinine yükleyin
 */

// HATA RAPORLAMASI KAPALI (JSON bozmasın)
error_reporting(0);
ini_set('display_errors', 0);

// JSON HEADER'LARI - EN ÖNEMLİ KISIM!
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, Accept, User-Agent');

// OPTIONS isteği için
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

// SADECE JSON ÇIKTI - HİÇBİR HTML YOK!
try {
    // Türkçe gizli kelime havuzu
    $wordPool = [
        'güvenlik',
        'sistem',
        'kapı',
        'giriş',
        'çıkış',
        'merhaba',
        'hoşgeldin',
        'teşekkür',
        'lütfen',
        'tamam',
        'başla',
        'bitir',
        'devam',
        'dur',
        'bekle',
        'açık',
        'kapalı',
        'yeşil',
        'kırmızı',
        'mavi',
        'bir',
        'iki',
        'üç',
        'dört',
        'beş',
        'altı',
        'yedi',
        'sekiz',
        'dokuz',
        'on',
        'güzel',
        'harika',
        'mükemmel',
        'başarılı',
        'doğru',
        'ev',
        'ofis',
        'masa',
        'sandalye',
        'pencere',
        'telefon',
        'bilgisayar',
        'tablet',
        'kamera',
        'mikrofon',
        'kitap',
        'kalem',
        'kağıt',
        'dosya',
        'klasör',
        'su',
        'çay',
        'kahve',
        'ekmek',
        'peynir',
        'sabah',
        'öğle',
        'akşam',
        'gece',
        'gün',
        'pazartesi',
        'salı',
        'çarşamba',
        'perşembe',
        'cuma',
        'ocak',
        'şubat',
        'mart',
        'nisan',
        'mayıs',
        'haziran',
        'temmuz',
        'ağustos',
        'eylül',
        'ekim'
    ];

    // 3 dakikalık zaman dilimlerine göre kelime seç
    $currentTime = time();
    $intervalSeconds = 3 * 60; // 3 dakika = 180 saniye
    $intervalIndex = floor($currentTime / $intervalSeconds);
    $wordIndex = $intervalIndex % count($wordPool);
    $selectedWord = $wordPool[$wordIndex];
    
    // Sonraki değişim zamanı
    $nextChangeTime = ($intervalIndex + 1) * $intervalSeconds;
    $remainingSeconds = $nextChangeTime - $currentTime;
    
    // Basit rate limiting
    $clientIP = $_SERVER['REMOTE_ADDR'] ?? 'unknown';
    $cacheFile = sys_get_temp_dir() . '/rate_limit_' . md5($clientIP);
    
    if (file_exists($cacheFile)) {
        $lastRequest = (int)file_get_contents($cacheFile);
        if (time() - $lastRequest < 2) { // 2 saniyede bir istek
            http_response_code(429);
            echo json_encode([
                'success' => false,
                'error' => 'Too many requests',
                'retry_after' => 2
            ], JSON_UNESCAPED_UNICODE);
            exit();
        }
    }
    
    file_put_contents($cacheFile, time());
    
    // BAŞARILI YANIT - SADECE JSON
    $response = [
        'success' => true,
        'secret_word' => $selectedWord,
        'timestamp' => $currentTime,
        'interval_info' => [
            'interval_index' => $intervalIndex,
            'next_change_in_seconds' => $remainingSeconds,
            'next_change_time' => date('Y-m-d H:i:s', $nextChangeTime)
        ],
        'server_info' => [
            'php_version' => PHP_VERSION,
            'server_time' => date('Y-m-d H:i:s'),
            'timezone' => date_default_timezone_get()
        ]
    ];
    
    // Debug modu
    if (isset($_GET['debug']) && $_GET['debug'] === '1') {
        $response['debug'] = [
            'word_pool_size' => count($wordPool),
            'current_time' => $currentTime,
            'interval_seconds' => $intervalSeconds,
            'word_index' => $wordIndex,
            'client_ip' => $clientIP
        ];
    }
    
    // JSON ÇIKTI - HİÇBİR EK KARAKTER YOK
    echo json_encode($response, JSON_UNESCAPED_UNICODE);
    
} catch (Exception $e) {
    // HATA DURUMUNDA DA SADECE JSON
    http_response_code(500);
    echo json_encode([
        'success' => false,
        'error' => 'Internal server error',
        'message' => $e->getMessage()
    ], JSON_UNESCAPED_UNICODE);
} catch (Error $e) {
    // FATAL ERROR DURUMUNDA DA SADECE JSON
    http_response_code(500);
    echo json_encode([
        'success' => false,
        'error' => 'Fatal error',
        'message' => $e->getMessage()
    ], JSON_UNESCAPED_UNICODE);
}

// HİÇBİR EK ÇIKTI YOK - SADECE JSON!
exit();
?>
