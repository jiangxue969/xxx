from flask import Flask, render_template, request, session, redirect, flash, url_for
from werkzeug.urls import url_parse

from app import app, db
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User


#2个路由
@app.route('/')
@app.route('/index')
@login_required
# @login_auto
#1个视图函数
def index():
	# user = {'username':'jiang'}
	# posts = [  # 创建一个列表：帖子。里面元素是两个字典，每个字典里元素还是字典，分别作者、帖子内容。
	# 	{
	# 		'author': {'username': 'John'},
	# 		'body': '可乐!'
	# 	},
	#     {
	# 	    'author': {'username': 'Susan'},
	# 	    'body': '美年达!'
	#     }
	# ]posts=posts
	return render_template('index.html')

@app.route('/login',methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))

	login_form = LoginForm()
	if login_form.validate_on_submit():
		user = User.query.filter_by(username=login_form.username.data).first()
		if user is None or not user.check_password(login_form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))

		login_user(user, remember=login_form.remember_me.data)

		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(url_for('index'))

	return render_template('login.html', title='login', form=login_form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
