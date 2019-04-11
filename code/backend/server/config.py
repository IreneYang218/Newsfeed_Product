import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY=os.urandom(24)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'user_credential.db')
    # SQLALCHEMY_DATABASE_URI  = 'mysql://newsphi:msds603newsphi@{endpoint}/newsphi'
    SQLALCHEMY_TRACK_MODIFICATIONS = True # flask-login uses sessions which require a secret Key
