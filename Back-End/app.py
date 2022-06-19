from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from mysql.connector import connect
from bcrypt import hashpw, gensalt, checkpw
from time import strftime

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = '*********'

db = connect(host = 'localhost', user = 'root', database = 'morse')

@app.route('/')
def main():
    if 'status' in session.keys(): return render_template('home.html')

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
        data = request.form

        csr = db.cursor(dictionary = True)
        csr.execute('SELECT * FROM user WHERE username = %s', (data['username'],))
        data_user = csr.fetchone()
        csr.close()

        if data is not None:
            if checkpw(data['password'].encode('UTF-8'), data_user['password']):
                del data
                session['status'] = True
                session['role'] = data_user['status']
                session['nama'] = data_user['nama']
                session['gender'] = data_user['gender']
                session['username'] = data_user['username']
                del data_user

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
        data = request.form
        data['password'] = hashpw(data['password'].encode('UTF-8'), gensalt())

        csr = db.cursor()
        try:
            csr.execute('INSERT INTO user (nama, gender, username, password) VALUES (%s, %s, %s, %s)', (data['nama'], data['gender'], data['username'], data['password']))
            db.commit()
            del data
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
        if session['status'] and session['role'] == 'admin': return render_template('kelola_user.html')

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
                data = request.form

                csr = db.cursor()
                try:
                    csr.execute('UPDATE user SET nama = %s, gender = %s, username = %s WHERE id = %s', (data['nama'], data['gender'], data['username'], id))
                    db.commit()
                    del data
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

@app.route('/data_riwayat')
def data_riwayat():
    csr = db.cursor(dictionary = True)
    csr.execute('SELECT * FROM riwayat WHERE username = %s ORDER BY id DESC', (session['username'],))
    data = jsonify(csr.fetchall())
    csr.close()

    data.headers.add('Access-Control-Allow-Origin', '*')
    data.headers.add('Access-Control-Allow-Methods', 'GET')

    return data

@app.route('/riwayat')
def riwayat():
    if 'status' in session.keys(): return render_template('riwayat_terjemahan.html')

    return redirect(url_for('login'))

def tambah_riwayat(username, bentuk_awal, terjemahan):
    csr = db.cursor()
    csr.execute('INSERT INTO riwayat (username, `bentuk awal`, terjemahan, waktu) VALUES (%s,%s,%s,%s)', (username, bentuk_awal, terjemahan, strftime('%Y-%m-%d %H:%M:%S')))
    db.commit()
    csr.close()

    return True

@app.route('/hapus_riwayat/<int:id>')
def hapus_riwayat(id):
    if 'status' in session.keys():
        csr = db.cursor()
        if not id: csr.execute('DELETE FROM riwayat WHERE username = %s', (session['username'],))
        else: csr.execute('DELETE FROM riwayat WHERE id = %s AND username = %s', (id, session['username']))
        db.commit()
        csr.close()
        flash('Riwayat berhasil dihapus', 'success')

        return redirect(url_for('riwayat'))
    return redirect(url_for('login'))

@app.route('/latin')
def terjemahan_kalimat():
    button = {}
    if 'status' in session.keys(): button['class'], button['function'], button['teks'] = 'danger', 'logout("/logout")', 'Logout'
    else: button['class'], button['function'], button['teks'] = 'info', 'login("/login")', 'Login'
    
    return render_template('latin.html', button = button)

@app.route('/terjemah_latin')
def terjemah_kalimat():
    data = request.args.get
    username, kalimat = data('username'), data('latin')
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

    status = tambah_riwayat(username, kalimat, arti) if username else False

    hasil = jsonify(dict(latin = kalimat, terjemahan = arti, status = status))
    hasil.headers.add('Access-Control-Allow-Origin', '*')
    hasil.headers.add('Access-Control-Allow-Methods', 'GET')

    return hasil

@app.route('/kode_morse')
def terjemahan_kode():
    button = {}
    if 'status' in session.keys(): button['class'], button['function'], button['teks'] = 'danger', 'logout("/logout")', 'Logout'
    else: button['class'], button['function'], button['teks'] = 'info', 'login("/login")', 'Login'
   
    return render_template('kode_morse.html', button = button)

@app.route('/terjemah_kode')
def terjemah_kode():
    data = request.args.get
    username, morse = data('username'), data('kode')
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

    status = tambah_riwayat(username, morse, arti) if username else False

    hasil = jsonify(dict(kode_morse = morse, terjemahan = arti, status = status))
    hasil.headers.add('Access-Control-Allow-Origin', '*')
    hasil.headers.add('Access-Control-Allow-Methods', 'GET')

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
    
if __name__ == '__main__':
    app.run()
    db.close()