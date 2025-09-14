# Ultimate FastAPI Backend

Demo of a FastAPI Backend

---

## Tech

- FastAPI
- Python
- Sqlite

---

## Start

We will use the fastapi cli to run the fastapi backend.

```shell
fastapi dev
```

---

## Session Blacklists with Redis

You can run your Redis server whereever you like. I like to run mine with Docker.

```shell
docker run -d --name redis-1 -v redis-1-data:/data -p 6679:6379 redis/redis-stack-server:latest
```

This will start Redis on port `6679` I picked this one to not conflict with the default `6379`. But do whatever works for you.

Whatever you choose make sure to add these items to your `.env` file.

```shell
REDIS_HOST=localhost
REDIS_PORT=6679
```

---
