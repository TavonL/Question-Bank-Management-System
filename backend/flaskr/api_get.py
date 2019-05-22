import functools
import json
from flask import (
	Blueprint, g, request, session, url_for, jsonify
)

from flaskr.db import (
	get_db, excute_select, excute_delete, excute_insert, excute_procedure, excute_update
)

bp = Blueprint('get', __name__, url_prefix='/api/get')

subject = {'0': '不限', '1': '语文', '2': '数学', '3': '英语', '4': '物理', '5': '化学', '6': '生物', '7': '地理', '8': '历史', '9': '政治'}
question_type = ['不限', '填空题', '单选题', '多选题', '应用题', '简答题', '综合题', '阅读']

@bp.route('/Question', methods=('POST', ))
def get_Question():
	#试题库获取每页题目
	data = request.get_data()
	data = json.loads(data)
	know_point = " , ".join(data["conditionForm"]["knowledge_point"])
	# sql = "SELECT T2.question_no, T2.question_content, T1.paper_info, figure.figure_url \
	# 		FROM (SELECT paper_info, paper_no FROM paper WHERE grade = {grade} AND paper_subject = {subject}) AS T1 INNER JOIN \
	# 		(SELECT paper_no, question_no, question_content FROM question  WHERE Locate('{where}' ,question_content) > 0 AND \
	# 		question_no IN (SELECT question_no FROM kq_cor WHERE know_no IN ({know}))) AS T2 \
	# 		ON T1.paper_no = T2.paper_no LEFT JOIN figure on figure.question_no = T2.question_no \
	# 		order by T2.question_no".format(grade=int(data["conditionForm"]["paper_grade"]),
	# 							subject=int(data["conditionForm"]["paper_subject"]),
	# 							where=data["conditionForm"]["keyword"],
	# 							know=know_point)
	sql = "SELECT T2.question_no, T2.question_content, T1.paper_info, figure.figure_url \
			FROM (SELECT paper_info, paper_no FROM paper WHERE grade = {grade} AND paper_subject = {subject}) AS T1 INNER JOIN \
			(SELECT paper_no, question_no, question_content FROM question  WHERE Locate('{where}' ,question_content) > 0 AND \
			know_no IN ({know})) AS T2 \
			ON T1.paper_no = T2.paper_no LEFT JOIN figure on figure.question_no = T2.question_no \
			order by T2.question_no".format(grade=int(data["conditionForm"]["paper_grade"]),
								subject=int(data["conditionForm"]["paper_subject"]),
								where=data["conditionForm"]["keyword"],
								know=know_point)
	db = get_db()
	db_res = excute_select(db, sql)

	length = min(data["quetisonNum"] + data["questionOffset"], len(db_res))
	result = []
	for i in range(data["questionOffset"], length):
		item = list(db_res[i])
		dic = {"question_no": str(item[0]),
				"question_content": item[1],
				"paper_name": item[2],
				"figure_url": item[3]
		}
		result.append(dic)
	return jsonify({"questions": result})


@bp.route('/QuestionDetail', methods=('GET', ))
def get_QuestionDetail():
	# question_type = ['填空题', '选择题', '应用题', '阅读', '综合题']
	data = request.get_data()
	data = json.loads(data)

	sql = "SELECT T1.question_diff, T1.question_type, T1.question_content, T1.question_answer, T1.question_analy, figure_url, paper_info, know_no \
	  FROM (SELECT * from question where question_no = {question_no}) AS T1 LEFT JOIN figure on figure.question_no = T1.question_no \
	  INNER JOIN paper ON paper.paper_no = T1.paper_no".format(question_no=data["question_no"])
	# return jsonify(sql)
	db = get_db()
	db_res = excute_select(db, sql)
	code = 0
	# return jsonify(sql)
	if db_res == ():
		code = -1
	else:
		sql = "SELECT know_no, super_no from know"
		res = excute_select(db, sql)
		res = [list(item) for item in list(res)]
		dic = dict()
		for item in res:
			dic[str(item[0])] =  "0" if item[1] == None else str(item[1])
		db_res = [list(item) for item in list(db_res)]
		db_res = db_res[0]
		know_list = [str(db_res[7])]
		item = dic[str(db_res[7])]
		while item != "0":
			know_list.append(item)
			item = dic[item]
		know_list.reverse()

		# 查有没有子题目
		sql = "SELECT little_question_no, little_question_type, little_question_content, \
		  little_question_answer, little_question_analy \
		  FROM little_question where super_question_no = {question_no} order by question_no".format(question_no=data["question_no"])
		res = excute_select(db, sql)
		result = []
		for item in res:
			item = list(item)
			dic = {"little_question_no":str(item[0]),
				   "little_question_type":str(question_type.index(item[1])),
				   "little_question_content":item[2],
				   "little_question_answer":item[3],
				   "little_question_analy":item[4]
				  }
			result.append(dic)
		dic = { "code":code , 
				"question_diff":str(db_res[0]), 
				"question_type":str(question_type.index(db_res[1])),
				"question_content":db_res[2],
				"question_answer":db_res[3],
				"question_analy":db_res[4],
				"figure_url":db_res[5],
				"paper_name":db_res[6],
				"knowledge_point":know_list,
				"little_question":result,
			  }
		return jsonify(dic)
	return jsonify({"code":code})


@bp.route('/KnowledgePoints', methods=('GET', ))
def get_KnowledgePoints():
	# 获取所有知识点
	sql = "SELECT T1.know_no, T1.know_name, T1.super_no, T2.know_name\
			FROM know AS T1 LEFT JOIN know AS T2 ON T1.super_no = T2.know_no"
	db = get_db()
	db_res = excute_select(db, sql)
	result = []
	for item in db_res:
		item = list(item)
		dic = {"know_no": str(item[0]),
			 "know_name": item[1],
			 "super_no": "0" if item[2] == None else str(item[2]),
			 "super_name": item[3]
		}
		result.append(dic)
	return jsonify({"know": result})


