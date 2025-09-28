// JavaScript tabanlı Gizli Kelime API
// PHP çalışmadığında kullanılır

// CORS headers için
if (typeof window === 'undefined') {
    // Node.js ortamında
    const headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Accept',
        'Content-Type': 'application/json'
    };
}

// Türkçe gizli kelime havuzu
const wordPool = [
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
    'sabah', 'öğle', 'akşam', 'gece', 'gün',
    'pazartesi', 'salı', 'çarşamba', 'perşembe', 'cuma',
    'ocak', 'şubat', 'mart', 'nisan', 'mayıs',
    'haziran', 'temmuz', 'ağustos', 'eylül', 'ekim'
];

// 3 dakikalık zaman dilimlerine göre kelime seç
function getCurrentSecretWord() {
    const currentTime = Math.floor(Date.now() / 1000);
    const intervalSeconds = 3 * 60; // 3 dakika = 180 saniye
    const intervalIndex = Math.floor(currentTime / intervalSeconds);
    const wordIndex = intervalIndex % wordPool.length;
    const selectedWord = wordPool[wordIndex];
    
    const nextChangeTime = (intervalIndex + 1) * intervalSeconds;
    const remainingSeconds = nextChangeTime - currentTime;
    
    return {
        word: selectedWord,
        intervalIndex: intervalIndex,
        currentTime: currentTime,
        nextChangeTime: nextChangeTime,
        remainingSeconds: remainingSeconds
    };
}

// Rate limiting (basit)
const rateLimitCache = new Map();

function checkRateLimit(clientIP) {
    const now = Date.now();
    const lastRequest = rateLimitCache.get(clientIP) || 0;
    
    if (now - lastRequest < 2000) { // 2 saniye
        return false;
    }
    
    rateLimitCache.set(clientIP, now);
    return true;
}

// Ana API fonksiyonu
function getSecretWordAPI(clientIP = 'unknown', debug = false) {
    try {
        // Rate limiting kontrolü
        if (!checkRateLimit(clientIP)) {
            return {
                success: false,
                error: 'Too many requests',
                retry_after: 2
            };
        }
        
        // Gizli kelimeyi al
        const secretWordInfo = getCurrentSecretWord();
        
        // Başarılı yanıt
        const response = {
            success: true,
            secret_word: secretWordInfo.word,
            timestamp: secretWordInfo.currentTime,
            interval_info: {
                interval_index: secretWordInfo.intervalIndex,
                next_change_in_seconds: secretWordInfo.remainingSeconds,
                next_change_time: new Date(secretWordInfo.nextChangeTime * 1000).toISOString()
            },
            server_info: {
                php_version: 'JavaScript Alternative v1.0',
                server_time: new Date().toISOString(),
                timezone: Intl.DateTimeFormat().resolvedOptions().timeZone
            }
        };
        
        // Debug modu
        if (debug) {
            response.debug = {
                word_pool_size: wordPool.length,
                current_time: secretWordInfo.currentTime,
                interval_seconds: 180,
                word_index: secretWordInfo.intervalIndex % wordPool.length,
                client_ip: clientIP,
                rate_limit_cache_size: rateLimitCache.size
            };
        }
        
        return response;
        
    } catch (error) {
        return {
            success: false,
            error: 'Internal server error',
            message: error.message
        };
    }
}

// Browser ortamında global olarak kullanılabilir hale getir
if (typeof window !== 'undefined') {
    window.getSecretWordAPI = getSecretWordAPI;
    window.getCurrentSecretWord = getCurrentSecretWord;
    
    // JSONP desteği
    window.secretWordJSONP = function(callback) {
        const result = getSecretWordAPI();
        if (typeof callback === 'function') {
            callback(result);
        }
        return result;
    };
}

// Node.js ortamında export et
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        getSecretWordAPI,
        getCurrentSecretWord,
        wordPool
    };
}

// Tarayıcıda doğrudan çağrılırsa JSON döndür
if (typeof window !== 'undefined' && window.location) {
    const urlParams = new URLSearchParams(window.location.search);
    const debug = urlParams.get('debug') === '1';
    const clientIP = 'browser-client';
    
    const result = getSecretWordAPI(clientIP, debug);
    
    // JSON olarak göster
    if (document.body) {
        document.body.innerHTML = '<pre>' + JSON.stringify(result, null, 2) + '</pre>';
    } else {
        console.log(JSON.stringify(result, null, 2));
    }
}
