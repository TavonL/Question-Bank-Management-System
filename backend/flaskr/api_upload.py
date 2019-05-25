import functools
import json
import os
import re
from flask import (
	Blueprint, g, request, session, url_for, jsonify, make_response
)

from flaskr.db import (
	get_db, excute_select, excute_delete, excute_insert, excute_procedure, excute_update
)

from python_script.md2word import (
	convertFile, addHeader, createMdFile, deleteFiles
)

from flaskr.uploader import Uploader

bp = Blueprint('upload', __name__, url_prefix='/api/upload', static_folder='static')


types = ['不限', '填空题', '单选题', '多选题', '应用题', '综合题']


# @bp.route('/', methods=('GET', ))
# def Hello_World():
# 	return jsonify(app.static_folder)


@bp.route('/Paper', methods=('POST', ))
def upload_Paper():
	# 上传试卷试题 code 0成功 -1不成功 
	data = request.get_data()
	data = json.loads(data)
	# return jsonify(1)
	paperForm = data["paperInfoForm"]
	questionsForm = data["questionsForm"]
	# 定义数据库连接
	db = get_db()
	# 插入试卷
	sql = "INSERT INTO paper(paper_subject, grade, paper_info, source)\
		VALUES ({subject},{grade},'{info}',{source})".format(
			subject=paperForm["paper_subject"], grade=paperForm["paper_grade"],
			info=paperForm["paper_year"]+paperForm["paper_name"],
			source=paperForm["paper_source"]
			)
	db_res = excute_insert(db, sql)
	if db_res == 'Error':
		return jsonify({"code" : -1})
	# 查看试卷号
	sql = "SELECT paper_no FROM paper WHERE paper_subject={subject} AND grade={grade} \
		AND paper_info='{info}' AND source={source}".format(
			subject=paperForm["paper_subject"], grade=paperForm["paper_grade"],
			info=paperForm["paper_year"]+paperForm["paper_name"],
			source=paperForm["paper_source"]
			)
	db_res = excute_select(db, sql)
	if db_res == ():
		return jsonify({"code" : -1})
	paper_no = db_res[0][0]
	# return jsonify(paper_no)
	# 插入题目
	code = 0
	error_result = []
	for i in range(0, len(questionsForm)):
		item = questionsForm[i]
		if item["question_type"] != 5:
			sql = "INSERT INTO question(paper_no, question_type, question_diff, \
				question_content, question_answer, question_analy, know_no) \
				VALUES ({paper},'{type}',{diff},'{content}','{answer}','{analy}',{know_no})".format(
					paper=paper_no, type=types[item["question_type"]],
					diff=item["question_diff"], content=item["question_content"],
					answer=item["question_answer"], analy=item["question_analy"],
					know_no=item["knowledge_point"]
					)
			db_res = excute_insert(db, sql)
			# return jsonify(db_res)
			if db_res == 'Error':
				code = -1
				error_result.append(i)
		else:
			sql = "INSERT INTO question(paper_no, question_type, question_diff, \
				question_content, question_analy, know_no) \
				VALUES ({paper},'{type}',{diff},'{content}','{analy}',{know_no})".format(
					paper=paper_no, type=types[item["question_type"]],
					diff=item["question_diff"], content=item["question_content"],
					analy=item["question_analy"], know_no=item["knowledge_point"]
					)
			# return jsonify(sql)
			db_res = excute_insert(db, sql)
			# return jsonify(db_res)
			if db_res == 'Error':
				code = -1
				error_result.append(i)
			# 查看刚插入的编号
			sql = "SELECT question_no FROM question WHERE paper_no={paper} AND \
				question_type='{type}' AND question_diff={diff} AND question_content='{content}' \
				AND question_analy='{analy}' AND know_no={know_no}".format(
					paper=paper_no, type=types[item["question_type"]],
					diff=item["question_diff"], content=item["question_content"],
					analy=item["question_analy"], know_no=item["knowledge_point"]
				)
			db_res = excute_select(db, sql)
			# return jsonify(db_res)
			if db_res == ():
				code = -1
			else:
				super_question_no = db_res[0][0]
				# return jsonify(db_res[0][0])
				for subitem in item["question_answer"]:
					# return jsonify(subitem)
					sql = "INSERT INTO little_question(little_question_type, \
					 little_question_content, little_question_answer, \
					 super_question_no) VALUES ('{type}','{content}','{answer}',\
					 {super_no})".format(type=types[subitem["question_type"]],
						content=subitem["question_content"],
						answer=subitem["question_answer"], super_no=super_question_no
						)
					# return jsonify(sql)
					db_res = excute_insert(db, sql)
					if db_res == 'Error':
						code = -1
						error_result.append(i)
	if code == 0:
		return jsonify({"code":0})
	return jsonify({"code":-1, "error_result":error_result})


# @bp.route('/PaperInfo', methods=('POST', ))
# def upload_PaperInfo():
# 	# 上传试卷信息 code -1 有同名试卷 code -2 该年级没有该科目或者该学校不存在
# 	data = request.get_data()
# 	data = json.loads(data)
# 	# return jsonify(1)
# 	data = data["paperInfoForm"]
# 	# return jsonify("1")
# 	# 查有没有同名试卷
# 	db = get_db()
# 	sql = "SELECT * FROM paper WHERE paper_subject={subject} AND grade={grade} \
# 	AND paper_info='{info}' AND source={source}".format(
# 			subject=data["paper_subject"], grade=data["paper_grade"],
# 			info=data["paper_year"]+data["paper_name"],source=data["paper_source"]
# 			)
# 	db_res = excute_select(db, sql)
# 	if db_res != ():
# 		return jsonify({"code" : -1})
# 	# 插入，为了并发性考虑，我觉得最好创建触发器
# 	sql = "INSERT INTO paper(paper_subject, grade, paper_info, source)\
# 		VALUES ({subject},{grade},'{info}',{source})".format(
# 			subject=data["paper_subject"], grade=data["paper_grade"],
# 			info=data["paper_year"]+data["paper_name"],source=data["paper_source"]
# 			)
# 	db_res = excute_insert(db, sql)
# 	if db_res == 'Error':
# 		return jsonify({"code" : -2})
# 	# 查看试卷号
# 	sql = "SELECT paper_no FROM paper WHERE paper_subject={subject} AND grade={grade} \
# 	AND paper_info='{info}' AND source={source}".format(
# 			subject=data["paper_subject"], grade=data["paper_grade"],
# 			info=data["paper_year"]+data["paper_name"],source=data["paper_source"]
# 			)
# 	db_res = excute_select(db, sql)
# 	if db_res != ():
# 		db_res = db_res[0]
# 		return jsonify({"code" : 0, "paper_no":db_res[0]})
# 	return jsonify({"code" : -3})


# @bp.route('/Question', methods=('POST', ))
# def upload_Question():
# 	# 返回重复/错误 题号
# 	data = request.get_data()
# 	data = json.loads(data)
# 	# return jsonify(1)
# 	db = get_db()
# 	paper_no = data["paper_no"]
# 	sql = "SELECT paper_no FROM paper INNER JOIN (SELECT source FROM paper \
# 		WHERE paper_no = {0}) AS T1 ON paper.source = T1.source".format(paper_no)
# 	db_res = excute_select(db, sql)
# 	db_res =[list(item) for item in list(db_res)]
# 	paper_no = []
# 	for item in db_res:
# 		for i in item:
# 			paper_no.append(str(i))
# 	# return jsonify(paper_no)
# 	paper_no = ", ".join(paper_no)
# 	# return jsonify(paper_no)
# 	data = data["questionsForm"]
# 	db = get_db()
# 	for i in range(0, len(data)):
# 		tmp = data[i]
# 		# 题目查重, 最好略过url 进行查重
# 		sql = "SELECT * FROM question WHERE "
# 	return jsonify(1)


@bp.route('/Fig', methods=('GET', 'POST', 'OPTIONS'))
def upload_Fig():
	mimetype = 'application/json'
	action = request.args.get('action')
	result = {}

	with open(os.path.join(bp.static_folder, 'ueditor', 'php', 
							'config.json'), encoding = 'utf-8') as fp:
		try:
			CONFIG = json.loads(re.sub(r'\/\*.*\*\/', '', fp.read()))
		except:
			CONFIG = {}

	if action == 'config':
		# 初始化时，返回配置文件给客户端
		result = CONFIG
	elif action == 'uploadimage':
		fieldName = CONFIG.get('imageFieldName')
		config = {
			"pathFormat": CONFIG['imagePathFormat'],
			# 上传保存路径,可以自定义保存路径和文件名格式
			"maxSize": CONFIG['imageMaxSize'], # 上传大小限制
			"allowFiles": CONFIG['imageAllowFiles']
		}
		if fieldName in request.files:
			field = request.files[fieldName]
			uploader = Uploader(field, config, bp.static_folder)
			result = uploader.getFileInfo()
		else:
			result['state'] = '上传接口出错'
	else:
		result['state'] = '请求地址出错'

	result = json.dumps(result)
	if 'callback' in request.args:
		callback = request.args.get('callback')
		if re.match(r'^[\w_]+$', callback):
			result = '%s(%s)' % (callback, result)
			mimetype = 'application/javascript'
		else:
			result = json.dumps({'state': 'callback参数不合法'})

	res = make_response(result)
	res.mimetype = mimetype
	res.headers['Access-Control-Allow-Origin'] = '*'
	res.headers['Access-Control-Allow-Headers'] = 'X-Requested-With,X_Requested_With'
	return res


@bp.route('/Schools', methods=('POST', ))
def upload_Schools():
	data = request.get_data()
	data = json.loads(data)
	code = 0
	db = get_db()
	# sql = "SELECT school_no FROM school WHERE school_name={super} \
	# 	".format(super=data["parent_name"])
	# db_res = db.excute_select()
	# if db_res == ():
	# 	return jsonify({"code":-1})
	# super_no = db_res[0][0]
	if data["opt"] == "add":
		sql = "INSERT INTO school(school_name, school_nature, super_no) VALUES \
			  ('{name}', '{nature}', {super})".format(
				name=data["school_name"], nature=data["school_nature"], 
				super=data["parent_no"]
				)
		db_res = excute_insert(db, sql)
	elif data["opt"] == "del":
		sql = "DELETE FROM school WHERE school_name='{name}'".format(
			name=data["school_name"])
		db_res = excute_delete(db, sql)
	if db_res == 'Error':
		code = -1
	return jsonify({"code":code})


@bp.route('/KnowledgePoints', methods=('POST', ))
def upload_KnowledgePoints():
	data = request.get_data()
	data = json.loads(data)
	code = 0
	db = get_db()
	# sql = "SELECT know_no FROM know WHERE know_name={super} \
	# 	".format(super=data["parent_name"])
	# db_res = db.excute_select()
	# if db_res == ():
	# 	return jsonify({"code":-1})
	# super_no = db_res[0][0]
	if data["opt"] == "add":
		sql = "INSERT INTO know(know_name, super_no) VALUES \
			  ('{name}', {super})".format(
				name=data["know_name"], super=data["parent_no"]
				)
		db_res = excute_insert(db, sql)
	elif data["opt"] == "del":
		sql = "DELETE FROM know WHERE know_name='{name}'".format(
			name=data["know_name"])
		db_res = excute_delete(db, sql)
	if db_res == 'Error':
		code = -1
	return jsonify({"code":code})