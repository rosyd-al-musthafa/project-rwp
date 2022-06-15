from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from mysql.connector import connect
from bcrypt import hashpw, gensalt, checkpw
from time import strftime

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = '********'

db = connect(host = 'localhost', user = 'root', database = 'morse')

@app.route('/')
def main():
    if 'status' in session.keys():
        page = 'home'
        if session['role'] == 'admin': page += '_admin'

        return render_template(page + '.html', gender = session['gender'])
    return redirect(url_for('login'))

@app.route('/info')
def info():
    data = jsonify(dict(nama = session['nama']))
    data.headers.add('Access-Control-Allow-Origin', '*')
    data.headers.add('Access-Control-Allow-Methods', 'GET')

    return data

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        csr = db.cursor(dictionary = True)
        csr.execute('SELECT * FROM user WHERE username = %s', (username,))
        data = csr.fetchone()
        csr.close()

        if data is not None:
            if checkpw(password.encode('UTF-8'), data['password']):
                session['status'] = True
                session['role'] = data['status']
                session['nama'] = data['nama']
                session['gender'] = data['gender']
                session['username'] = data['username']

                return redirect(url_for('main'))
            else: flash('Password salah', 'danger')
        else: flash('Username tidak ditemukan', 'danger')
        return redirect(url_for('login'))
    
    if 'status' in session.keys(): return redirect(url_for('main'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Anda berhasil logout', 'warning')
    return redirect(url_for('login'))

@app.route('/register', methods = ['POST', 'GET'])
def register():
    if request.method == 'POST':
        nama = request.form['nama']
        gender = request.form['gender']
        username = request.form['username']
        password = hashpw(request.form['password'].encode('UTF-8'), gensalt())

        csr = db.cursor()
        try:
            csr.execute('INSERT INTO user (nama, gender, username, password) VALUES (%s, %s, %s, %s)', (nama, gender, username, password))
            db.commit()
        except: status = False
        else: status = True
        csr.close()

        if status: flash('Register berhasil', 'success')
        else: flash('Register gagal', 'danger')

        return redirect(url_for('login'))

    return render_template('registrasi.html')

@app.route('/kelola_user')
def kelola_user():
    if 'status' in session.keys():
        if session['status'] and session['role'] == 'admin':
            return render_template('kelola_user.html')

    return redirect(url_for('login'))

@app.route('/read_user')
def read_user():
    if 'status' in session.keys():
        if session['status'] and session['role'] == 'admin':
            csr = db.cursor(dictionary = True)
            csr.execute("SELECT id, nama, gender, username FROM user WHERE status = 'client'")
            data = csr.fetchall()
            for data0 in data: data0['gender'] = 'Laki-laki' if data0['gender'] == 'L' else 'Perempuan'
            data = jsonify(data)
            csr.close()

            data.headers.add('Access-Control-Allow-Origin', '*')
            data.headers.add('Access-Control-Allow-Methods', 'GET')

            return data
    return redirect(url_for('login'))

@app.route('/update_user/<int:id>', methods = ['GET', 'POST'])
def update_user(id):
    if 'status' in session.keys():
        if session['status'] and session['role'] == 'admin':
            if request.method == 'POST':
                nama = request.form['nama']
                gender = request.form['gender']
                username = request.form['username']

                csr = db.cursor()
                try:
                    csr.execute('UPDATE user SET nama = %s, gender = %s, username = %s WHERE id = %s', (nama, gender, username, id))
                    db.commit()
                except: status = False
                else: status = True
                csr.close()

                if status: flash('Data user berhasil diubah', 'success')
                else: flash('Data user gagal diubah', 'danger')

                return redirect(url_for('kelola_user'))

            csr = db.cursor(dictionary = True)
            csr.execute("SELECT nama, gender, username FROM user WHERE id = %s", (id,))
            data = csr.fetchone()
            csr.close()

            return render_template('update_user.html', data = data, id = id)
    return redirect(url_for('login'))

@app.route('/hapus_user/<int:id>')
def hapus_user(id):
    if 'status' in session.keys():
        if session['status'] and session['role'] == 'admin':
            csr = db.cursor()
            csr.execute(f'DELETE FROM user WHERE id = {id}')
            db.commit()
            csr.close()
            flash('Data user berhasil dihapus', 'success')

            return redirect(url_for('kelola_user'))
    return redirect(url_for('login'))

@app.route('/lihat_riwayat')
def lihat_riwayat():
    if 'status' in session.keys():
        if session['status'] and session['role'] == 'admin': return redirect(url_for('kelola_riwayat'))
    return render_template('riwayat.html')

@app.route('/riwayat')
def riwayat():
    csr = db.cursor(dictionary = True)
    csr.execute('SELECT * FROM riwayat ORDER BY id DESC')
    data = jsonify(csr.fetchall())
    csr.close()

    data.headers.add('Access-Control-Allow-Origin', '*')
    data.headers.add('Access-Control-Allow-Methods', 'GET')

    return data

@app.route('/kelola_riwayat')
def kelola_riwayat():
    if 'status' in session.keys():
        if session['status'] and session['role'] == 'admin': return render_template('kelola_riwayat.html')

    return redirect(url_for('login'))

@app.route('/hapus_riwayat/<int:id>')
def hapus_riwayat(id):
    if 'status' in session.keys():
        if session['status'] and session['role'] == 'admin':
            csr = db.cursor()
            if not id: csr.execute('DELETE FROM riwayat')
            else: csr.execute(f'DELETE FROM riwayat WHERE {id = }')
            db.commit()
            csr.close()
            flash('Riwayat berhasil dihapus', 'success')

            return redirect(url_for('kelola_riwayat'))
    return redirect(url_for('login'))

@app.route('/latin')
def terjemahan_kalimat(): return render_template('latin.html')

@app.route('/terjemah_latin')
def terjemah_kalimat():
    kalimat = request.args.get('latin')
    huruf, kode = [], []

    for i in range(len(kalimat)):
        huruf.append(kalimat[i])

    for i in huruf:
        if i == ' ':
            kode.append('')
            continue

        csr = db.cursor()
        csr.execute('SELECT Kode FROM kode_morse WHERE Karakter = %s', (i,))
        data = csr.fetchone()
        csr.close()
        kode.append(data[0]) if data is not None else kode.append('#')

    arti = '\\'.join(kode)
 
    hasil = jsonify(dict(latin = kalimat, terjemahan = arti))
    hasil.headers.add('Access-Control-Allow-Origin', '*')
    hasil.headers.add('Access-Control-Allow-Methods', 'GET')

    csr = db.cursor()
    csr.execute('INSERT INTO riwayat (`bentuk awal`, terjemahan, waktu) VALUES (%s, %s, %s)', (kalimat, arti, strftime('%Y-%m-%d %H:%M:%S')))
    db.commit()
    csr.close()

    return hasil

@app.route('/kode_morse')
def terjemahan_kode(): return render_template('kode_morse.html')

@app.route('/terjemah_kode')
def terjemah_kode():
    morse = request.args.get('kode')
    cek_kode_morse = morse.replace('.', '').replace('-', '').replace('\\', '')
    if  cek_kode_morse == '':
        kode_morse = morse.split('\\')
        kode, huruf = [], []

        for i in kode_morse:
            kode.append(i)
        
        for i in kode:
            if i == '':
                huruf.append(' ')
                continue
            
            csr = db.cursor()
            csr.execute('SELECT Karakter FROM kode_morse WHERE Kode = %s', (i,))
            data = csr.fetchone()
            huruf.append(data[0]) if data is not None else huruf.append('#')
            csr.close()
        
        arti = ''.join(huruf)

    else: arti = 'Gagal menerjemahkan karena terdapat karakter:\n' + ''.join(sorted(set([cek_kode_morse[i] for i in range(len(cek_kode_morse))])))

    hasil = jsonify(dict(kode_morse = '\\'.join(kode_morse), terjemahan = arti))
    hasil.headers.add('Access-Control-Allow-Origin', '*')
    hasil.headers.add('Access-Control-Allow-Methods', 'GET')

    csr = db.cursor()
    csr.execute('INSERT INTO riwayat (`bentuk awal`, terjemahan, waktu) VALUES (%s, %s, %s)', (morse, arti, strftime('%Y-%m-%d %H:%M:%S')))
    db.commit()
    csr.close()

    return hasil

@app.route('/api')
def api():
    csr = db.cursor(dictionary = True)
    csr.execute('SELECT * FROM kode_morse LIMIT 26')
    data0 = csr.fetchall()
    csr.execute('SELECT * FROM kode_morse LIMIT 10 OFFSET 26')
    data1 = csr.fetchall()
    csr.execute('SELECT * FROM kode_morse LIMIT 18 OFFSET 36')
    data2 = csr.fetchall()
    csr.close()

    api = jsonify(dict(data = dict(huruf = data0, angka = data1, simbol = data2)))
    api.headers.add('Access-Control-Allow-Origin', '*')
    api.headers.add('Access-Control-Allow-Methods', 'GET')
    
    return api
    
if __name__ == '__main__': app.run()