> A user authentication system built with flask and python

# Setup
```bash
$ git clone https://github.com/Murtaza-Udaipurwala/authentication.py
$ cd authentication.py
$ pip install -r requirements.txt

# initialise database
$ python
>>> from auth_app import db
>>> from auth_app.user.models import User
>>> db.create_all()
```
open `auth_app/__init__.py` and add the email info(the one that sends the registered user the link to reset his/her password and make sure to allow less secured app is enabled incase of gmail)

# run
```bash
python run.py
```

# Features
* Registration
* login
* logout
* password recovery by sending an email to the registered user
* Allow user to change email, password and profile picture
* Passwords are stored encrypted in the database(sqlite3)

#### This webApp was built after watching [Corey Scafer's flask series on youtube](https://www.youtube.com/watch?v=MwZwr5Tvyxo&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH). A huge thanks to him for putting out quality tutorials on youtube❤️.
