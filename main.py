# import necessary libraries
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

# initialize Flask app
app = Flask(__name__)

# create database connection
conn = sqlite3.connect('books.db', check_same_thread=False)
c = conn.cursor()

with open('my_sql_code.sql', 'r') as sql_file:
    sql_text = sql_file.read()
    c.executescript(sql_text)

conn.commit()


# define routes and view functions
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # retrieve search parameters from form
        print(request.form)
        title = request.form['tit']
        # author = request.form['author']
        year = request.form['yr']
        # course = request.form['course']
        # sid = request.form['sid']

        # construct SQL query
        query = 'SELECT * FROM books WHERE 1=1'
        params = []
        if title:
            query += ' AND title LIKE ?'
            params.append(f'%{title}%')
        # if author:
        #     query += ' AND author LIKE ?'
        #     params.append(f'%{author}%')
        if year:
            query += ' AND year = ?'
            params.append(int(year))
        # if course:
        #     query += ' AND course LIKE ?'
        #     params.append(f'%{course}%')
        # if sid:
        #     query += ' AND id = ?'
        #     params.append(sid)

        # execute query and retrieve results
        c.execute(query, tuple(params))
        books = c.fetchall()
        print(books)
        return render_template('search_results.html', books=books)
    else:
        return render_template('home.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        # retrieve book details from form
        title = request.form.get('itle')
        author = request.form.get('author')
        id = request.form.get('cid')
        year = request.form.get('ayear')
        number = request.form.get('number')
        course = request.form.get('course')
        # insert book into database
        c.execute("INSERT INTO books (year,title, author, course,id,number) VALUES (?, ?, ?, ?, ?, ?)",
                  (year, title, author,course, id, number))
        conn.commit()
        return redirect(url_for('home'))
    else:
        return render_template('addbook.html')


# run Flask app
if __name__ == '__main__':
    app.run(debug=True)
