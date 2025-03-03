# Stripe Test Project

Этот проект демонстрирует интеграцию Stripe в Django для обработки платежей и вебхуков. Проект запускается с использованием Docker Compose.

---

## Требования

Перед началом работы убедитесь, что у вас установлены следующие инструменты:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Git](https://git-scm.com/)

---

## Установка и запуск

1. **Клонируйте репозиторий:**

   ```bash
   git clone https://github.com/Arteea/stripe_test.git
   cd stripe_test/test_pay
   ```

2. **Конфиги под пользователя Stripe CLI вшиты в репозиторий**

3. **Запустите проект с помощью Docker Compose:**

   ```bash
   docker-compose up --build
   ```

   После запуска:
   - Django-сервер будет доступен по адресу: [http://localhost:8000](http://localhost:8000).
   - Stripe CLI будет прослушивать события на порту `4242`.


## Использование

1. **Доступные маршруты:**

   - **Список товаров:** [http://localhost:8000/items_list/](http://localhost:8000/items_list/)
   - **Конкретный товар Стол:** [http://localhost:8000/item/1/](http://localhost:8000/item/1/)
   - **Конкретный товар Стул:** [http://localhost:8000/item/2/](http://localhost:8000/item/2/)
   - **Конкретный товар Кресло:** [http://localhost:8000/item/3/](http://localhost:8000/item/3/)
   - **Вебхуки:** [http://localhost:8000/webhook/](http://localhost:8000/webhook/)

2. **Тестирование платежей:**

   - Используйте тестовые данные карты Stripe для оплаты:
     - Номер карты: `4242 4242 4242 4242`
     - Срок действия: любая будущая дата
     - CVC: любой три цифры

---

## Логи

- Логи Django-сервера можно увидеть в терминале, где запущен `docker-compose`.
- Логи Stripe CLI также выводятся в терминал.

---

## Остановка проекта

Чтобы остановить проект, выполните:

```bash
docker-compose down
```

---

## Перезапуск проекта

Если вы внесли изменения в код и хотите перезапустить проект, используйте:

```bash
docker-compose up --build
```

---

## Лицензия

Этот проект распространяется под лицензией MIT. Подробнее см. в файле [LICENSE](LICENSE).

---

## Автор

- [Arteea](https://github.com/Arteea)

---

Если у вас возникли вопросы или проблемы, создайте [issue](https://github.com/Arteea/stripe_test/issues) в репозитории.
