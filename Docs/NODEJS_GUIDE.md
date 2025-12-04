# Node.js Environment - Руководство

## ✅ Node.js окружение настроено!

### Что установлено:

**Глобальные пакеты:**
- ✅ **TypeScript** 5.9.3 - Типизированный JavaScript
- ✅ **ts-node** 10.9.2 - Выполнение TypeScript напрямую
- ✅ **nodemon** 3.1.11 - Авто-перезапуск при изменениях
- ✅ **pm2** 6.0.14 - Process manager для продакшена
- ✅ **http-server** 14.1.1 - Простой HTTP сервер
- ✅ **eslint** 9.39.1 - JavaScript/TypeScript линтер
- ✅ **prettier** 3.7.4 - Форматировщик кода
- ✅ **yarn** 1.22.22 - Альтернативный package manager
- ✅ **pnpm** 10.24.0 - Быстрый package manager

**Конфигурация:**
- Global modules: `D:\DevTools\NodeJS\global_modules`
- npm cache: `D:\DevTools\Caches\npm`
- npm config: `D:\DevTools\NodeJS\.npmrc`

## 🚀 Использование

### Активация окружения

```powershell
# Добавить Node.js инструменты в PATH
.\Scripts\node-env.ps1
```

После активации доступны все глобальные инструменты:
```bash
tsc --version        # TypeScript compiler
ts-node script.ts    # Запустить TypeScript
nodemon app.js       # Авто-перезапуск
pm2 start app.js     # Process manager
eslint .             # Проверка кода
prettier --write .   # Форматирование
```

### Создание нового проекта

```powershell
# JavaScript проект
.\Scripts\create-node-project.ps1 my-app -Template javascript

# TypeScript проект
.\Scripts\create-node-project.ps1 my-app -Template typescript

# Express.js сервер
.\Scripts\create-node-project.ps1 my-api -Template express
```

### Быстрый запуск Node.js

```powershell
# Запустить скрипт
.\Scripts\quick-node.ps1 script.js

# Или напрямую
node script.js
```

## 📦 Работа с пакетами

### npm (встроенный)

```bash
# Установить пакет локально
npm install express

# Установить dev зависимость
npm install --save-dev jest

# Установить глобально
npm install -g package-name

# Обновить пакеты
npm update
```

### yarn (установлен)

```bash
# Инициализация
yarn init

# Установка пакетов
yarn add express
yarn add --dev jest

# Запуск скриптов
yarn start
yarn test
```

### pnpm (установлен, быстрее npm)

```bash
# Установка пакетов
pnpm install express
pnpm add -D jest

# Запуск
pnpm start
```

## 🔧 TypeScript

### Создание TypeScript проекта

```bash
# Создать tsconfig.json
tsc --init

# Скомпилировать
tsc

# Скомпилировать и запустить
ts-node src/index.ts
```

### Пример tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true
  }
}
```

### Пример TypeScript кода

```typescript
// src/index.ts
interface User {
  name: string;
  age: number;
}

const greet = (user: User): string => {
  return `Hello, ${user.name}! You are ${user.age} years old.`;
};

const user: User = { name: 'John', age: 30 };
console.log(greet(user));
```

## 🔄 Nodemon (авто-перезапуск)

### Базовое использование

```bash
# Запустить с авто-перезапуском
nodemon app.js

# TypeScript
nodemon --exec ts-node src/index.ts
```

### Конфигурация nodemon.json

```json
{
  "watch": ["src"],
  "ext": "ts,js",
  "ignore": ["src/**/*.spec.ts"],
  "exec": "ts-node ./src/index.ts"
}
```

### package.json scripts

```json
{
  "scripts": {
    "start": "node index.js",
    "dev": "nodemon index.js",
    "dev:ts": "nodemon --exec ts-node src/index.ts"
  }
}
```

## 🎯 PM2 (Process Manager)

### Запуск приложений

```bash
# Запустить приложение
pm2 start app.js --name my-app

# TypeScript
pm2 start ts-node -- --project tsconfig.json src/index.ts

# С переменными окружения
pm2 start app.js --name my-app --env production

# Кластерный режим
pm2 start app.js -i max
```

### Управление процессами

```bash
# Список процессов
pm2 list

# Логи
pm2 logs

# Перезапуск
pm2 restart my-app

# Остановка
pm2 stop my-app

# Удаление
pm2 delete my-app

# Мониторинг
pm2 monit
```

### ecosystem.config.js

```javascript
module.exports = {
  apps: [{
    name: 'my-app',
    script: './app.js',
    instances: 2,
    exec_mode: 'cluster',
    env: {
      NODE_ENV: 'development'
    },
    env_production: {
      NODE_ENV: 'production'
    }
  }]
};
```

## 🌐 HTTP Server

### Простой файловый сервер

```bash
# Запустить в текущей папке
http-server

# На конкретном порту
http-server -p 8080

# С CORS
http-server --cors

# Открыть в браузере
http-server -o
```

## 🎨 ESLint (линтер)

### Инициализация

```bash
# Создать конфигурацию
npm init @eslint/config
```

### .eslintrc.json

```json
{
  "env": {
    "node": true,
    "es2021": true
  },
  "extends": "eslint:recommended",
  "parserOptions": {
    "ecmaVersion": "latest"
  },
  "rules": {
    "semi": ["error", "always"],
    "quotes": ["error", "single"]
  }
}
```

### Использование

```bash
# Проверить код
eslint .

# Автофикс
eslint . --fix

# Проверить конкретный файл
eslint src/index.js
```

## ✨ Prettier (форматирование)

### .prettierrc

```json
{
  "semi": true,
  "trailingComma": "all",
  "singleQuote": true,
  "printWidth": 80,
  "tabWidth": 2
}
```

### Использование

```bash
# Проверить форматирование
prettier --check .

# Отформатировать
prettier --write .

# Конкретный файл
prettier --write src/index.js
```

### Интеграция с ESLint

```bash
npm install --save-dev eslint-config-prettier
```

## 📝 Примеры проектов

### 1. Простой HTTP сервер

```javascript
// server.js
const http = require('http');

const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end('Hello World!');
});

server.listen(3000, () => {
  console.log('Server running at http://localhost:3000/');
});
```

### 2. Express.js API

```javascript
// app.js
const express = require('express');
const app = express();

app.use(express.json());

app.get('/api/users', (req, res) => {
  res.json([
    { id: 1, name: 'Alice' },
    { id: 2, name: 'Bob' }
  ]);
});

app.listen(3000, () => {
  console.log('API running on http://localhost:3000');
});
```

### 3. TypeScript CLI приложение

```typescript
// src/cli.ts
import { Command } from 'commander';

const program = new Command();

program
  .name('my-cli')
  .description('CLI tool example')
  .version('1.0.0');

program
  .command('greet <name>')
  .description('Greet someone')
  .action((name: string) => {
    console.log(`Hello, ${name}!`);
  });

program.parse();
```

## 🔗 Полезные команды

### package.json scripts

```json
{
  "scripts": {
    "start": "node index.js",
    "dev": "nodemon index.js",
    "build": "tsc",
    "lint": "eslint .",
    "format": "prettier --write .",
    "test": "jest"
  }
}
```

### Запуск скриптов

```bash
npm run dev
npm run build
npm run lint
npm run format
npm test
```

## 🆘 Решение проблем

### npm не находит пакеты

```bash
# Проверить конфигурацию
npm config list

# Сбросить к DevTools настройкам
npm config set prefix D:\DevTools\NodeJS\global_modules
npm config set cache D:\DevTools\Caches\npm
```

### Очистить кэш npm

```bash
npm cache clean --force
```

### Переустановить зависимости

```bash
rm -rf node_modules package-lock.json
npm install
```

## 📚 Ресурсы

- [Node.js Documentation](https://nodejs.org/docs/)
- [npm Documentation](https://docs.npmjs.com/)
- [TypeScript Documentation](https://www.typescriptlang.org/docs/)
- [Express.js Guide](https://expressjs.com/en/guide/routing.html)
- [PM2 Documentation](https://pm2.keymetrics.io/docs/)

---

**Node.js окружение готово к работе!** 🚀

**Быстрый старт:**
1. `.\Scripts\node-env.ps1` - активировать окружение
2. `.\Scripts\create-node-project.ps1 my-app` - создать проект
3. Начинайте разработку!
