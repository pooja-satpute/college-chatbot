from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

def get_db():
    return sqlite3.connect('college.db')


# LOGIN
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        if request.form['username']=="admin" and request.form['password']=="admin123":
            session['admin']=True
            return redirect('/admin')
        else:
            return "Invalid Login"
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('admin',None)
    return redirect('/login')
@app.route('/')
def home():
    return redirect('/login')


# DASHBOARD
@app.route('/admin')
def admin():
    if 'admin' not in session:
        return redirect('/login')

    conn=get_db()
    cur=conn.cursor()

    cur.execute("SELECT * FROM faq")
    faq=cur.fetchall()

    cur.execute("SELECT * FROM courses")
    courses=cur.fetchall()

    cur.execute("SELECT * FROM scholarships")
    scholarships=cur.fetchall()

    conn.close()

    return render_template('admin.html',faq=faq,courses=courses,scholarships=scholarships)


# ADD FAQ
@app.route('/add',methods=['POST'])
def add():
    q=request.form['question']
    a=request.form['answer']
    conn=get_db()
    cur=conn.cursor()
    cur.execute("INSERT INTO faq(question,answer) VALUES(?,?)",(q,a))
    conn.commit()
    conn.close()
    return redirect('/admin')


# DELETE FAQ
@app.route('/delete/<int:id>')
def delete(id):
    conn=get_db()
    cur=conn.cursor()
    cur.execute("DELETE FROM faq WHERE id=?",(id,))
    conn.commit()
    conn.close()
    return redirect('/admin')


# EDIT FAQ
@app.route('/edit/<int:id>',methods=['GET','POST'])
def edit(id):
    conn=get_db()
    cur=conn.cursor()

    if request.method=='POST':
        q=request.form['question']
        a=request.form['answer']
        cur.execute("UPDATE faq SET question=?,answer=? WHERE id=?",(q,a,id))
        conn.commit()
        conn.close()
        return redirect('/admin')

    cur.execute("SELECT * FROM faq WHERE id=?",(id,))
    data=cur.fetchone()
    conn.close()
    return render_template('edit.html',data=data)


# ADD COURSE
@app.route('/add_course',methods=['POST'])
def add_course():
    name=request.form['name']
    eligibility=request.form['eligibility']
    fees=request.form['fees']
    duration=request.form['duration']

    conn=get_db()
    cur=conn.cursor()
    cur.execute("INSERT INTO courses(name,eligibility,fees,duration) VALUES(?,?,?,?)",
                (name,eligibility,fees,duration))
    conn.commit()
    conn.close()
    return redirect('/admin')


# ADD SCHOLARSHIP
@app.route('/add_scholarship',methods=['POST'])
def add_scholarship():
    name=request.form['name']
    details=request.form['details']

    conn=get_db()
    cur=conn.cursor()
    cur.execute("INSERT INTO scholarships(name,details) VALUES(?,?)",(name,details))
    conn.commit()
    conn.close()
    return redirect('/admin')
@app.route('/edit_course/<int:id>', methods=['GET', 'POST'])
def edit_course(id):
    if 'admin' not in session:
        return redirect('/login')

    conn = get_db()
    cur = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        eligibility = request.form['eligibility']
        fees = request.form['fees']
        duration = request.form['duration']

        cur.execute("""
            UPDATE courses 
            SET name=?, eligibility=?, fees=?, duration=? 
            WHERE id=?
        """, (name, eligibility, fees, duration, id))

        conn.commit()
        conn.close()
        return redirect('/admin')

    cur.execute("SELECT * FROM courses WHERE id=?", (id,))
    data = cur.fetchone()
    conn.close()

    return render_template('edit_course.html', data=data)
@app.route('/delete_course/<int:id>')
def delete_course(id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("DELETE FROM courses WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect('/admin')
@app.route('/edit_scholarship/<int:id>', methods=['GET', 'POST'])
def edit_scholarship(id):
    if 'admin' not in session:
        return redirect('/login')

    conn = get_db()
    cur = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        details = request.form['details']

        cur.execute("""
            UPDATE scholarships 
            SET name=?, details=? 
            WHERE id=?
        """, (name, details, id))

        conn.commit()
        conn.close()
        return redirect('/admin')

    cur.execute("SELECT * FROM scholarships WHERE id=?", (id,))
    data = cur.fetchone()
    conn.close()

    return render_template('edit_scholarship.html', data=data)
@app.route('/delete_scholarship/<int:id>')
def delete_scholarship(id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("DELETE FROM scholarships WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect('/admin')


if __name__ == "__main__":
    app.run(debug=True,port=5001)