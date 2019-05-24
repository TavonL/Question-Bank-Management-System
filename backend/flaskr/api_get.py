import functools
import json
from flask import (
	Blueprint, g, request, session, url_for, jsonify
)

from flaskr.db import (
	get_db, excute_select, excute_delete, excute_insert, excute_procedure, excute_update
)

from flaskr.functions import(
	get_all_sub, get_parent_no_list, get_parent_name_list, get_child_list, dfs_children
)

bp = Blueprint('get', __name__, url_prefix='/api/get')

types = ['不限', '填空题', '单选题', '多选题', '应用题', '综合题']
natures = ['不限', '公立', '私立']

# @bp.route('/Test', methods=('GET', ))
# def Test():
# 	data = request.get_data()
# 	data = json.loads(data)
# 	result = get_know_child_list(str(data["question_no"]))
# 	return jsonify(result)


@bp.route('/Question', methods=('POST', ))
def get_Question():
	#试题库获取每页题目
	data = request.get_data()
	data = json.loads(data)
	
	paper_grade = [str(item) for item in data["conditionForm"]["paper_grade"]]
	paper_grade = ", ".join(paper_grade) # "10, 11, 12"
	
	paper_subject = ""
	if data["conditionForm"]["paper_subject"] != 0:
		paper_subject = "AND paper_subject = {0}".format(data["conditionForm"]["paper_subject"])
	
	paper_source = ""
	if data["conditionForm"]["paper_source"] != 0:
		source = get_parent_no_list("source", str(data["conditionForm"]["paper_source"]))
		paper_source = "AND source in ({0})".format(", ".join(source))
	# return jsonify(paper_source)
	paper_nature = ""
	if data["conditionForm"]["paper_nature"] != 0:
		paper_nature = "AND source in (SELECT school_no FROM school \
				WHERE school_nature = '{0}')".format(natures[data["conditionForm"]["paper_nature"]])
	# return jsonify(paper_nature)
	knowledge_point = ""
	if data["conditionForm"]["knowledge_point"] != 0:
		know = get_child_list("know", str(data["conditionForm"]["knowledge_point"]))
		know = ", ".join(know)
		knowledge_point = "AND know_point in (%s)" % know
	
	question_type = ""
	if data["conditionForm"]["question_type"] != 0:
		question_type = "AND question_type = '{0}'".format(types[data["conditionForm"]["question_type"]])
	
	question_diff = ""
	if data["conditionForm"]["question_diff"] != 0:
		question_diff = "AND question_diff = {0}".format(data["conditionForm"]["question_diff"])
	# return jsonify(question_diff)
	sql = "SELECT T2.question_no, T2.question_content, T1.paper_info FROM \
		(SELECT paper_info, paper_no FROM paper WHERE grade in ({grade}) \
		{subject} {source} {nature}) AS T1 \
		INNER JOIN (SELECT paper_no, question_no, question_content FROM question \
		WHERE Locate('{keyword}' ,question_content) > 0 {know_point} {ques_type} \
		{ques_diff}) AS T2 ON T1.paper_no=T2.paper_no".format(grade=paper_grade, subject=paper_subject,
				 source=paper_source, nature=paper_nature, 
				 keyword=data["conditionForm"]["keyword"],
				 know_point=knowledge_point, ques_type=question_type,
				 ques_diff=question_diff)
	# return jsonify(sql)
	db = get_db()
	db_res = excute_select(db, sql)
	# return jsonify(db_res)
	length = min(data["quetisonNum"] + data["questionOffset"], len(db_res))
	result = []
	for i in range(data["questionOffset"], length):
		item = list(db_res[i])
		dic = {"question_no": str(item[0]),
				"question_content": item[1],
				"paper_name": item[2],
				# "figure_url": item[3]
		}
		result.append(dic)
	return jsonify({"quantity":len(db_res), "questions": result})


@bp.route('/QuestionDetail', methods=('GET', ))
def get_QuestionDetail():
	# 查看题目详情
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
		db_res = [list(item) for item in list(db_res)]
		db_res = db_res[0]
		# return jsonify(db_res[7])
		know_list = get_parent_name_list("know", str(db_res[7]))
		# return jsonify(know_list)
		# 查看有没有子题目
		sql = "SELECT little_question_no, little_question_type, little_question_content, \
				little_question_answer, little_question_analy \
		 		FROM little_question where super_question_no = {question_no} order by question_no".format(question_no=data["question_no"])
		res = excute_select(db, sql)
		result = []
		for item in res:
			item = list(item)
			dic = {"little_question_no":str(item[0]),
				   "little_question_type":str(types.index(item[1])),
				   "little_question_content":item[2],
				   "little_question_answer":item[3],
				   "little_question_analy":item[4]
				  }
			result.append(dic)
		dic = { "code":code , 
				"question_diff":str(db_res[0]), 
				"question_type":str(types.index(db_res[1])),
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
	db_res = [list(item) for item in list(db_res)]
	# return jsonify(db_res)
	dic = dict()
	for item in db_res:
		super_no = "0" if item[2] == None else str(item[2])
		super_name = "0" if item[3] == None else item[3]
		if super_no not in dic:
			dic[super_no] = {"no": super_no, "label": super_name, "children" : []}
		if str(item[0]) not in dic:
			dic[str(item[0])] = {"no": str(item[0]), "label": item[1], "children" : []}
		dic[super_no]["children"].append(str(item[0]))
	# return jsonify(dic)
	dic = dfs_children(dic, "0")
	res = dic["0"]["children"]
	return jsonify(res)


@bp.route('/SourcesNo', methods=('GET', ))
def get_SourcesNo():
	# 获取所有试卷来源, 按市-区-学校
	sql = "SELECT T1.school_no, T1.school_name, T1.super_no, T2.school_name\
			FROM school AS T1 LEFT JOIN school AS T2 ON T1.super_no = T2.school_no"
	db = get_db()
	db_res = excute_select(db, sql)
	db_res = [list(item) for item in list(db_res)]
	# return jsonify(db_res)
	dic = dict()
	for item in db_res:
		super_no = "0" if item[2] == None else str(item[2])
		super_name = "0" if item[3] == None else item[3]
		if super_no not in dic:
			dic[super_no] = {"no": super_no, "label": super_name, "children" : []}
		if str(item[0]) not in dic:
			dic[str(item[0])] = {"no": str(item[0]), "label": item[1], "children" : []}
		dic[super_no]["children"].append(str(item[0]))
	# return jsonify(dic)
	dic = dfs_children(dic, "0")
	res = dic["0"]["children"]
	return jsonify(res)


# @bp.route('/SourcesNature', methods=('GET', ))
# def get_SourcesNature():
# 	# 获取所有试卷来源，按性质-学校
# 	sql = "SELECT school_no, school_name, school_nature FROM school"
# 	db = get_db()
# 	db_res = excute_select(db, sql)
# 	db_res = [list(item) for item in list(db_res)]
# 	# return jsonify(db_res)
# 	dic = dict()
# 	result = []
# 	for item in db_res:
# 		if item[2] not in dic:
# 			result.append(item[2])
# 			dic[item[2]] = {"value":len(result), "label":item[2], "children":[]}
# 		tmp = {"value":len(dic[item[2]]["children"]) + 1, "label":item[1], "no": str(item[0])}
# 		dic[item[2]]["children"].append(tmp)

# 	length = len(result)
# 	for i in range(0, length):
# 		result[i] = dic[result[i]]
# 	return jsonify(result)
