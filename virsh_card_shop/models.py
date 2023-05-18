from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash
from flask_login import UserMixin, LoginManager
from flask_marshmallow import Marshmallow
import uuid, secrets

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    token = db.Column(db.String, default='', unique=True)
    join_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, username, email, password):
        self.id = self.set_id()
        self.username = username
        self.email = email
        self.password = self.set_password(password)
        self.token = self.set_token(32)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        return generate_password_hash(password)

    def set_token(self, length):
        return secrets.token_hex(length)

    def __repr__(self):
        return f'username: {self.username}, email: {self.email} added to Users'

class PullSheet(db.Model):
    id = db.Column(db.String, primary_key=True)
    product_name = db.Column(db.String)
    condition = db.Column(db.String)
    card_number = db.Column(db.String)
    card_set = db.Column(db.String)
    rarity = db.Column(db.String)
    quantity = db.Column(db.Integer)
    file_name = db.Column(db.String)

    def __init__(self, product_name, condition, card_number, card_set, rarity, quantity, file_name):
        self.id = self.set_id()
        self.product_name = product_name
        self.condition = condition
        self.card_number = card_number
        self.card_set = card_set
        self.rarity = rarity
        self.quantity = quantity
        self.file_name = file_name

    def set_id(self):
        return str(uuid.uuid4())

    def __repr__(self):
        return f'{self.product_name} was read and added from {self.file_name}'

class PullSheetSchema(ma.Schema):
    class Meta:
        fields = ['id', 'product_name', 'condition', 'card_number',
                  'card_set', 'rarity', 'quantity', 'file_name']

pullsheet_schema = PullSheetSchema()
pullsheets_schema = PullSheetSchema(many=True)