from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import os
import datetime


app = Flask(__name__ , template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = ''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


class users(db.Model):
    __tablename__ = 'users'
    Id = db.Column(db.Integer,primary_key = True)
    Uuid = db.Column(db.String(64), unique=True)
    Userid = db.Column(db.String(64))
    Display_name = db.Column(db.String(64))
    Church = db.Column(db.String(128))
    State = db.Column(db.Integer)
    IsFoodBank = db.Column(db.Integer)
    FoodIndex = db.Column(db.Integer)
    Region = db.Column (db.String (64))
    Time = db.Column (db.DateTime ())

    def __init__(self , Id , Uuid , Userid , Display_name , Church , State , IsFoodBank , FoodIndex , Region , Time):
        self.Id = Id
        self.Uuid = Uuid
        self.Userid = Userid
        self.Display_name = Display_name
        self.Church = Church
        self.State = State
        self.IsFoodBank = IsFoodBank 
        self.FoodIndex = FoodIndex 
        self.Region = Region 
        self.Time = Time 

    def __repr__(self):
        return '<users %r>' % (self.Userid)

class letter_list(db.Model):
    __tablename__ = 'letter_list'
    index = db.Column(db.Integer, primary_key=True)
    church = db.Column(db.String(40))
    case_num = db.Column(db.Integer)
    name = db.Column(db.String(40))
    sw = db.Column(db.String(40))
    persons = db.Column(db.String(40))
    title = db.Column(db.String(10))
    event = db.Column(db.String(40))
    notice = db.Column(db.Date())
    due = db.Column(db.Date())
    event_detail = db.Column(db.String(50))
    email_type = db.Column(db.String(10))

    def __init__(self , index , church , case_num , name, sw , persons , title , event , notice , due , event_detail , email_type  ):
        self.index = index
        self.church = church
        self.case_num = case_num
        self.name = name
        self.sw = sw
        self.persons = persons
        self.title = title
        self.event = event
        self.notice = notice
        self.due = due
        self.event_detail = event_detail
        self.email_type = email_type

class food (db.Model):
    __tablename__ = 'food'
    index = db.Column (db.Integer , primary_key = True)
    item = db.Column (db.String (80))
    total = db.Column (db.Integer)
    unit = db.Column (db.String (10))
    Max = db.Column (db.Integer)

    def __init__(self , index , item , total , unit , Max):
        self.index = index 
        self.item = item 
        self.total = total
        self.unit = unit 
        self.Max = Max 

class food_num (db.Model):
    __tablename__ = 'food_num'
    index = db.Column (db.Integer , primary_key = True)
    num = db.Column (db.Integer)

    def __init__(self , index , num):
        self.index = index 
        self.num = num 

class food_registrate (db.Model):
    __tablename__ = 'food_registrate'
    index = db.Column (db.Integer , primary_key = True)
    time = db.Column (db.DateTime ())
    userid = db.Column (db.String (64))
    item = db.Column (db.String (80))
    num = db.Column (db.Integer)
    IsFinished = db.Column (db.Integer)

    def __init__(self , index , time , userid , item , num , IsFinished):
        self.index = index 
        self.time = time 
        self.userid = userid 
        self.item = item
        self.num = num 
        self.IsFinished = IsFinished 

class fixed_item (db.Model):
    __tablename__ = 'fixed_item'
    Id = db.Column (db.Integer , primary_key = True)
    update_user_id = db.Column (db.String (64))
    fixed_user_id = db.Column (db.String (64))
    update_time = db.Column (db.DateTime ())
    Display_name = db.Column (db.String (20))
    church_name = db.Column (db.String (40))
    
    def __init__ (self , Id , update_user_id , fixed_user_id , update_time , Display_name , church_name):
        self.Id = Id
        self.update_user_id = update_user_id
        self.fixed_user_id = fixed_user_id 
        self.update_time = update_time 
        self.Display_name = Display_name
        self.church_name = church_name 
    
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    manager.run()
