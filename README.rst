=============================
Aiogram telegram bot template
=============================

=======
Обо мне
=======

Шаблон для написания телеграмм ботов с помощью aiogram 3.x.



===========
Зависимости
===========

* `python 3.10.x <https://www.python.org/downloads/release/python-3108/>`_
* `poetry <https://python-poetry.org/>`_
* `aiogram <https://github.com/aiogram/aiogram>`_
* `python-environ <https://github.com/pjialin/django-environ>`_
* `cachetools <https://github.com/tkem/cachetools>`_
* `pytimeparse <https://github.com/wroberts/pytimeparse>`_


=========
Троттлинг
=========

Настройка
---------
В config.settings.THROTTLES определите ключ с значением (кол-во сообщений)/(время)

Например 5/1s 5 сообщений в секунду

Например 1/1min 1 сообщение в минуту

После чего оберните handler в декоратор rate_limit и укажите ключ, определенный в config.settings.THROTTLES

В bot.middlewares.MessageThrottlingMiddleware._process_message_throttling
вы можете определить поведение бота на флуд, например замутить пользователя в чате.

При исчерпании лимитов update не дойдет до handlers, а "прибьется на уровне middleware"

Использование
-------------
Оберните свой хендлер в декоратор rate_limit

====================
Переменные окружения
====================

TELEGRAM_BOT_TOKENS
-------------------

Токены бота Telegram, разделенные запятыми

Примеры:

- TELEGRAM_BOT_TOKENS=1:qwerty

- TELEGRAM_BOT_TOKENS=1:qwerty,2:qwerty

=============
Использование
=============

Установка
---------

Создайте файл .env и заполните его по примеру из файла .env.example. Так же вы можете просто пробросить эти переменные через переменные окружения.

.. code:: shell

    poetry install && poetry shell

.. code:: python

    python main.py


Разворачивание при помощи Docker
--------------------------------

Создайте файл .env и заполните его по примеру из файла .env.example. Так же вы можете просто пробросить эти переменные через переменные окружения.

.. code:: shell

    docker build -t telegram-bot .

.. code:: shell

    docker run telegram-bot

===
FAQ
===

* `Как установить poetry? <https://python-poetry.org/docs/>`_
* `Как установить docker? <https://docs.docker.com/desktop/install/windows-install/>`_
