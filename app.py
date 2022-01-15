#

# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2  # pip install psycopg2
import psycopg2.extras

app = Flask(__name__)
app.secret_key = "cairocoders-ednalan"

DB_HOST = "localhost"
DB_NAME = "sampledb"
DB_USER = "postgres"
DB_PASS = "12345"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER,
                        password=DB_PASS, host=DB_HOST)


@app.route('/')
def homepage():
    return render_template('homepage.html')


@app.route('/donate')
def donate():
    return render_template('donate.html')


@app.route('/index')
def Index():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT * FROM donor_details"
    cur.execute(s)  # Execute the SQL
    list_users = cur.fetchall()
    return render_template('index.html', list_users=list_users)


@app.route('/adminadd')
def adminadd():
    return render_template('adminAdd.html')


@app.route('/add_donor', methods=['POST'])
def add_donor():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        bType = request.form['btype']
        email = request.form['email']
        date = request.form['date']
        cur.execute(
            "INSERT INTO donor_details (donor_fname, donor_lname, donor_blood_type, donor_email, donor_donate_date) VALUES (%s,%s,%s,%s,%s)", (fname, lname, bType, email, date))
        conn.commit()
        flash('Donation Added Successfully.    Thank you for Donating!!')
        return redirect(url_for('donate'))


@app.route('/add_donor_admin', methods=['POST'])
def add_donor_admin():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        bType = request.form['btype']
        email = request.form['email']
        date = request.form['date']
        cur.execute(
            "INSERT INTO donor_details (donor_fname, donor_lname, donor_blood_type, donor_email, donor_donate_date) VALUES (%s,%s,%s,%s,%s)", (fname, lname, bType, email, date))
        conn.commit()
        flash('Donor Added successfully')

        return redirect(url_for('Index'))


@app.route('/edit/<donor_id>', methods=['POST', 'GET'])
def get_employee(donor_id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute('SELECT * FROM donor_details WHERE donor_id = %s', (donor_id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit.html', student=data[0])


@app.route('/update/<donor_id>', methods=['POST'])
def update_student(donor_id):
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        bType = request.form['btype']
        email = request.form['email']
        date = request.form['date']

        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("""
            UPDATE donor_details
            SET donor_fname = %s,
                donor_lname = %s,
                donor_blood_type = %s,
                donor_email = %s,
                donor_donate_date = %s
            WHERE donor_id = %s
        """, (fname, lname, bType, email, date,  donor_id))
        flash('Donor Updated Successfully')
        conn.commit()
        return redirect(url_for('Index'))


@app.route('/delete/<string:donor_id>', methods=['POST', 'GET'])
def delete_student(donor_id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute(
        'DELETE FROM donor_details WHERE donor_id = {0}'.format(donor_id))
    conn.commit()
    flash('Donor Removed Successfully')
    return redirect(url_for('Index'))


if __name__ == "__main__":
    app.run(debug=True)
    
