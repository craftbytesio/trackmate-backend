if [ "$1" = "production" ]; then
    docker-compose -f docker-compose.production.yml up
else
    docker-compose -f docker-compose.development.yml up
fi