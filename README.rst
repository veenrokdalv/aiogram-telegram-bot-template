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

* `poetry <https://python-poetry.org/>`_
* `aiogram <https://github.com/aiogram/aiogram>`_
* `python-environ <https://github.com/pjialin/django-environ>`_

============
Переменные окружения
============

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
