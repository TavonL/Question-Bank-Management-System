import pymysql


class Question_Bank_MS():

	def __init__(self):
		self.db = pymysql.connect(
			host='localhost',
			port=3306,
			user='root',
			password='22@lingAO',
			database='qm',
			charset='utf8'
		)
		self.cursor = self.db.cursor()

	def __del__(self):
		self.cursor.close()
		self.db.close()

	def excute_select_sql(self, sql):
		select_res = ()
		try:
			self.cursor.execute(sql)
			select_res = self.cursor.fetchall()
		except Exception as e:
			print(e)
			self.db.rollback()
		return select_res  # 查不到返回()

	def excute_insert_sql(self, sql):
		try:
			self.cursor.execute(sql)
			self.db.commit()
			print ('Successful!')
			return 'Sucessful'
		except Exception as e:
			print("[Insert Error!]", e)
			self.db.rollback()
			return 'Error'

	def excute_delete_sql(self, sql):
		try:
			self.cursor.execute(sql)
			self.db.commit()
			print ('Successful!')
			return 'Sucessful'
		except Exception as e:
			print("[Delete Error!]", e)
			self.db.rollback()
			return 'Error'

	def excute_update_sql(self, sql):
		try:
			self.cursor.execute(sql)
			self.db.commit()
			print ('Successful!')
			return 'Sucessful'
		except Exception as e:
			print("[Update Error!]", e)
			self.db.rollback()
			return 'Error'

	def excute_procedure_sql(self, sql):
		select_res = ()
		try:
			self.cursor.execute(sql)
			select_res = self.cursor.fetchall()
		except Exception as e:
			print(e)
			self.db.rollback()
		return select_res  # 查不到返回()

if __name__ == '__main__':
	test = Question_Bank_MS()
	# SQL___ = "insert into school(school_name, school_nature) values('测试初中','公办普通初中')"
	# all_info = test.excute_insert_sql(SQL___)
	# SQL___ = "select * from school"
	# all_info = test.excute_select_sql(SQL___)
	exe = "select user_pwd, user_auth from user"
	select_user_res = test.excute_select_sql(exe)
	print(select_user_res)
	print(len(select_user_res))
	for i in range(0, len(select_user_res)):
		item = list(select_user_res[i])
		print(item)
	# select_user_res = [list(item) for item in select_user_res]
	# print(select_user_res)
	# print(select_user_res[0][0])
	# print(all_info)
