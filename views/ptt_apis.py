from flask import Blueprint, request, current_app, redirect, url_for, render_template
from libs.ptt_bs4 import main as ptt_main
from datetime import datetime
from models import ptt_articles, Ptt_board_names
from sqlalchemy import func, or_
from main import db
import arrow

bp = Blueprint("ptt_api", __name__)

@bp.route("/", methods=["GET"])
def index():
    print(1)
    return "Hello ptt api"

@bp.route("/ptt", methods=['GET'])
def ptt():
    ############ read args ##########################
    board_name = request.args.get('board_name', 'Gossiping')
    push_num = request.args.get('push_num', "1")
    search_title = request.args.get('search_title', "")
    print("u r in /ptt, and board_name:{},push_num:{},search_item:{}".format(board_name, push_num, search_title))

    status = 0
    now = datetime.now()
    ############ find data if exists ################
    if push_num == "" and search_title == "":
        status = 1
        used = ptt_articles.query.filter(ptt_articles.board_name == board_name).first()
    elif push_num == "":
        status = 2
        used = ptt_articles.query.filter(ptt_articles.board_name == board_name, func.lower(ptt_articles.search_item) == func.lower(search_title)).first()
    elif search_title == "":
        status = 3
        used = ptt_articles.query.filter(ptt_articles.board_name == board_name, ptt_articles.push_num == push_num).first()
    else:
        status = 4
        used = ptt_articles.query.filter(ptt_articles.board_name == board_name, ptt_articles.push_num == push_num ,
                func.lower(ptt_articles.search_item) == func.lower(search_title)).first()
    if used:
        if(now - used.update_time).total_seconds() > 14400:
            if status == 1:
                ptt_articles.query.filter(ptt_articles.board_name == board_name).delete()
            elif status == 2:
                ptt_articles.query.filter(ptt_articles.board_name == board_name, func.lower(ptt_articles.search_item) == func.lower(search_title)).delete()
            elif status == 3:
                ptt_articles.query.filter(ptt_articles.board_name == board_name, ptt_articles.push_num == push_num).delete()
            elif status == 4:
                ptt_articles.query.filter(ptt_articles.board_name == board_name, ptt_articles.push_num == push_num ,
                                            func.lower(ptt_articles.search_item) == func.lower(search_title)).delete()
            db.session.commit()
        else:
            print("query has been activated in 4 hour")
            return redirect(url_for('ptt_api.ptt_data', board_name = board_name, push_num = push_num, search_title = search_title))

    ############ call crawler func #################
    print("board_name: {}, push_num: {}, search_title: {}".format(board_name, push_num, search_title))
    JSON = ptt_main(board_name, push_num, search_title)
#    print(JSON)

    ############ insert data ########################
    data = []
    new = db.session.query(func.max(ptt_articles.Id).label('max_id')).first()
    if new.max_id is not None: 
        Id = new.max_id + 1
    else:   
        Id = 1
    now = datetime.now()
    for i, item in enumerate(JSON):
        item["date"] = arrow.now().datetime
        data.append(ptt_articles(
            Id = Id+i ,
            board_name=board_name, 
            url = item['url'], 
            article_date = item['date'], 
            push_count = item['push_count'] , 
            push_num = item['push_num'] , 
            title = item ['title'], 
            search_item = item ['search'], 
            update_time = now))
    db.session.add_all(data)
    db.session.commit()
#    return jsonify(JSON)
    return redirect(url_for('ptt_api.ptt_data', board_name = board_name, push_num = push_num, search_title = search_title))

@bp.route("/ptt_data")
def ptt_data():
    board_name = request.args.get('board_name')
    push_num = request.args.get('push_num')
    search_title = request.args.get('search_title')
    print("u r in /ptt_data, and board_name:{},push_num:{},search_item:{}".format(board_name, push_num, search_title))

    if push_num == "" and search_title == "":
        data = db.session.query(ptt_articles.title, ptt_articles.push_count ,
                                    ptt_articles.url, ptt_articles.article_date)\
                        .filter(ptt_articles.board_name == board_name).distinct().all()
#        data = ptt_articles.query.filter(ptt_articles.board_name == board_name).all()
    elif push_num == "":
        data = db.session.query(ptt_articles.title, ptt_articles.push_count ,
                                    ptt_articles.url, ptt_articles.article_date)\
                        .filter(ptt_articles.board_name == board_name, 
                                    func.lower(ptt_articles.search_item) == func.lower(search_title)).distinct().all()
    elif search_title == "":
        data = db.session.query(ptt_articles.title,
                    ptt_articles.push_count,
                    ptt_articles.url,
                    ptt_articles.article_date).filter(
                            ptt_articles.board_name==board_name,
                            ptt_articles.push_num==push_num).distinct().all()
    else:
        data = db.session.query(
            ptt_articles.title,
            ptt_articles.push_count,
            ptt_articles.url,
            ptt_articles.article_date).filter(
                ptt_articles.board_name == board_name,
                ptt_articles.push_num == push_num,
                func.lower(
                    ptt_articles.search_item) == func.lower(search_title)).distinct().all()
    
    print("len(data): {}".format(len(data)))
    row = []
    for i, item in enumerate(data):
        row.append(dict(Id=i+1,
            push_num=item.push_count,
            url=item.url,
            title=item.title,
            date=item.article_date))

    return render_template("ptt_data.html", html_records=row, board_name=board_name)

@bp.route("/select_ptt_data", methods=['GET', 'POST'])
def select_ptt_data():
    condition_query = []
    if request.method == 'POST':
        print(1)
        row = []
        print(request.form)
        for key, value in request.form.items():
            condition_query.append({key:value})
        print("condition_query:", condition_query)
        board_name = condition_query[0]['board_name']
        push_num = condition_query[1]['push_count']
        search_title = condition_query[2]['title']

        if push_num == "" and search_title == None:
            data = ptt_articles.query.filter(ptt_articles.board_name == board_name).all()
            one = ptt_articles.query.filter(ptt_articles.board_name == board_name).first()
            count = ptt_articles.query.filter(ptt_articles.board_name == board_name).count()
        elif push_num == "":
            data = ptt_articles.query.filter(ptt_articles.board_name == board_name, func.lower(ptt_articles.search_item) == func.lower(search_title)).all()
            one = ptt_articles.query.filter(ptt_articles.board_name == board_name, func.lower(ptt_articles.search_item) == func.lower(search_title)).first()
            count = ptt_articles.query.filter(ptt_articles.board_name == board_name, func.lower(ptt_articles.search_item) == func.lower(search_title)).count()
        elif search_title == None:
            data = ptt_articles.query.filter(ptt_articles.board_name == board_name, ptt_articles.push_num == push_num).all()
            one = ptt_articles.query.filter(ptt_articles.board_name == board_name, ptt_articles.push_num == push_num).first()
            count = ptt_articles.query.filter(ptt_articles.board_name == board_name, ptt_articles.push_num == push_num).count()
        else:
            data = ptt_articles.query.filter(ptt_articles.board_name == board_name, ptt_articles.push_num == push_num, func.lower(ptt_articles.search_item) == func.lower(search_title)).all()
            one = ptt_articles.query.filter(ptt_articles.board_name == board_name, ptt_articles.push_num == push_num, func.lower(ptt_articles.search_item) == func.lower(search_title)).first()
            count = ptt_articles.query.filter(ptt_articles.board_name == board_name, ptt_articles.push_num == push_num, func.lower(ptt_articles.search_item) == func.lower(search_title)).count()
        
        now = datetime.now()
        if count == 30 and(now - one.update_time).total_seconds() < 14400:
            for i, item in enumerate(data):
                row.append(dict(
                    Id=i+1, 
                    push_num=item.push_count,
                    url=item.url,
                    title=item.title,
                    date=item.article_date))
            return render_template("ptt_data.html", html_records=row, board_name = board_name)
        else:
            return redirect(url_for('ptt_api.ptt', board_name=board_name, push_num=push_num, search_title=search_title))
    else:
        board_names = Ptt_board_names.query.order_by(Ptt_board_names.Id).all() 
        return render_template("select_ptt_data.html", uniques=board_names)

