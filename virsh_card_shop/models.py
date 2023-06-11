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

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fireToken = db.Column(db.String)
    csv_name = db.Column(db.String)
    TCGplayer_Id = db.Column(db.String(50))
    Product_Line = db.Column(db.String(150))
    Set_Name = db.Column(db.String(150))
    Product_Name = db.Column(db.String(150))
    Title = db.Column(db.String(150))
    Number = db.Column(db.String(50))
    Rarity = db.Column(db.String(50))
    Condition = db.Column(db.String(50))
    TCG_Market_Price = db.Column(db.Float)
    TCG_Direct_Low = db.Column(db.String(50))
    TCG_Low_Price_With_Shipping = db.Column(db.Float)
    TCG_Low_Price = db.Column(db.Float)
    Total_Quantity = db.Column(db.Integer)
    Add_to_Quantity = db.Column(db.Integer)
    TCG_Marketplace_Price = db.Column(db.Float)
    Photo_URL = db.Column(db.String(500))

    def __init__(self, fireToken, csv_name, TCGplayer_Id, Product_Line, Set_Name, Product_Name, Title, Number, Rarity, Condition, TCG_Market_Price, TCG_Direct_Low, TCG_Low_Price_With_Shipping, TCG_Low_Price, Total_Quantity, Add_to_Quantity, TCG_Marketplace_Price, Photo_URL):
        self.fireToken = fireToken
        self.csv_name = csv_name
        self.TCGplayer_Id = TCGplayer_Id
        self.Product_Line = Product_Line
        self.Set_Name = Set_Name
        self.Product_Name = Product_Name
        self.Title = Title
        self.Number = Number
        self.Rarity = Rarity
        self.Condition = Condition
        self.TCG_Market_Price = TCG_Market_Price
        self.TCG_Direct_Low = TCG_Direct_Low
        self.TCG_Low_Price_With_Shipping = TCG_Low_Price_With_Shipping
        self.TCG_Low_Price = TCG_Low_Price
        self.Total_Quantity = Total_Quantity
        self.Add_to_Quantity = Add_to_Quantity
        self.TCG_Marketplace_Price = TCG_Marketplace_Price
        self.Photo_URL = Photo_URL

    def __repr__(self):
        return f'Item: {self.Product_Name}, Quantity: {self.Total_Quantity}, Price: {self.TCG_Market_Price} from csv: {self.csv_name}'