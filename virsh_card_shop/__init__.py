from flask import Flask
from config import Config
from .site.routes import site
from .authentication.routes import auth
from .hover_helpers import wrap_letters, wrap_words
from .models import db as root_db, login_manager, ma
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)

app.register_blueprint(site)
app.register_blueprint(auth)

app.config.from_object(Config)

app.jinja_env.filters['wrap_letters'] = wrap_letters
app.jinja_env.filters['wrap_words'] = wrap_words

root_db.init_app(app)
migrate = Migrate(app, root_db)

ma.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

CORS(app)