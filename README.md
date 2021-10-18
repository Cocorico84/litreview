![forthebadge](https://forthebadge.com/images/badges/cc-0.svg)
![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)
![forthebadge](https://forthebadge.com/images/badges/uses-html.svg)

# Description

LitReview is a platform to create reviews on books and ask reviews if you want some reviews on a specific book.

Additionally, you can create a community by following other people and be followed.

# Prerequisites

Python 3

# Installation

To clone the repository, you can download the zip or clone either HTTPS or SSH. And when you are in the repository you can activate your virtual environement.

On Linux or Mac
```console
pip install virtualenv
virtualenv venv --python=python3
source venv/bin/activate
pip install -r requirements.txt
```

On Windows
```console
c:\Python38\python -m venv c:\path\to\myenv
C:\\{venv}\\Scripts\\activate.bat
pip install -r requirements.txt
```

# Quickstart

To create a superuser:
```console
python manage.py createsuperuser
```
This will allow you to connect to the admin panel.

To see the website in local, run this command :

```console
python manage.py runserver
```
When you launch this command, it will start the website on http://127.0.0.1:8000.
You can create a user or you can login if you have already created one.

You can also create users from shell:
```py
python manage.py shell
from django.contrib.auth.models import User
User.objects.create_user('foo', password='bar')
```
If you want to give some permissions:
```py
python manage.py shell
from django.contrib.auth.models import User
user = User.objects.create_user('foo', password='bar')
user.is_superuser=True
user.is_staff=True
user.save()
```

# Contributor

If you have any suggestions to improve the project, you can create an issue.
