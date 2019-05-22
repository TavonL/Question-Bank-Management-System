import functools
import json
from flask import (
	Blueprint, g, request, session, url_for, jsonify
)

from flaskr.db import (
	get_db, excute_select, excute_delete, excute_insert, excute_procedure, excute_update
)

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route('/login', methods=('POST', ))
def login():
	# Log in a registered user by adding the user id to the session.
	# code 0 成功 -1 不成功
	data = request.get_data()
	data = json.loads(data)
	db = get_db()
	sql = "SELECT user_pwd,user_auth FROM user WHERE user_name = '{username}'".format(username = data["user_name"])
	db_res = excute_select(db, sql)
	code = 0
	if db_res == ():
		code = -1
	else:
		db_res = [list(item) for item in list(db_res)]
		if db_res[0][0] != data["user_pwd"]:
			code = -1

	if code == 0:
		# store the user id in a new session
		session.clear()
		session['user_name'] = data["user_name"]
		session['user_auth'] = db_res[0][1]
		return jsonify({"code":code, "user_name":data["user_name"], "user_auth":db_res[0][1]})
	return jsonify({"code":code})


@bp.route('/logout')
def logout():
	# Clear the current session, including the stored user id.
	session.clear()
	return jsonify(1)


@bp.route('/add_user', methods=('POST', ))
def add_user():
	#code 0 成功 -1 不成功
	data = request.get_data()
	data = json.loads(data)
	db = get_db()
	sql = "SELECT * FROM user WHERE user_name = '{username}'".format(username=data["user_name"])
	db_res = excute_select(db, sql)
	code = 0
	if db_res != ():
		code = -1
	else:
		sql = "INSERT INTO user(user_name, user_pwd, user_auth)\
		 VALUES ('{name}', '{pwd}','{auth}')".format(
		 	name=data["user_name"], pwd=data["user_pwd"], auth=data["user_auth"]
		 	)
		db_res = excute_insert(db, sql)
		if db_res == "Error":
			code = 1
	return jsonify({"code":code})


@bp.route('/update_pwd', methods=('POST', ))
def update_pwd():
	#code 0 成功 -1 旧密码不对 -2 两次密码不一致
	data = request.get_data()
	data = json.loads(data)
	if (data["new_pwd"] != data["repeat_pwd"]):
		return jsonify({"code":-2})
	db = get_db()
	sql = "SELECT * FROM user WHERE user_name = '{username}'".format(username=data["user_name"])
	db_res = excute_select(db, sql)
	code = 0
	if db_res == ():
		code = -1
	else:
		db_res = [list(item) for item in list(db_res)]
		if db_res[0][1] != data["old_pwd"]:
			code = -1
		else:
			sql = "UPDATE user SET user_pwd = '{new_pwd}' WHERE user_name = '{username}'".format(
				new_pwd=data["new_pwd"], username=data["user_name"]
				)
			db_res = excute_update(db, sql)
			if db_res == "Error":
				code = -1
	return jsonify({"code":code})


@bp.before_app_request
def load_logged_in_user():
	"""
	If a user id is stored in the session, load the user object from
	the database into ``g.user``.
	"""
	user_name = session.get('user_name')

	if user_name is None:
		g.user = None
	else:
		g.user = user_name


# def login_required(view):
# 	"""
# 	View decorator that redirects anonymous users to the login page.
# 	"""
# 	@functools.wraps(view)
# 	def wrapped_view(**kwargs):
# 		if g.user is None:
# 			return redirect(url_for('auth.login'))

# 		return view(**kwargs)

# 	return wrapped_view