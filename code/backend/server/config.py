import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """Class for config for user database"""
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,
                                                          'user_credential.db')
    # flask-login uses sessions which require a secret Key
    SQLALCHEMY_TRACK_MODIFICATIONS = True
