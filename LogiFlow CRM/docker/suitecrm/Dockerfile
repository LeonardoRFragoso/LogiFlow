# =============================================
# LogiFlow CRM - SuiteCRM PHP-FPM Dockerfile
# =============================================
FROM php:8.1-fpm

LABEL maintainer="LogiFlow CRM <contato@logiflow.com.br>"
LABEL description="SuiteCRM 8.x with PHP 8.1 and required extensions"

# Argumentos de build
ARG SUITECRM_VERSION=8.4.0
ARG DEBIAN_FRONTEND=noninteractive

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    git \
    curl \
    zip \
    unzip \
    libpng-dev \
    libjpeg-dev \
    libfreetype6-dev \
    libonig-dev \
    libxml2-dev \
    libzip-dev \
    libicu-dev \
    libldap2-dev \
    libcurl4-openssl-dev \
    cron \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Configurar e instalar extensões PHP
RUN docker-php-ext-configure gd --with-freetype --with-jpeg \
    && docker-php-ext-install -j$(nproc) \
        pdo \
        pdo_mysql \
        mysqli \
        gd \
        mbstring \
        xml \
        zip \
        intl \
        ldap \
        curl \
        opcache \
        bcmath \
        soap

# Instalar Redis extension
RUN pecl install redis \
    && docker-php-ext-enable redis

# Instalar Composer
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# Configurar diretório de trabalho
WORKDIR /var/www/html

# Criar usuário não-root para execução
RUN groupadd -g 1000 www \
    && useradd -u 1000 -ms /bin/bash -g www www

# Configurar permissões
RUN chown -R www:www /var/www/html

# Copiar configurações
COPY php.ini /usr/local/etc/php/conf.d/custom.ini
COPY www.conf /usr/local/etc/php-fpm.d/www.conf
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY crontab /etc/cron.d/suitecrm-cron

# Configurar cron (formato /etc/cron.d/ não precisa de crontab -i)
RUN chmod 0644 /etc/cron.d/suitecrm-cron \
    && touch /var/log/cron.log

# Expor porta PHP-FPM
EXPOSE 9000

# Iniciar com Supervisor
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
