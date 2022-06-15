from flask import Flask, jsonify, render_template, request
from mysql.connector import connect

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = '********'

db = connect(host = 'localhost', user = 'root', database = 'morse')

@app.route('/latin')
def terjemahan_kalimat(): return render_template('latin.html')

@app.route('/kode_morse')
def terjemahan_kode(): return render_template('kode_morse.html')

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
        kode.append(data[0]) if data is not None else kode.append('#')
        csr.close()

    arti = '\\'.join(kode)
 
    hasil = jsonify(dict(latin = kalimat, terjemahan = arti))
    hasil.headers.add('Access-Control-Allow-Origin', '*')
    hasil.headers.add('Access-Control-Allow-Methods', 'GET')

    return hasil

@app.route('/terjemah_kode')
def terjemah_kode():
    kode_morse = request.args.get('kode')
    cek_kode_morse = kode_morse.replace('.', '').replace('-', '').replace('\\', '')
    if  cek_kode_morse == '':
        kode_morse = kode_morse.split('\\')
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

    return hasil

@app.route('/')
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