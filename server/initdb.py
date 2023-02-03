from app import create_app
from models import db
from flask import Flask, render_template
from models import Composer

app = create_app()

with app.app_context():
    db.create_all()
    # @app.route('/')
    # def index():
    #     return render_template('index.html', data=Composer.query.all())
    

