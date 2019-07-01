from crud import celery, cache
from crud import db,app
from crud.models import Book
import time

@celery.task(name ='tasks.insert')
def insert(idd, title_book):
	try:	
		#print (AsyncResult.task_id)
		time.sleep(100)
		book = Book(id=idd, title=title_book)
		db.session.add(book)
		db.session.commit()
		# db.session.expunge_all()
		# db.session.close()
		books = Book.query.all()
		book = Book.query.filter_by(id = idd).first()
		cache.delete('title')
		# cache.set('title',books)
		cache.set(idd,book)
	except Exception as  e:
		print("can't add")
		print (e)

	return "DONE!!!"


@celery.task(name = 'tasks.show')
def show():
	try:
		books = Book.query.all()
	except Exception as e:
		print("can't show")
		print (e)
	return books


@celery.task(name  = 'tasks.updateData')
def updateData(newtitle, oldtitle):
	try:
		book = Book.query.filter_by(title = oldtitle).first()
		if book == None:
			return "value not exist"
		book.title = newtitle
		db.session.commit()
		# cache.delete('title')
		cache.flushall()
	except Exception as e:
	    print("Couldn't update book title")
	    print(e)
	return "UPDATION DONE"


@celery.task(name  = 'tasks.deleteData')
def deleteData(title):
	try:
		book = Book.query.filter_by(title = title).first()
		if book == None:
			return "value not exist"
		db.session.delete(book)
		db.session.commit()
		# cache.delete('title')
		cache.flushall()
	except Exception as e:
	    print("Couldn't delete book title")
	    print(e)
	return "Deletion DONE"


