#!/bin/bash
# SSL sertifikat birinchi marta olish uchun skript
# Serverda bir marta ishga tushiring

set -e

EMAIL="abdufattohfattoyev0@gmail.com"
DOMAIN="andro-boss.uz"

echo "==> 1. Nginx'ni faqat HTTP rejimida ishga tushiramiz..."
docker compose up -d nginx

echo "==> 2. Certbot orqali SSL sertifikat olamiz..."
docker compose run --rm certbot certonly \
    --webroot \
    --webroot-path=/var/www/certbot \
    --email "$EMAIL" \
    --agree-tos \
    --no-eff-email \
    -d "$DOMAIN" \
    -d "www.$DOMAIN"

echo "==> 3. Barcha containerlarni qayta ishga tushiramiz..."
docker compose down
docker compose up -d

echo "==> SSL sertifikat muvaffaqiyatli o'rnatildi!"
echo "==> Sayt: https://$DOMAIN"
