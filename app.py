from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Database connection
db = mysql.connector.connect(
    host = "xhias.h.filess.io",
    database= "dbflask_everything",
    port = "3305",
    username = "dbflask_everything",
    password = "651ceedad3c48f5b99d184e61da718b78c90b5d4"
)

# Home page
@app.route('/')
def index():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM mahasiswa")
    mahasiswa = cursor.fetchall()
    return render_template('index.html', mahasiswa=mahasiswa)

# Add data
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        nim = request.form['nim']
        nama = request.form['nama']
        asal = request.form['asal']
        cursor = db.cursor()
        cursor.execute("INSERT INTO mahasiswa (nim, nama, asal) VALUES (%s, %s, %s)", (nim, nama, asal))
        db.commit()
        return redirect(url_for('index'))
    return render_template('add.html')

# Edit data
@app.route('/edit/<old_nim>', methods=['GET', 'POST'])
def edit(old_nim):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM mahasiswa WHERE nim = %s", (old_nim,))
    mahasiswa = cursor.fetchone()
    
    if request.method == 'POST':
        new_nim = request.form['nim']
        nama = request.form['nama']
        asal = request.form['asal']
        cursor = db.cursor()
        cursor.execute("UPDATE mahasiswa SET nim = %s, nama = %s, asal = %s WHERE nim = %s", 
                      (new_nim, nama, asal, old_nim))
        db.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', mahasiswa=mahasiswa)

# Delete data
@app.route('/delete/<nim>')
def delete(nim):
    cursor = db.cursor()
    cursor.execute("DELETE FROM mahasiswa WHERE nim = %s", (nim,))
    db.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)