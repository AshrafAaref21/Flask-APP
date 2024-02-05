from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_migrate import Migrate
from flask_login import LoginManager



app = Flask(__name__)
db = SQLAlchemy(app)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SECRET_KEY'] ='my_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ os.path.join(basedir,'database.sqlite')
app.config['SQLALCHEMY_TRACK_MODEFICATIONS'] = False

Migrate(app,db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'


from companyblog.core.views import core
from companyblog.error_pages.handlers import error_pages
from companyblog.users.views import users
from companyblog.blog_posts.views import blog_posts
app.register_blueprint(core)
app.register_blueprint(error_pages)
app.register_blueprint(users)
app.register_blueprint(blog_posts)