# Django

this project is implemented on django

## Installation
1 Сreate a folder and clone this project

```bash
$ makedir carpatianknights
$ cd carpatianknights
$ git clone "https://github.com/KorenivskyOlexandr/carpatianknights.git"
```
2 You mast create virtualenv in project folder and activate one

```bash
$ python3 -m venv my_venv
$ source my_venv/bin/activate
(my_venv) $
```

3 Installation python packages 

```bash
(my_venv) $ pip install -r requirements.txt
```

4 Create database and superuser

```bash
(my_venv) $ python manage.py makemigrations
(my_venv) $ python manage.py migrate
(my_venv) $ python manage.py createsuperuser
```

## Usage

Server start

```bash
(my_venv) $ python manage.py runserver
```

You may stop your server use CTRL + C

Exit from my_venv
```bash
(my_venv) $ deactive
$
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
