from flask import Flask, request, jsonify, render_template, redirect
from mongoengine import (
    connect,
    Document,
    StringField,
    FloatField,
    IntField,
    DateTimeField,
    ListField
)
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# -------------------------------
# MongoDB Atlas Connection
# -------------------------------
connect(
    db="abhi",
    host="mongodb+srv://user:user@cluster0.rgocxdb.mongodb.net/"
)
from mongoengine import Document, StringField, FloatField, DateTimeField
from datetime import datetime

class Order(Document):
    order_id = StringField(required=True, unique=True)
    phone = StringField(required=True)
    item = StringField(required=True)
    total_amount = FloatField(required=True)
    status = StringField(default="Placed")
    created_at = DateTimeField(default=datetime.utcnow)

    
Order(
    order_id="ORD1001",
    phone="919999999999",
    item="Banarasi Silk Saree",
    total_amount=4500,
    status="Shipped"
).save()
