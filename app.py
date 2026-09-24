from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, request, redirect, url_for
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trip.db'
db.init_app(app)

class Trip(db.Model):
    __tablename__ = 'trip_table'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    content = db.Column(db.String(300), nullable=False)
    latitude = db.Column(db.String(100), nullable=False)
    longitude = db.Column(db.String(100), nullable=False)
    create_date = db.Column(db.DateTime, nullable=False, default=datetime.now)

@app.cli.command("initialize_DB")
def initialize_DB():
    db.drop_all()
    db.create_all()
    print("Database initialized.")

@app.route('/')
def index():
    title = "Trip Log :一覧画面"
    all_data = db.session.execute(db.select(Trip)).scalars()
    return render_template('index.html', title=title, all_data=all_data)

@app.route('/create', methods=['GET','POST'])
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        trip = Trip(
            title=title,
            content=content,
            latitude=latitude,
            longitude=longitude
        )
        db.session.add(trip)
        db.session.commit()
        return redirect('/')
    return render_template('new.html')

@app.route('/detail')
def detail():
    title = "Trip Log :詳細画面"
    id = request.args.get('id')
    trip = db.get_or_404(Trip, id)
    return render_template('detail.html', title=title, trip=trip)

@app.route('/edit', methods=['GET'])
def edit():
    title = "Trip Log :編集画面"
    id = request.args.get('id')
    trip = db.get_or_404(Trip, id)
    return render_template('edit.html', title=title, trip=trip)

@app.route('/update', methods=['POST'])
def update():
    id = request.args.get('id')
    trip = db.get_or_404(Trip, id)
    trip.title = request.form.get('title')
    trip.content = request.form.get('content')
    trip.latitude = request.form.get('latitude')
    trip.longitude = request.form.get('longitude')
    db.session.merge(trip)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete', methods=['POST'])
def delete():
    if request.method =='POST':
        id = request.args.get('id')
        trip = db.get_or_404(Trip, id)
        db.session.delete(trip)
        db.session.commit()
    return redirect(url_for('index'))
                               
#Flaskサーバーの起動
if __name__ == '__main__':
    app.run(debug=True)
