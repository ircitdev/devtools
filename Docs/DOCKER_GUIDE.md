# Docker Environment - Руководство

## ✅ Docker окружение настроено!

### Что создано:

**Docker Compose файлы:**
- `postgres.yml` - PostgreSQL 16
- `redis.yml` - Redis 7
- `mongodb.yml` - MongoDB 7
- `mysql.yml` - MySQL 8
- `fullstack.yml` - Все сервисы вместе

**Скрипты управления:**
- `start-all.ps1` - Запустить все контейнеры
- `stop-all.ps1` - Остановить все контейнеры
- `status.ps1` - Статус контейнеров

**Директории:**
- `Docker/compose/` - Compose файлы
- `Docker/volumes/` - Данные контейнеров
- `Docker/data/` - Дополнительные данные

## 🚀 Использование

### Запуск всех сервисов

```powershell
# Через менеджер (рекомендуется)
.\DevTools-Manager.ps1 docker start

# Или напрямую
.\Docker\start-all.ps1
```

### Остановка

```powershell
.\DevTools-Manager.ps1 docker stop
```

### Статус

```powershell
.\DevTools-Manager.ps1 docker status
```

## 🗄️ Базы данных

### PostgreSQL

**Подключение:**
```
Host: localhost
Port: 5432
User: developer
Password: dev_password
Database: devdb
```

**Запуск только PostgreSQL:**
```bash
docker-compose -f D:\DevTools\Docker\compose\postgres.yml up -d
```

**Подключение через psql:**
```bash
docker exec -it devtools_postgres psql -U developer -d devdb
```

**Connection string:**
```
postgresql://developer:dev_password@localhost:5432/devdb
```

### MySQL

**Подключение:**
```
Host: localhost
Port: 3306
User: developer
Password: dev_password
Database: devdb
Root Password: root_password
```

**Запуск только MySQL:**
```bash
docker-compose -f D:\DevTools\Docker\compose\mysql.yml up -d
```

**Подключение через mysql:**
```bash
docker exec -it devtools_mysql mysql -u developer -p
# Password: dev_password
```

**Connection string:**
```
mysql://developer:dev_password@localhost:3306/devdb
```

### MongoDB

**Подключение:**
```
Host: localhost
Port: 27017
User: developer
Password: dev_password
```

**Запуск только MongoDB:**
```bash
docker-compose -f D:\DevTools\Docker\compose\mongodb.yml up -d
```

**Подключение через mongosh:**
```bash
docker exec -it devtools_mongo mongosh -u developer -p dev_password
```

**Connection string:**
```
mongodb://developer:dev_password@localhost:27017
```

### Redis

**Подключение:**
```
Host: localhost
Port: 6379
```

**Запуск только Redis:**
```bash
docker-compose -f D:\DevTools\Docker\compose\redis.yml up -d
```

**Подключение через redis-cli:**
```bash
docker exec -it devtools_redis redis-cli
```

## 🔧 Примеры использования

### Python + PostgreSQL

```python
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    user="developer",
    password="dev_password",
    database="devdb"
)

cursor = conn.cursor()
cursor.execute("SELECT version();")
print(cursor.fetchone())
conn.close()
```

### Python + SQLAlchemy

```python
from sqlalchemy import create_engine

engine = create_engine('postgresql://developer:dev_password@localhost:5432/devdb')
conn = engine.connect()
result = conn.execute("SELECT 1")
print(result.fetchone())
conn.close()
```

### Node.js + PostgreSQL

```javascript
const { Client } = require('pg');

const client = new Client({
  host: 'localhost',
  port: 5432,
  user: 'developer',
  password: 'dev_password',
  database: 'devdb'
});

client.connect();
client.query('SELECT NOW()', (err, res) => {
  console.log(res.rows);
  client.end();
});
```

### Python + Redis

```python
import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)
r.set('key', 'value')
print(r.get('key'))
```

### Node.js + MongoDB

```javascript
const { MongoClient } = require('mongodb');

const url = 'mongodb://developer:dev_password@localhost:27017';
const client = new MongoClient(url);

async function run() {
  await client.connect();
  const db = client.db('devdb');
  const collection = db.collection('users');
  await collection.insertOne({ name: 'Alice' });
  console.log(await collection.find({}).toArray());
  await client.close();
}

run();
```

## 📊 Управление контейнерами

### Просмотр логов

```bash
# Все логи
docker-compose -f D:\DevTools\Docker\compose\fullstack.yml logs

# Только PostgreSQL
docker logs devtools_postgres

# Следить за логами
docker logs -f devtools_postgres
```

### Перезапуск контейнера

```bash
docker restart devtools_postgres
```

### Остановка конкретного контейнера

```bash
docker stop devtools_postgres
```

### Запуск конкретного контейнера

```bash
docker start devtools_postgres
```

### Удаление контейнера

```bash
# Остановить и удалить
docker-compose -f D:\DevTools\Docker\compose\postgres.yml down

# Удалить с данными
docker-compose -f D:\DevTools\Docker\compose\postgres.yml down -v
```

## 💾 Бэкап и восстановление

### PostgreSQL

**Бэкап:**
```bash
docker exec devtools_postgres pg_dump -U developer devdb > backup.sql
```

**Восстановление:**
```bash
docker exec -i devtools_postgres psql -U developer devdb < backup.sql
```

### MySQL

**Бэкап:**
```bash
docker exec devtools_mysql mysqldump -u developer -pdev_password devdb > backup.sql
```

**Восстановление:**
```bash
docker exec -i devtools_mysql mysql -u developer -pdev_password devdb < backup.sql
```

### MongoDB

**Бэкап:**
```bash
docker exec devtools_mongo mongodump --username developer --password dev_password --out /backup
```

**Восстановление:**
```bash
docker exec devtools_mongo mongorestore --username developer --password dev_password /backup
```

## 🔍 Полезные команды

### Просмотр всех контейнеров

```bash
docker ps -a
```

### Просмотр использования ресурсов

```bash
docker stats
```

### Очистка

```bash
# Удалить остановленные контейнеры
docker container prune

# Удалить неиспользуемые образы
docker image prune

# Удалить неиспользуемые volumes
docker volume prune

# Очистить всё
docker system prune -a
```

### Войти в контейнер

```bash
# PostgreSQL
docker exec -it devtools_postgres bash

# MongoDB
docker exec -it devtools_mongo bash

# Redis
docker exec -it devtools_redis sh
```

## 🆘 Решение проблем

### Контейнер не запускается

```bash
# Проверить логи
docker logs devtools_postgres

# Проверить статус
docker ps -a

# Пересоздать
docker-compose -f D:\DevTools\Docker\compose\postgres.yml down
docker-compose -f D:\DevTools\Docker\compose\postgres.yml up -d
```

### Порт занят

```bash
# Проверить что использует порт
netstat -ano | findstr :5432

# Остановить процесс
taskkill /PID <PID> /F
```

### Volumes заполнены

```bash
# Посмотреть размер
docker system df

# Очистить старые данные
docker volume prune
```

### Docker Desktop не запускается

1. Перезагрузите компьютер
2. Запустите Docker Desktop от администратора
3. Проверьте WSL2: `wsl --status`

## 📚 Ресурсы

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [PostgreSQL Docker](https://hub.docker.com/_/postgres)
- [MySQL Docker](https://hub.docker.com/_/mysql)
- [MongoDB Docker](https://hub.docker.com/_/mongo)
- [Redis Docker](https://hub.docker.com/_/redis)

---

**Docker окружение готово!** 🐳

**Быстрый старт:**
```powershell
.\DevTools-Manager.ps1 docker start
```
