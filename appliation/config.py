import os
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    Server = os.getenv('SERVER')
    Driver = os.getenv('DRIVER')
    UserName = os.getenv('USER_NAME')
    Password = os.getenv('PASS_WORD')
    DataBase = os.getenv('DATA_BASE')
    DataBase_Connection_String = f'mssql://{UserName}:{Password}@{Server}/{DataBase}?driver={Driver}'
    SQLALCHEMY_DATABASE_URI = DataBase_Connection_String
    # app.config["RECAPTCHA_PUBLIC_KEY"] = "6LfBTtcZAAAAAHZQgfRt7YV1yvxqKDAB05SX9eEZ"
    # app.config["RECAPTCHA_PRIVATE_KEY"] = "6LfBTtcZAAAAAA-eEpHiXA4kjBaeD8ShQ4R2hyI8"
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    # MAIL_USE_SSl = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')