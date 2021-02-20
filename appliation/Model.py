from application import db
from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
def Insert_Data(user_name, user_email, user_password, user_image):
    user = User(user_name=user_name, user_email=user_email, user_password=user_password, user_image=user_image)
    db.session.add(user)
    db.session.commit()
class User(db.Model,UserMixin):
    user_id = db.Column('user_id',db.Integer,primary_key=True,autoincrement=True)
    user_name = db.Column('user_name',db.String(50),nullable=False)
    user_email = db.Column('user_email',db.String(50),nullable=False,unique=True)
    user_password = db.Column('user_password',db.String(100),nullable=False)
    user_image = db.Column('user_image',db.String(100),nullable=False)
    def get_id(self):
        return int(self.user_id)

    def get_reset_token(self,expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'],expires_in=1800)
        return s.dumps({'user_id':self.user_id})
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)