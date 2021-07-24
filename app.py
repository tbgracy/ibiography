# COMMENT THIS DAMN CODE !!!
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename, redirect
# from flask_sqlalchemy import SQLAlchemy
import sqlite3
import markdown

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database'
# db = SQLAlchemy(app)
# db = sqlite3.connect('database')
# cur = db.cursor()
def queryExecution(database, query, datas):
    db = sqlite3.connect(database)
    cur = db.cursor()
    cur.execute(query, datas)
    db.commit()
    return cur.fetchall()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/archives/<string:section>')
def archives(section):
    status = ['', '', '']
    pays = []

    if section == 'alphabet':
        status[0] = 'onglet-actif'
        results = queryExecution('database.db', """
            SELECT fullname, id, short_description, pictureUrl FROM personnage 
            ORDER BY 1 
        """, ())
        # results.sort()
        # results.append()
        # for result in results:
        #     result.append('')
    elif section == 'thematique':
        status[1] = 'onglet-actif'
        results = []
    elif section == 'pays':
        # results = []
        results = queryExecution('database.db', """
            SELECT fullname, id, short_description, pictureUrl, nationality
            FROM personnage ORDER BY 1
        """, ())
        for result in results:
            if result[4] not in pays: 
                pays.append(result[4])
                print(result[4])
        # pays.sort()
        status[2] = 'onglet-actif'
    return render_template('archives.html', section=section, status=status, results=results, pays=pays)

@app.route('/add', methods=['POST', 'GET'])
def ajouter():
    if request.method == 'POST':
        db = sqlite3.connect('database.db')
        cur = db.cursor()

        fullname = request.form['fullname']
        nationality = request.form['nationality']
        long_bio = markdown.markdown(request.form['long_bio'])
        # long_bio = request.form['long_bio']
        short_description = request.form['short_description']
        birthdate = request.form['birthdate']
        deathdate = request.form['deathdate']
        p = request.files['picture']
        pictureUrl = secure_filename(p.filename) 
        p.save('static/images/' + pictureUrl)
        father = request.form['father']
        mother = request.form['mother']
        website = request.form['website']

        biography_data = (fullname, nationality, long_bio, short_description, birthdate, deathdate, pictureUrl, father, mother, website)
        biography_columns = '(fullname, nationality, long_bio, short_description, birthdate, deathdate, pictureUrl, father, mother, website)'
        placeholders = '(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'

        cur.execute(f'INSERT INTO personnage {biography_columns} VALUES {placeholders}',
                    biography_data)

        cur.close()
        db.commit()
        db.close()
        return redirect('/')

    return render_template('new_bio.html')

@app.route('/biography/<int:id>')
def biography(id):

    query = "SELECT * FROM personnage where id = ?"
    results = queryExecution('database.db', query, (id,))
    # db = sqlite3.connect('database.db')
    # cur = db.cursor()
    # cur.execute(query, (id,))
    # db.commit()
    # results = cur.fetchall()

    return render_template('biography.html', results=results)

if __name__ == "__main__":
    app.run(debug="True")