#from sqlalchemy import sessionmaker
#from model import db_connect, signup_table, SignUp

#class SignUpPipeline(object):
	#def __init__(self):
#		engine = db_connect()
#		signup_table(engine)
#		self.Session = sessionmaker(bind=engine)

#	def __repr__(self):
#		return'<id {}>'.format(self.id)

#	def process_item(self, item):
#		session  = self.Session()
#		signup = SignUp(**item)
#
#		try:
#			session.add(signup)
#			session.commit()
#		except:
#			session.rollback()
#			raise
#		finally:
#			session.close()
#		return item