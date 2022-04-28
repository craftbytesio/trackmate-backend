if [ "$1" = "production" ]; then
    docker-compose -f docker-compose.production.yml up -d
else
    docker-compose -f docker-compose.development.yml up -d
fi