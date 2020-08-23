# 建立資料表欄位
from main import db

class Todo(db.Model):
    # __table__name = 'user_table'，若不寫則看 class name
    # 設定 primary_key
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(80))

    def __init__(self, content):
        self.content = content

    def __repr__(self):
        return '<Todo %r>' % self.content

class ptt_articles (db.Model):
    __tablename__ = 'ptt_articles'
    Id = db.Column (db.Integer , primary_key = True)
    board_name = db.Column (db.String (20))
    url = db.Column (db.String (80))
    article_date = db.Column (db.DateTime)
    push_count = db.Column (db.Integer)
    push_num = db.Column (db.Integer)
    title = db.Column (db.String (70))
    search_item = db.Column (db.String (20))
    update_time = db.Column (db.DateTime)
   
    def __init__ (self , Id , board_name , url , article_date , push_count , push_num , title , search_item , update_time):
        self.Id = Id
        self.board_name = board_name
        self.url = url
        self.push_count = push_count
        self.push_num = push_num
        self.title = title 
        self.search_item = search_item
        self.article_date = article_date 
        self.update_time = update_time
