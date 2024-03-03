### Контекст

- Тестовый проект
- Результатом создания проекта будет бэкенд-сервер, который возвращает клиенту JSON-структуры
- Платформа для онлайн-обучения в которой каждый желающий может размещать свои полезные материалы или курсы


### Для запуска необходимо:

- Перейти в папку в которой будем работать

    - path_to_dir - ваша рабочая директория
  ``` PowerShell
  cd path_to_dir
  ```

- Склонировать репозиторий
  ``` PowerShell
  git clone https://github.com/Nudlik/mailer_service.git
  ```

- Cоздать виртуальное окружение
  ``` PowerShell
  - python -m venv venv
  ```

- Активировать виртуальное окружение
  ``` PowerShell
  .\venv\Scripts\activate
  ```

- Установить зависимости
  ``` PowerShell
  pip install -r requirements.txt
  ```

- Прописать в .env ваши настройки(пример файла .env.example):

- Приминить миграции
  ``` PowerShell
  python .\manage.py migrate
  ```

- Для создания веб хука, зайдите в панель администрирования страйпа и пропишите веб-хуки для эвента
`checkout.session.completed`, запишите секретный ключ в .env `STRIPE_SECRET_WEBHOOK` или запустите команду и следуйте
инструкциям
  ``` PowerShell
  python .\manage.py create_webhook
  ```

- Запустить `ngrok http 8000` и прописать в .env `SITE_HOST_NAME` Forwarding из консоли, пример 
`4dc9-94-199-68-90.ngrok-free.app`

- Запустить брокер redis, заходим в wsl
  ``` PowerShell
  sudo service redis-server start
  ```

- Запускаем worker в Celery
  ``` PowerShell
  celery -A config worker -l INFO -P eventlet
  ```
  
- Запускаем периодические задачи Celery beat
  ``` PowerShell
  celery -A config beat -l INFO -S django
  ```

- Запустить программу из консоли/среды разработки
  ``` PowerShell
  python .\manage.py runserver
  ```


### Полезные команды

- Запуск подсчета покрытия и вывод отчета

- Создание локальной бд с информацией о тестах
  ``` python
  coverage run --source='.' manage.py test
  ```

- Вывод покрытия в терминал
  ``` python
  coverage report
  ```

- Создать html файл для более детального просмотра 
  ``` python
  coverage html
  ```

- Создать фикстуру содержащую кирилицу с правильной кодировкой и отступами
  ``` python
  python -Xutf8 .\manage.py dumpdata --indent=4 -o utils/fixtures/data.json
  ```

- Генерация пайлинт конфига
  ``` python
  pylint --generate-rcfile | out-file -encoding utf8 .pylintrc
  ```

### Stripe ссылки

- 2