cat oplossing.c | nc localhost 5432 > oplossing
chmod +x oplossing
docker run -v "$(pwd)"/oplossing:/app/oplossing alpine /app/oplossing