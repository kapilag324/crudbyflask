from flask import render_template,request, redirect,render_template_string,url_for, flash
from crud import app, celery, cache
from crud import db
from crud.models import Book
from crud.tasks import *
import uuid




@app.route('/', methods=["GET", "POST"])
@cache.cached(timeout =50)
def home():
	return render_template("home.html"), 200


@app.route('/add', methods = ["GET","POST"])
def add():
	return render_template("add.html"), 200

@app.route('/allBooks',methods=["GET", "POST"])
def allBooks():
	#books = None
	try:
		# books = Book.query.all()
		books = cache.get('title')
		print ('dssss')
		print (books)
		print ('-----------')
		#print("helo world")
		# books = str(books)
		# print(books)
		if books  == None or books == '':
			print('hello')	
			books = Book.query.all()
			cache.set('title', books)
	except Exception as e:
		print("can't print")	
		print (e)
	return render_template('show.html', books  = books), 200

# @cache.cached(timeout=50000, key_prefix='title')
# def get_all_comments():
#     comments = do_serious_dbio()
#     return [x.author for x in commen




@app.route('/addData', methods=["GET","POST"])
def addData():
	global title_book
	title_book = request.form.get("title")
	idd = uuid.uuid1()
	res=insert.delay(idd,title_book)
	# db.session.expunge_all()
	# db.session.close()
	flash(f'Task id is  { idd }', 'success')
	return redirect("add"), 200



@app.route("/update", methods=["POST"])
def update():
    newtitle = request.form.get("newtitle")
    oldtitle = request.form.get("oldtitle")
    res = updateData.delay(newtitle, oldtitle)
    return redirect("/"), 200

@app.route("/delete", methods=["POST"])
def delete():
	try:
		title = request.form.get("title")
		deleteData.delay(title)
	except Exception as e:
		print("can't delet")
		print(e)
	return redirect("/"),200




@app.route('/singleBook',methods=["GET", "POST"])
def singleBook():
	books = None
	try:
		# books = Book.query.all()
		idd = request.form.get("id")
		books = cache.get('idd')
		print(idd)
		print ('dssss')
		print (books)
		print ('-----------')
		#print("helo world")
		# books = str(books)
		# print(books)
		if books  == None or books == '':
			print('hello')	
			books = Book.query.filter_by(id = idd).first()
			if books == None or books =='':
				return "wait task is in progress or either ur keys is deleted", 202
			print(books)
			cache.set(idd, books)
	except Exception as e:
		print("can't print")	
		print (e)
	return render_template('showone.html', books  = books), 200


