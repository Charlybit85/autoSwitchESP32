# AutoSwitchESP32 — migración a Laravel

El código Flask original se conserva. `backend/` contiene Laravel 13, el panel Blade y el backend; `docker/` contiene PHP-FPM 8.5 y Nginx. Docker Compose utiliza un volumen persistente para SQLite, sesiones y caché. No se publica la base de datos ni PHP-FPM.

## Inicio

Desde esta carpeta, ejecutar `./scripts/setup.sh` para construir, migrar y arrancar. Después crear el usuario con el comando indicado abajo. Pasos equivalentes:

```sh
# Si backend/.env no existe, copiar backend/.env.example y completar APP_KEY y DEVICE_TOKEN.
docker compose build
docker compose run --rm app php -r "touch('/app/storage/database.sqlite');"
docker compose run --rm app php artisan migrate --force
docker compose run --rm app php artisan app:create-user administrador
docker compose up -d
```

Abrir http://localhost:8080. La contraseña se solicita de forma oculta; no hay usuarios predeterminados. La instalación local preparada ya tiene una APP_KEY y DEVICE_TOKEN aleatorios en `backend/.env`, que no se versiona. Para una instalación nueva, generar APP_KEY con `docker compose run --rm app php artisan key:generate --show` y un token con `openssl rand -hex 32`; guardar sus resultados en `.env` sin publicarlos. No cambiar APP_KEY en instalaciones existentes.

## Estructura

- `app/Http/Controllers`: autenticación y control del relevador.
- `app/Http/Middleware/DeviceToken.php`: autenticación del hardware.
- `app/Models/Relay.php`: estado deseado/reportado persistente.
- `database/migrations`: esquema versionado.
- `routes/web.php`: panel y endpoints con sesión y CSRF.
- `routes/api.php`: API del dispositivo, sin cookies, con Bearer token.
- `resources/views`, `public/css`, `public/js`: panel migrado del original.

Las rutas de esta lista son relativas a `backend/`.

## Contrato de comunicación

Se conservan `/estado`, `/encender`, `/apagar` y `/api/led` para el panel. Las escrituras requieren sesión y CSRF. `/api/led` acepta `{"estado":"on"}` o `{"estado":"off"}`.

El hardware consulta `GET /api/esp32/config` (respuesta `{"led":"on"}` o `off`) y reporta `POST /api/esp32/estado` con `{"led":"on"}` o `off`. Ambas rutas requieren `Authorization: Bearer <DEVICE_TOKEN>`. Cada orden devuelve 202: el estado reportado cambia cuando el dispositivo confirma. No es una confirmación eléctrica del relevador.

El simulador usa `SERVER_URL` y `DEVICE_TOKEN` del entorno. El firmware original utiliza ESP8266WiFi, aunque se llama ESP32: definir la placa real antes de compilar. El encabezado Bearer ya se añadió a ambos HTTPClient. Copiar `Esp32/config.example.h` a `Esp32/config.h` y configurar WiFi, host y token. No hay compatibilidad deliberada con dispositivos sin token. Las credenciales WiFi incrustadas en el original deben sustituirse y rotarse si fueron reales.

## Seguridad y despliegue

Sesiones regeneradas al iniciar sesión, CSRF, contraseñas hash, validación de on/off, límites de solicitudes y contenedores sin privilegios. El puerto se limita a 127.0.0.1. Para acceso desde hardware en LAN, configurar BIND_ADDRESS y firewall; para uso fuera de una máquina de desarrollo, poner un proxy HTTPS y configurar APP_URL y SESSION_SECURE_COOKIE=true. El firmware también debe validar el certificado TLS; no usar setInsecure(). El token viaja en claro sobre HTTP, por lo que HTTP solo es apropiado para pruebas locales aisladas.

No ejecutar Flask y Laravel contra la misma base de datos. Los hashes Werkzeug de `usuarios.db` no son compatibles con Laravel: recrear usuarios con el comando y asignar contraseñas nuevas. El estado Flask era volátil; no hay estado histórico que importar. Hacer respaldo antes de mover datos reales. La base nueva está en el volumen de Docker: no usar `docker compose down -v` si se desea conservarla. Detener la aplicación antes de respaldar SQLite.

Esta implementación controla un único relevador, como el original; no incorpora roles ni múltiples dispositivos. No arrancar simulador y hardware a la vez con el mismo token.

## Verificación

```sh
docker compose ps
docker compose logs --tail=50
docker build --target test -f docker/Dockerfile -t autoswitch-tests .
docker run --rm autoswitch-tests
```

Para copiar el proyecto a otro servidor: copiar código y `backend/.env` por un canal seguro, respaldar/restaurar el volumen si se necesitan los datos existentes y ejecutar `scripts/setup.sh`. No copiar ni publicar secretos en Git. `backend/composer.lock` fija las versiones resueltas, incluido Laravel 13.42.0.
