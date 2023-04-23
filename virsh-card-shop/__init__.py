from flask import Flask
from config import Config
from .site.routes import site

app = Flask(__name__)
    
app.register_blueprint(site)

app.config.from_object(Config)

def wrap_letters(text, class_name):
    return "".join(f'<span class="{class_name}" data-letter="{letter}">{letter}</span>' for letter in text)
app.jinja_env.filters['wrap_letters'] = wrap_letters