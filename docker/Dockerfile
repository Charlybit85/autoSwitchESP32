FROM php:8.5-fpm-alpine AS runtime
RUN apk add --no-cache unzip
COPY --from=composer/composer:2-bin /composer /usr/local/bin/composer
COPY docker/php.ini /usr/local/etc/php/conf.d/99-app.ini
WORKDIR /app
COPY backend/composer.* ./
RUN composer install --no-dev --no-scripts --prefer-dist --no-interaction
COPY backend/ ./
RUN rm -rf tests
RUN composer dump-autoload --optimize --no-dev \
 && mkdir -p storage/framework/cache storage/framework/sessions storage/framework/views storage/logs bootstrap/cache \
 && chown -R www-data:www-data /app
USER www-data
EXPOSE 9000
CMD ["php-fpm", "-F"]

FROM runtime AS test
COPY --chown=www-data:www-data backend/tests /app/tests
USER root
RUN composer install --prefer-dist --no-interaction \
 && chown -R www-data:www-data /app
USER www-data
ENV APP_ENV=testing DB_CONNECTION=sqlite DB_DATABASE=:memory: SESSION_DRIVER=array CACHE_STORE=array
CMD ["php", "artisan", "test"]
