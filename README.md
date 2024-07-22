[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
<div align="center">
    <h1>QRKot</h1> 
    <p>
    Это благотворительный фонд, направленный на сбор и распределение пожертвований на цели, связанные с поддержкой хвостатых.
    </p>
</div>

---

## Описание

Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.

## Проекты

В Фонде QRKot может быть открыто несколько целевых проектов. У каждого проекта есть название, описание и сумма, которую планируется собрать. После того, как нужная сумма собрана — проект закрывается.
Пожертвования в проекты поступают по принципу First In, First Out: все пожертвования идут в проект, открытый раньше других; когда этот проект набирает необходимую сумму и закрывается — пожертвования начинают поступать в следующий проект.

## Пожертвования

Каждый пользователь может сделать пожертвование и сопроводить его комментарием. Пожертвования не целевые: они вносятся в фонд, а не в конкретный проект. Каждое полученное пожертвование автоматически добавляется в первый открытый проект, который ещё не набрал нужную сумму. Если пожертвование больше нужной суммы или же в Фонде нет открытых проектов — оставшиеся деньги ждут открытия следующего проекта. При создании нового проекта все неинвестированные пожертвования автоматически вкладываются в новый проект.

## Пользователи

Целевые проекты создаются администраторами сайта. 
Любой пользователь может видеть список всех проектов, включая требуемые и уже внесенные суммы. Это касается всех проектов — и открытых, и закрытых.
Зарегистрированные пользователи могут отправлять пожертвования и просматривать список своих пожертвований.

---

<div align="center">
    <h3 align="center">
        <p>Использовались языки и инструменты:</p>
        <div>
            <img src="https://github.com/devicons/devicon/blob/master/icons/python/python-original-wordmark.svg" title="Python" alt="Python" width="40" height="40"/>&nbsp;
            <img src="https://github.com/devicons/devicon/blob/master/icons/pytest/pytest-original-wordmark.svg" title="pytest" alt="pytest" width="40" height="40"/>&nbsp;
            <img src="https://github.com/devicons/devicon/blob/master/icons/fastapi/fastapi-original-wordmark.svg" title="FastApi" alt="FastApi" width="40" height="40"/>&nbsp;
            <img src="https://github.com/devicons/devicon/blob/master/icons/postman/postman-original-wordmark.svg" title="postman" alt="postman" width="40" height="40"/>&nbsp;
            <img src="https://github.com/devicons/devicon/blob/master/icons/sqlalchemy/sqlalchemy-original-wordmark.svg" title="SQLAlchemy" alt="SQLAlchemy" width="40" height="40"/>&nbsp;
            <img src="https://github.com/devicons/devicon/blob/master/icons/vscode/vscode-original-wordmark.svg" title="VSCode" alt="VSCode" width="40" height="40"/>&nbsp;
        </div>
    </h3>
</div>

---

## Локальная установка проекта

1. Склонируйте репозиторий:
```bash
git clone https://github.com/Iv-EN/support_an_animal.git
```
2.  Создайте и активируйте виртуальное пространство:
```bash
python3 -m venv venv
```
```bash
sourse venv/bin/activate
```
3. Обновите pip и установите зависимости:
```bash
python3 -m pip install --upgrade pip
```
```bash
pip install -r requirements.txt
```
4. В корне проекта создайте файл `.env` 
```bash
touch .env
```
5. Опишите в нём переменные окружения:
```bash
DATABASE_URL=<настройки подключения к БД, например: sqlite+aiosqlite:///./development.db>
SECRET=<секретный ключ>
FIRST_SUPERUSER_EMAIL=<email первого суперпользователя>
FIRST_SUPERUSER_PASSWORD=<пароль первого суперпользователя>
```

## Запуск проекта
1. Для создания БД примените миграции:
```bash
alembic upgrade head
```
2. Для запуска проекта выполните команду:
```bash
uvicorn app.main:app --reload
```
_Если в файле `.env` были определены переменные
`FIRST_SUPERUSER_EMAIL` и `FIRST_SUPERUSER_PASSWORD`, 
то при первом запуске приложения в базе данных будет создан суперпользователь.
Эти данные можно использовать для авторизации._
___

## Документация API
Документация по проекту:
 - `/docs` — документация в формате Swagger;
 - `/redoc` — документация в формате ReDoc.
___

<h3 align="center">
    <p><img src="https://media.giphy.com/media/iY8CRBdQXODJSCERIr/giphy.gif" width="30" height="30" style="margin-right: 10px;">Автор: Евгений Иванов. </p>
</h3>
<p align="center">

 <div align="center"  class="icons-social" style="margin-left: 10px;">
        <a href="https://vk.com/engenivanov" target="blank" rel="noopener noreferrer">
      <img src="https://img.shields.io/badge/%D0%92%20%D0%BA%D0%BE%D0%BD%D1%82%D0%B0%D0%BA%D1%82%D0%B5-blue?style=for-the-badge&logo=VK&logoColor=white" alt="В контакте Badge"/>
    </a>
    <a href="https://t.me/IvENauto" target="blank" rel="noopener noreferrer">
    <img src="https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white"/>
    </a>
  </div>
</p>
