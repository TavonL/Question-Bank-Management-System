# -*-codeing:utf-8 -*-
import pymysql

from flask import g


def get_db():
	"""Connect to the application's configured database. The connection
	is unique for each request and will be reused if this is called
	again
 	"""
	if 'db' not in g:
		g.db = pymysql.connect(
			host='localhost',
			port=3306,
			user='root',
			password='',
			database='qm',
			charset='utf8'
		)
	return g.db


def close_db(e = None):
	"""If this request connected to the database, close the
	connection.
	"""
	db = g.pop('db', None)

	if db is not None:
		db.close()


def init_app(app):
	"""Register database functions with the Flask app. This is called by
	the application factory.
	"""
	app.teardown_appcontext(close_db)


def excute_select(db, sql):
	cursor = db.cursor()
	select_res = ()
	try:
		cursor.execute(sql)
		select_res = cursor.fetchall()
	except Exception as e:
		print(e)
		db.rollback()
	cursor.close()	
	return select_res  # 查不到返回()

def excute_insert(db, sql):
	cursor = db.cursor()
	res = ''
	try:
		cursor.execute(sql)
		db.commit()
		res = 'Successful'
		print ('Successful!')
	except Exception as e:
		db.rollback()
		res ='Error'
		print("[Insert Error!]", e)
		db.rollback()
	cursor.close()
	return res

def excute_delete(db, sql):
	cursor = db.cursor()
	res = ''
	try:
		cursor.execute(sql)
		db.commit()
		print ('Successful!')
		res = 'Sucessful'
	except Exception as e:
		db.rollback()
		res = 'Error'
		print("[Delete Error!]", e)
	cursor.close()
	return res

def excute_update(db, sql):
	cursor = db.cursor()
	res = ''
	try:
		cursor.execute(sql)
		db.commit()
		print ('Successful!')
		res = 'Sucessful'
	except Exception as e:
		db.rollback()
		res = 'Error'
		print("[Update Error!]", e)
	cursor.close()
	return res

def excute_procedure(db, sql):
	cursor = db.cursor()
	select_res = ()
	try:
		cursor.execute(sql)
		select_res = cursor.fetchall()
	except Exception as e:
		print(e)
		db.rollback()
	cursor.close()
	return select_res  # 查不到返回()


# class Question_Bank_MS():

# 	def __init__(self):
# 		self.db = pymysql.connect(
# 			host='localhost',
# 			port=3306,
# 			user='root',
# 			password='22@lingAO',
# 			database='qm',
# 			charset='utf8'
# 		)
# 		self.cursor = self.db.cursor()

# 	def __del__(self):
# 		self.cursor.close()
# 		self.db.close()

# 	def excute_select_sql(self, sql):
# 		select_res = ()
# 		try:
# 			self.cursor.execute(sql)
# 			select_res = self.cursor.fetchall()
# 		except Exception as e:
# 			print(e)
# 			self.db.rollback()
# 		return select_res  # 查不到返回()

# 	def excute_insert_sql(self, sql):
# 		try:
# 			self.cursor.execute(sql)
# 			self.db.commit()
# 			print ('Successful!')
# 			return 'Sucessful'
# 		except Exception as e:
# 			print("[Insert Error!]", e)
# 			self.db.rollback()
# 			return 'Error'

# 	def excute_delete_sql(self, sql):
# 		try:
# 			self.cursor.execute(sql)
# 			self.db.commit()
# 			print ('Successful!')
# 			return 'Sucessful'
# 		except Exception as e:
# 			print("[Delete Error!]", e)
# 			self.db.rollback()
# 			return 'Error'

# 	def excute_update_sql(self, sql):
# 		try:
# 			self.cursor.execute(sql)
# 			self.db.commit()
# 			print ('Successful!')
# 			return 'Sucessful'
# 		except Exception as e:
# 			print("[Update Error!]", e)
# 			self.db.rollback()
# 			return 'Error'

# 	def excute_procedure_sql(self, sql):
# 		select_res = ()
# 		try:
# 			self.cursor.execute(sql)
# 			select_res = self.cursor.fetchall()
# 		except Exception as e:
# 			print(e)
# 			self.db.rollback()
# 		return select_res  # 查不到返回()

# if __name__ == '__main__':
	# test = Question_Bank_MS()
	# # SQL___ = "insert into school(school_name, school_nature) values('测试初中','公办普通初中')"
	# # all_info = test.excute_insert_sql(SQL___)
	# # SQL___ = "select * from school"
	# # all_info = test.excute_select_sql(SQL___)
	# exe = "select user_pwd, user_auth from user where user_name = '%s'" % "丁二"
	# select_user_res = list(test.excute_select_sql(exe))
	# select_user_res = [list(item) for item in select_user_res]
	# print(select_user_res)
	# print(select_user_res[0][0])
	# # print(all_info)
