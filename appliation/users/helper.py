import secrets
import os
from flask import url_for, current_app
from application import mail
from flask_mail import Message

def get_and_save_picture(image):
    file_name = secrets.token_hex(8)
    _, file_ext = os.path.splitext(image.filename)
    image_file_name = file_name + file_ext
    path = os.path.join(current_app.root_path+'/static/images/account/'+image_file_name)
    image.save(path)
    return image_file_name

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message("Password Request Message")
    msg.sender = os.getenv('MAIL_USERNAME')
    msg.recipients = [user.user_email]
    msg.body = f''' Click the following link to proceed further:
{url_for('users.reset_token', token=token, _external=True)}
if You did\'nt make the request. Ignore this message. '''
    mail.send(msg)

