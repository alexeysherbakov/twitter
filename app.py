from flask import Flask, render_template, request, redirect, url_for, make_response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder='static')
app.secret_key = 'hellosarpens'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Userlogpass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    #Для пользователей

class Postmodel(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_title = db.Column(db.String(100), unique=False)
    currauthor = db.Column(db.String(100))
    post_include = db.Column(db.String(100))
    def __repr__(self):
        return '<Post by {}>'.format(self.currauthor)
    #Для постов


with app.app_context():
    db.create_all()


@app.route("/")
def index():
        postmodel_list = db.session.query(Postmodel).all()
        return render_template('index.html', postmodel_list=postmodel_list)
    #Главная страница


@app.route("/regs")
def regs():
    return render_template('reg.html')
    #Страница регистрации


@app.route("/login")
def log():
    return render_template('login.html')
    #Cтраница авторизации

@app.route("/cookiedelete")
def cookiedelete():
    return render_template('cookie_delete.html')
    #Удаление cookie

@app.post("/regs")
def reg():
    iusr = request.form.get("iusr")
    ipass = request.form.get("ipass")
    if iusr and ipass in db.session.query(Userlogpass):
        return '<center><h5>account already exists, please log in</h5></center>' + render_template('login.html')
    else:
        login = Userlogpass(username=iusr, password=ipass)
        db.session.add(login)
        db.session.commit()
        return redirect( url_for('login') )
    #Функционал регистрации

@app.route("/login", methods = ['POST', 'GET']) 
def login():
    usr = {"username": request.form.get("iusrku"), "password":request.form.get("ipassku")}
    exists = db.session.query(Userlogpass).filter_by(username=usr["username"], password=usr["password"]).first()
    if exists != None:
        resp = make_response(redirect( url_for('index') ))
        resp.set_cookie('dataxd', usr['username'], max_age=300000)
        return resp
    else :
        return '<center><h5>account not found, sign up instead</h5></center>' + render_template('reg.html')
    #Функционал авторизации + чек по ДБ

@app.route('/', methods=['GET', 'POST'])
def removecookie():
    res = make_response(redirect( url_for('cookiedelete') ))
    res.set_cookie('dataxd', max_age=0)
    return res
    #Удаление cookie

#Функционал постов

@app.post("/new-post")
def new_post():
    ip_author = request.cookies.get('dataxd')
    ip_title = request.form.get("title_input_form")
    ip_form = request.form.get("post_input_form")
    final_post = Postmodel(currauthor=ip_author, post_title=ip_title, post_include=ip_form)
    db.session.add(final_post)
    db.session.commit()
    return redirect( url_for('index') )
    #Создание поста + занесение его в датабазу

@app.route('/<currauthor>/<int:postmodel_id>/')
def posts(currauthor, postmodel_id):
    currauthors = db.session.query(Postmodel).filter_by(currauthor = currauthor, id = postmodel_id).first()
    if request.cookies.get('dataxd') is None:
        return '<center><h5>Seems like no cookie for me...</h5></center>'
    else:       
        try: 
            currauthors.currauthor == currauthor and request.cookies.get('dataxd')
            return f"<center><h2>Title: {currauthors.post_title} | Post: {currauthors.post_include}</h2></center>" + render_template('posts.html')
        except:
            return "<center><h2>Sorry! Try different author or id. Maybe, you have no cookie...</h2></center>" + render_template('posts.html')
        #Получение ссылок по имени автора + номеру поста

if __name__ == '__main__':
    app.run()