YaBackup
========

YaBackup is a simple Django app to backup your files and database to Yandex.Disk

Requirements
------------

```
Python >= 3
Django >= 1.11
YaDiskClient >= 0.4.5
```

Older versions might work too

Install
-------

```
pip install django-yabackup
```
or
> [easy_install](https://pypi.python.org/pypi/setuptools) [YaBackup](https://pypi.python.org/pypi/django-yabackup)


Quick start
-----------

1. Add "YaBackup" to your INSTALLED_APPS setting like this:
```
    INSTALLED_APPS = [
        ...
        'YaBackup',
    ]
```

2. Add YABACKUP_SETTINGS to your project settings:
```
    YABACKUP_SETTINGS = {
        'DATE_TIME_FORMAT': '%Y-%m-%d_%H-%M-%S',  # Will be added to your backup file name
        'YADISK_LOGIN': 'login',                  # Yandex.Disk login
        'YADISK_PASSWORD': 'password',            # Yandex.Disk password
        'YADISK_BACKUP_ROOT': '/BACKUPS/',        # path to your backups folder at Yandex.Disk MUST BE CREATED BEFORE RUNNING BACKUPS
    }
```

3. Run `python manage.py migrate` to create the YaBackup models.


Usage
-----

You can create and run your backups from the admin backend. Also, you can run them with management command:
```
python manage.py YaBackup
```

Cron
----

> You can use [Chroniker](https://github.com/chrisspen/django-chroniker)
or other apps to schedule your backups by running management command.



