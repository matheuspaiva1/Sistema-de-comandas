# Rodar apenas o banco de dados e o mongo-express:
docker compose -f docker/docker-compose.db.yaml --env-file .env up

# Rodar apenas o MinIO:
docker compose -f docker/docker-compose.storage.yaml --env-file .env up

# Rodar a api:
docker compose -f docker/docker-compose.yaml --env-file .env up

# Para rodar todos de uma vez:
docker compose -f docker/docker-compose.storage.yaml --env-file .env -f docker/docker-compose.db.yaml --env-file .env -f docker/docker-compose.yaml --env-file .env up

# Parar os containers:
docker compose -f docker/docker-compose.db.yaml --env-file .env down
docker compose -f docker/docker-compose.storage.yaml --env-file .env down
docker compose -f docker/docker-compose.yaml --env-file .env down
