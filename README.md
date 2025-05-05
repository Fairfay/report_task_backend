## Тестовое задание для компании Аэродин

# Для запуска проекта локально

Заполнить .env по примеру .env.template

Запустить проект
```bash
docker-compose up --build
```
# Для запуска проекта в прод

Заполнить .env.prod по примеру .env.template

Запустить проект
```bash
docker-compose -f docker-compose.prod.yml up --build
```

Дополнительные команды можно посмотреть в Makefile
