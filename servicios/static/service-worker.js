// service-worker.js

const CACHE_NAME = 'itech-cache-v1';
// Rutas CRÍTICAS: Código HTML, CSS, JS y la API que maneja el guardado.
const urlsToCache = [
    '/',
    '/login/',
    '/calendario/',
    '/registro_temp/', // No se puede cachear dinámicamente, pero intentamos
    '/static/manifest.json',
    // Asegúrate de incluir aquí las rutas a tus archivos críticos (Tailwind, FontAwesome, logo)
    // Ejemplo: '/static/img/logo.JPEG', 
    'https://cdn.tailwindcss.com',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css',
];

// ----------------------------------------------------
// PASO 1: INSTALACIÓN - Almacenar Archivos Críticos
// ----------------------------------------------------
self.addEventListener('install', event => {
    console.log('[Service Worker] Instalando y cacheando shell estático');
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                // Abre el caché e intenta añadir todos los archivos
                return cache.addAll(urlsToCache).catch(error => {
                    console.error('[Service Worker] Error al cachear: algunos recursos no se pudieron guardar.', error);
                    // No fallamos la instalación si algunos archivos de terceros fallan.
                });
            })
    );
});

// ----------------------------------------------------
// PASO 2: FETCH - Servir Archivos desde la Caché (Modo Offline)
// ----------------------------------------------------
self.addEventListener('fetch', event => {
    // Interceptar peticiones solo si no son la API de guardado de datos
    const requestUrl = new URL(event.request.url);
    
    // Si es la API de GUARDADO DE DATOS, la dejamos pasar.
    if (requestUrl.pathname.endsWith('/registro-tecnico/guardar/')) {
        // La lógica para guardar offline (IndexedDB) debe estar en el CLIENTE (main script).
        // El Service Worker solo intercepta si la petición de envío falla para reintentarla (Background Sync),
        // pero la recolección de datos y la DataURL de firmas se maneja en el script principal.
        return; 
    }

    // Para el resto de peticiones (HTML, CSS, JS, imágenes), intentar la caché primero
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                // Devolver el recurso cacheado si existe
                if (response) {
                    console.log(`[Service Worker] Sirviendo desde caché: ${event.request.url}`);
                    return response;
                }
                
                // Si no está en caché, intentar la red (y luego cachear si tiene éxito)
                return fetch(event.request).then(networkResponse => {
                    // Si la respuesta es válida (200) y no es opaca (cross-origin), cachearla
                    if (networkResponse && networkResponse.status === 200 && networkResponse.type === 'basic') {
                        const responseToCache = networkResponse.clone();
                        caches.open(CACHE_NAME).then(cache => {
                            // Caching dinámico para nuevas rutas o archivos
                            cache.put(event.request, responseToCache);
                        });
                    }
                    return networkResponse;
                }).catch(error => {
                    console.log('[Service Worker] Fallo de red:', event.request.url, error);
                    // Podrías devolver una página de error offline aquí
                });
            })
    );
});