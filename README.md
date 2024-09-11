# Setup
To setup, install these packages 

```bash
pip install SQLAlchemy flask-socketio simple-websocket
```

# Running the App
To run the app, 

```bash
python3 app.py
```


# Usage
To use the app, setup and run the app as per the instructions above. Also, if you're using VSCode, I recommend installing the Better Jinja extension (it's not perfect unfortunately, but it's enough). 

Now, it will show `Running on http://127.0.0.1:5000`, open that link in 2 different browsers (for instance Chrome and Firefox).

Click "Sign up", or "Log in" if you've already signed up. Put in your username and password.

Now, open your other browser and sign up/log in with a different username and password. 

In the first browser, type in the other username (the username inputted into the other browser) and click Chat. Do the same for the other browser.

Once both users have connected, you're good to go. Go ahead and start chatting to yourself :D

To chat with a different user, feel free to leave the room and chat with another user.

# A Warning
Since this app uses cookies, you can't open it in separate tabs to test multiple client communication. This is because cookies are shared across tabs. You'd have to use multiple browsers to test client communication.

# Credits (or I guess the "tech stack" used)
- Javascript
- Python

## Javascript Dependencies
- Socket.io
- Axios (for sending post requests, but a bit easier than using fetch())
- JQuery (if you're familiar with web frameworks this is like the stone age all over again)
- Cookies (small browser library that makes working with cookies just a bit easier)

## Python Dependencies
- Template Engine: Jinja
- Database ORM: SQL Alchemy (use SQLite instead if you are an SQL master)
- Flask Socket.io
