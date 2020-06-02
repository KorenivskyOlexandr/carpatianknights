# Django

this project is implemented on django

## Installation
1 Сreate a folder and clone this project

```bash
makedir carpatianknights
cd carpatianknights
git clone "https://github.com/KorenivskyOlexandr/carpatianknights.git"
```
2 You should create virtualenv in project folder and activate one

```bash
python3 -m venv venv
source venv/bin/activate
(venv) $
```
Further we work only with venv

3 Installation python packages

```bash
pip install -r requirements.txt
```

4 Create database and superuser

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

## Usage

Server start

```bash
python manage.py runserver
```

You may stop your server use CTRL + C

Exit from venv
```bash
(venv) $ deactive
$
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
