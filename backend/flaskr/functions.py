import json
from flask import jsonify

from flaskr.db import (
	get_db, excute_select, excute_delete, excute_insert, excute_procedure, excute_update
)


def get_all_sub(sql):
	# 返回字典，所有知识点/source对应的一级子知识点/source(列表)，学科/上海的父节点为"0"
	db = get_db()
	res = excute_select(db, sql)
	res = [list(item) for item in list(res)]

	dic = dict()
	for item in res:
		super_no = "0" if item[1] == None else str(item[1])
		if super_no not in dic:
			dic[super_no] = []
		if str(item[0]) not in dic:
			dic[str(item[0])] = []
		dic[super_no].append(str(item[0]))
	return dic


def get_parent_no_list(flag, point):
	# 给定一个知识点/source，返回知识点/source列表，父、子、子、最后当前知识点/source
	sql = ""
	if flag == "know":
		sql = "SELECT know_no, super_no from know"
	else:
		sql = "SELECT school_no, super_no from school"
	db = get_db()
	res = excute_select(db, sql)
	res = [list(item) for item in list(res)]
	dic = dict()
	for item in res:
		dic[str(item[0])] =  "0" if item[1] == None else str(item[1])
	know_list = [point]
	item = dic[point]
	while item != "0":
		know_list.append(item)
		item = dic[item]
	know_list.reverse()
	return know_list


def get_parent_name_list(flag, point):
	# 给定一个知识点/source，返回知识点/source列表，父、子、子、最后当前知识点/source
	sql = ""
	if flag == "know":
		sql = "SELECT know_no, know_name, super_no from know"
	else:
		sql = "SELECT school_no, school_name, super_no from school"
	db = get_db()
	res = excute_select(db, sql)
	res = [list(item) for item in list(res)]
	dic = dict()
	for item in res:
		dic[str(item[0])] =  {"super_no": "0", "name":item[1]} if item[2] == None else {"super_no":str(item[2]), "name":item[1]}
	# return jsonify(dic)
	know_list = [dic[point]["name"]]
	item = dic[point]["super_no"]
	while item != "0":
		know_list.append(dic[item]["name"])
		item = dic[item]["super_no"]
	know_list.reverse()
	return know_list


def get_child_list(flag, point):
	# 返回列表，当前知识点/source对应的所有子知识点/source, 且包含当前知识点/source
	sql = ""
	if flag == "know":
		sql = "SELECT know_no, super_no from know"
	else:
		sql = "SELECT school_no, super_no from school"
	dic = get_all_sub(sql)
	# return dic
	for item in dic[point]:
		dic[point].extend(dic[item])
	dic[point].append(point)
	return dic[point]


def dfs_children(dic, current):
	# 形成列表嵌套字典嵌套......
	if "children" not in dic[current]:
		return dic
	length = len(dic[current]["children"])
	for i in range(0, length):
		item = dic[current]["children"][i]
		dfs_children(dic, item)
		dic[item]["value"] = i + 1
		dic[current]["children"][i] = dic[item]
		dic.pop(item)
	return dic
