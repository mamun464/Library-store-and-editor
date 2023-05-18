from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy


import sqlite3

from sqlalchemy.orm import session

# db = sqlite3.connect("books-collection.db") ##creating data base
# cursor = db.cursor()
# # cursor.execute("CREATE TABLE books (id INTEGER PRIMARY KEY, "
# #                "title varchar(250) NOT NULL UNIQUE, "
# #                "author varchar(250) NOT NULL, "
# #                "rating FLOAT NOT NULL)")
#
# cursor.execute("INSERT INTO books VALUES(3, 'Hassrry ssPottejr', 'J. K. Rowling', '9.3')")
# db.commit()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"

db = SQLAlchemy(app)
Bootstrap(app)



class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250),nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<Book %r>' % self.title

with app.app_context():
    db.create_all()





all_books = []


@app.route('/')
@app.route('/index')
def home():
    global all_books
    all_books = db.session.query(Book).all()
    return render_template("index.html", books=all_books, size=len(all_books))


@app.route("/add",  methods=["GET", "POST"])
def add():
    global all_books
    if request.method == 'POST':
        #reading rata from form
        book_name = request.form['book_name']
        athor_name = request.form['athor_name']
        rating= request.form['rating']

        ##validate form
        error_fields = []

        if not book_name:
            error_fields.append('book_name')
        if not athor_name:
            error_fields.append('athor_name')
        if not rating:
            error_fields.append('rating')

        if error_fields:
            return render_template('add.html', error_fields=error_fields)

        try:
            rating = float(rating)
        except ValueError:
            return 'Rating must be a valid number'

        #Book data entry
        new_book = Book(title=book_name, author=athor_name, rating=rating)
        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template('add.html')

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_rating(id):
    book_id = id
    book_to_update = Book.query.get(book_id)

    if request.method == 'POST':
        ratting_cng = request.form['ratting_cng']
        print(ratting_cng)
        book_to_update.rating=ratting_cng
        db.session.commit()
        return redirect(url_for('home'))
    else:
        print("------------false------------")

    return render_template("edit.html",book=book_to_update)

@app.route("/delete/<int:id>")
def delete(id):
    book_id = id
    book_to_delete = Book.query.get(book_id)
    db.session.delete(book_to_delete)
    db.session.commit()

    return redirect(url_for('home'))



if __name__ == "__main__":
    app.run(debug=True)

