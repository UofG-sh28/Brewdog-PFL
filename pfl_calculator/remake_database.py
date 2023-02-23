import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pfl_calculator.settings')
import django
django.setup()
from calculator_site.models import *
from django.contrib.auth.models import User

def create_super_user():
    user = User()
    user.is_active = True
    user.is_superuser = True
    user.is_staff = True
    user.username, user.email = "sh28", "sh28@admin.com"
    user.set_password("sh28")
    user.save()

def flush_database():
    if os.path.exists("db.sqlite3"):
        os.remove("db.sqlite3")
        print("Path exists: ", os.path.exists("db.sqlite3"))

def remake_database():
    print("Creating Migrations...")
    message = os.popen("python manage.py makemigrations")
    print(message.read())

    print("Migrating...")
    message = os.popen("python manage.py migrate")
    print(message.read())

def populate_pledges():
    msg = os.popen("python population_script.py")
    print(msg.read())

if __name__ == "__main__":
    print("Deleting old database...")
    flush_database()

    print("Remaking Database...")
    remake_database()

    print("Creating Admin Users...")
    create_super_user()

    print("Populating Models...")
    populate_pledges()

    print("Finished")
