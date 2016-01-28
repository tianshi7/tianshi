#!/usr/bin/env python
# encoding: utf-8

from flask import Flask, request, render_template,session,redirect,url_for,flash
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from datetime import datetime
from flask.ext.wtf import Form
from wtforms import StringField,SubmitField
from wtforms.validators import Required
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Shell
from flask.ext.mail import Mail,Message
import os
from threading import Thread
basedir = os.path.abspath(os.path.dirname(__file__))


def make_shell_context():
    return dict(app=app,db=db,User=User,Role=Role)


class NameForm(Form):
    name = StringField('what is your name?',validators=[Required()])
    submit = SubmitField('Submit')

app = Flask(__name__)
app.config['SECRET_KEY']='hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI']=\
        'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']= True

app.config['MAIL_SERVER'] = 'smtp.qq.com'
#app.config['MAIL_PORT'] = 25
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = '89032902@qq.com'
app.config['MAIL_PASSWORD'] = 'tianhe930618'
app.config['TIANHE_SUBJECT_PREFIX']='[tianheaishibin]'
app.config['TIANHE_MAIL_SENDER'] = 'ittianhe <89032902@qq.com>'
app.config['TIANHE_ADMIN'] = '89032902@qq.com'


bootstrap = Bootstrap(app)

moment = Moment(app)
manager = Manager((app))
manager.add_command("shell",Shell(make_context=make_shell_context))
db = SQLAlchemy(app)
mail = Mail(app)
def send_email(to,subject,template,**kwargs):

        msg = Message(app.config['TIANHE_SUBJECT_PREFIX']+subject,sender=app.config['TIANHE_MAIL_SENDER']
                ,recipients=[to])
        msg.body = render_template(template+'.txt',**kwargs)
        msg.html = render_template(template+'.html',**kwargs)
        thr = Thread(target=send_async_email,args=[app,msg])
        thr.start()
        return thr
def send_async_email(app,msg):
    try:
        with app.app_context():
            mail.send(msg)
    except:
        print 'cuowu'
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    users = db.relationship('User',backref='role',lazy='dynamic')

    def __repr__(self):
        return '<Role %r' % self.name

class User(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),unique=True,index=True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    def __repr__(self):
        return '<User %r>' % self.username



@app.route('/',methods=['GET','POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username = form.name.data)
            print form.name.data
            db.session.add(user)
            session['known'] = False
            if app.config['TIANHE_ADMIN']:
                send_email(app.config['TIANHE_ADMIN'],'new user','mail/new_user',user=user)
                print form.name.data
            else:
                session['known'] = True
        session['name']= form.name.data
        form.name.data=''
        return redirect(url_for('index'))
    return render_template('index.html',
                           current_time=datetime.utcnow(),
                    form=form,name=session.get('name'),known=session.get('known',False))


@app.route('/user/<name>')
def user(name):
    # return '<h1>hello %s' % name
    return render_template('user.html', name=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    manager.run()
