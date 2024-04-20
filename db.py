'''
db
database file, containing all the logic to interface with the sql database
'''

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import *

from pathlib import Path

# creates the database directory
Path("database") \
    .mkdir(exist_ok=True)

# "database/main.db" specifies the database file
# change it if you wish
# turn echo = True to display the sql output
engine = create_engine("sqlite:///database/main.db", echo=False)

# initializes the database
Base.metadata.create_all(engine)
# inserts a user to the database
def insert_user(username: str, password: str, salt: str, pubKey: str, friends: str = "", incoming: str = "", outgoing: str = ""):
    with Session(engine) as session:
        user = User(username=username, password=password, salt=salt, pubKey=pubKey, friends=friends, incoming=incoming, outgoing=outgoing)
        session.add(user)
        session.commit()

# gets a user from the database
def get_user(username: str):
    with Session(engine) as session:
        return session.get(User, username)

def get_friend_list(username: str):
    with Session(engine) as session:
        user = session.query(User).filter_by(username=username).first()
        friend_list = user.friends.split('?')
        return friend_list

def get_outgoing_requests(username: str):
    with Session(engine) as session:
        user = session.query(User).filter_by(username=username).first()
        outgoing_requests = user.outgoing.split('?') if user.outgoing else []
        return outgoing_requests

def get_incoming_requests(username: str):
    with Session(engine) as session:
        user = session.query(User).filter_by(username=username).first()
        incoming_requests = user.incoming.split('?') if user.incoming else []
        return incoming_requests

def add_friend(username: str, friend_username: str):
    with Session(engine) as session:
        user = session.query(User).filter_by(username=username).first()
        if friend_username not in user.friends.split('?'):
            user.friends = (user.friends + '?' + friend_username) if user.friends else friend_username
        session.commit()

def remove_friend_request(username: str, friend_username: str):
    with Session(engine) as session:
        user = session.query(User).filter_by(username=username).first()
        friend_user = session.query(User).filter_by(username=friend_username).first()
        if friend_username in user.incoming.split('?'):
            updated_requests = '?'.join(fr for fr in user.incoming.split('?') if fr != friend_username)
            user.incoming = updated_requests if updated_requests else ''
            updated_requests = '?'.join(fr for fr in friend_user.outgoing.split('?') if fr != username)
            friend_user.outgoing = updated_requests if updated_requests else ''
        session.commit()

def approve_friend_request(username: str, friend_username: str):
    with Session(engine) as session:
        user = session.query(User).filter_by(username=username).first()
        friend_user = session.query(User).filter_by(username=friend_username).first()

        if not user or not friend_user:
            return {'error': 'One or both users not found'}

        if friend_username in (user.incoming or '').split('?'):
            updated_requests = '?'.join(fr for fr in user.incoming.split('?') if fr != friend_username)
            user.incoming = updated_requests if updated_requests else ''
            user.friends = user.friends + '?' + friend_username if user.friends else friend_username
        else:
            return {'error': 'No incoming friend request from ' + friend_username}

        if username in (friend_user.outgoing or '').split('?'):
            updated_requests = '?'.join(fr for fr in friend_user.outgoing.split('?') if fr != username)
            friend_user.outgoing = updated_requests if updated_requests else ''
            friend_user.friends = friend_user.friends + '?' + username if friend_user.friends else username
        else:
            return {'error': 'No outgoing friend request to ' + friend_username}

        session.commit()
        return {'username': username, 'friend_username': friend_username}
        

def send_friend_request(username: str, friend_username: str):
    if username == friend_username:
        return
    with Session(engine) as session:
        user = session.query(User).filter_by(username=friend_username).first()
        requesting_user = session.query(User).filter_by(username=username).first()
        if user is not None:
            if requesting_user.friends and friend_username in requesting_user.friends.split('?'):
                print(f"{friend_username} is already your friend.")
                return
            if user.incoming and username not in user.incoming.split('?'):
                user.incoming += '?' + username
            elif not user.incoming:
                user.incoming = username
            if requesting_user.outgoing and friend_username not in requesting_user.outgoing.split('?'):
                requesting_user.outgoing += '?' + friend_username
            elif not requesting_user.outgoing:
                requesting_user.outgoing = friend_username
            session.commit()
        else:
            print(f"No user found with username {friend_username}")

def add_chatroom(username: str, friend_username: str):
    with Session(engine) as session:
        current_chatroom = chat_history(userA=username, userB=friend_username)
        session.add(current_chatroom)
        session.commit()


#Get history room of two participants
def get_history(userA, userB):
    with Session(engine) as session:
        history = session.query(chat_history).filter(chat_history.userA == userA, chat_history.userB == userB).first()
        if history == None:
            history = session.query(chat_history).filter(chat_history.userA == userB, chat_history.userB == userA).first()
        return history
    
def get_pubKey(username):
    with Session(engine) as session:
        user = session.query(User).filter_by(username=username).first()
        return user.pubKey


    
def update_history(userA, userB, message):
    with Session(engine) as session:
        print("ENCRYPTED MSG   : " + message)
        delim = "ⴰ𐄂Ⱞ𐎀"
        history = session.query(chat_history).filter(chat_history.userA == userA, chat_history.userB == userB).first()
        identifier = "a"
        if history == None:
            history = session.query(chat_history).filter(chat_history.userA == userB, chat_history.userB == userA).first()
            identifier = "b"

        if history:
            if not history.History:
                history.History = message + identifier
            else:
                history.History += delim + message + identifier
            session.commit()
