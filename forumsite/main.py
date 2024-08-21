from flask import Flask, render_template, redirect, request, flash, session
import pymysql.cursors
import random as rd

db = pymysql.connect(host='localhost',
                     user='root',
                     password='1234',
                     db='forum',
                     charset='utf8mb4',
                     cursorclass=pymysql.cursors.DictCursor)

con = db.cursor()

app = Flask(__name__)
app.config['SECRET_KEY'] = str(rd.randint(0, 9999999999999))
auth = False

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login_backend', methods = ['POST'])
def login_backend():
    global auth
    global username
    global password
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        con.execute('SELECT user_id, username, password FROM forum_user WHERE username = %s AND password = %s', (username, password))
        users = con.fetchall()
        db.commit()

        for user in users:
            name = user['username']
            passwd = user['password']

        if username == name and password == passwd:
            auth = True
            session['username'] = username  # Store username in the session
            return redirect('/main')

@app.route('/main')
def index():
    global auth
    if 'username' in session:  # Eğer oturumda kullanıcı adı varsa
        con.execute('SELECT * FROM forums')
        forums = con.fetchall()
        return render_template('index.html', forums=forums)
    else:
        return redirect('/')



@app.route('/<forum_id>')
def forum(forum_id):
    global auth
    if auth == True:
        con.execute('SELECT forum_title, forum_include, forum_id FROM forums WHERE forum_id = %s', (forum_id,))
        forum_includee = con.fetchall()
        con.execute('SELECT reply_include, replier FROM replies WHERE forum_id = %s',(forum_id))
        forum_replies = con.fetchall()
        return render_template('include.html', forum_includee=forum_includee, forum_replies=forum_replies)
    else:
        errTitle = 'KULLANICI KAYNAKLI HATA'
        errDescription = 'Özelliklerden yararlanmak için giriş yapmanız gerekli'
        buttonLink = '/'
        buttonContent = 'GİRİŞ YAP'
        return render_template('error_page.html', errTitle=errTitle, errDescription = errDescription, buttonLink=buttonLink, buttonContent=buttonContent)

@app.route('/reply', methods = ['POST'])
def reply():
    if request.method == 'POST':
        forum_idd = request.form.get('forum_id')
        replier = request.form.get('replier')
        reply_content = request.form.get('reply')
        reply_id = rd.randint(0, 99999999)
        con.execute('INSERT INTO replies VALUES(%s, %s, %s, %s)',(int(reply_id), reply_content, replier,forum_idd))
        db.commit()

        return redirect(f'/{forum_idd}')
    
@app.route('/add_forumf')
def frontend():
    global auth
    if auth == True:
        return render_template('add_forum.html')
    else:
        errTitle = 'KULLANICI KAYNAKLI HATA'
        errDescription = 'Özelliklerden yararlanmak için giriş yapmanız gerekli'
        buttonLink = '/'
        buttonContent = 'GİRİŞ YAP'
        return render_template('error_page.html', errTitle=errTitle, errDescription = errDescription, buttonLink=buttonLink, buttonContent=buttonContent)

@app.route('/add_forum', methods = ['POST'])
def add():
    if request.method == 'POST':
        f_title = request.form.get('forum_title')
        f_include = request.form.get('forum_include')
        f_category = request.form.get('kategori')
        f_id = rd.randint(0, 99999999)

        con.execute('INSERT INTO forums VALUES(%s, %s, %s, %s)',(f_id, f_title, f_include, f_category))
        db.commit()

        return redirect(f'/{f_id}')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register_backend', methods = ['POST'])
def register_backend():
    global auth
    if request.method == 'POST':
        try:
            reg_username = request.form.get('reg_username')
            reg_password = request.form.get('reg_password')
            reg_id = rd.randint(0, 99999999)

            con.execute('INSERT INTO forum_user VALUES(%s, %s, %s)',(reg_id, reg_username, reg_password))
            db.commit()

            return redirect('/')
        except:
            errTitle = 'alForum KAYNAKLI HATA'
            errDescription = 'Sunucularımızdaki sorundan dolayı özür dileriz.'
            buttonLink = '/register'
            buttonContent = 'TEKRAR DENE'
            return render_template('error_page.html', errTitle=errTitle, errDescription=errDescription, buttonLink=buttonLink, buttonContent=buttonContent)

@app.route('/user')
def user():
    global auth
    con.execute('SELECT username, user_id, password FROM forum_user WHERE username = %s AND password = %s',(username, password))
    infos = con.fetchall()
    db.commit()
    return render_template('user.html', infos=infos) 
    
@app.route('/redirectCategory', methods = ['POST'])
def redirectToCategory():
    if request.method == 'POST':
        kategoriler = request.form.get('kategoriler')

        return redirect(kategoriler)
    else:
        errTitle = 'KULLANICI KAYNAKLI HATA'
        errDescription = 'Özelliklerden yararlanmak için giriş yapmanız gerekli'
        buttonLink = '/'
        buttonContent = 'GİRİŞ YAP'
        return render_template('error_page.html', errTitle=errTitle, errDescription = errDescription, buttonLink=buttonLink, buttonContent=buttonContent)

@app.route('/veribilimi')
def veribilimi():
    global auth
    if auth == True:
        con.execute('SELECT forum_title, forum_include, forum_id FROM forums WHERE forum_category = %s',('/veribilimi'))
        forums = con.fetchall()
        return render_template('index.html', forums=forums)
    else:
        errTitle = 'KULLANICI KAYNAKLI HATA'
        errDescription = 'Özelliklerden yararlanmak için giriş yapmanız gerekli'
        buttonLink = '/'
        buttonContent = 'GİRİŞ YAP'
        return render_template('error_page.html', errTitle=errTitle, errDescription = errDescription, buttonLink=buttonLink, buttonContent=buttonContent)

@app.route('/donanim')
def donanim():
    global auth
    if auth == True:
        con.execute('SELECT forum_title, forum_include, forum_id FROM forums WHERE forum_category = %s',('/donanim'))
        forums = con.fetchall()
        return render_template('index.html', forums = forums)
    else:
        errTitle = 'KULLANICI KAYNAKLI HATA'
        errDescription = 'Özelliklerden yararlanmak için giriş yapmanız gerekli'
        buttonLink = '/'
        buttonContent = 'GİRİŞ YAP'
        return render_template('error_page.html', errTitle=errTitle, errDescription = errDescription, buttonLink=buttonLink, buttonContent=buttonContent)

@app.route('/yazilim')
def yazilim():
    global auth
    if auth == True:
        con.execute('SELECT forum_title, forum_include, forum_id FROM forums WHERE forum_category = %s',('/yazilim'))
        forums = con.fetchall()
        return render_template('index.html', forums = forums)
    else:
        errTitle = 'KULLANICI KAYNAKLI HATA'
        errDescription = 'Özelliklerden yararlanmak için giriş yapmanız gerekli'
        buttonLink = '/'
        buttonContent = 'GİRİŞ YAP'
        return render_template('error_page.html', errTitle=errTitle, errDescription = errDescription, buttonLink=buttonLink, buttonContent=buttonContent)

@app.route('/etikhacking')
def etikhacking():
    global auth
    if auth == True:
        con.execute('SELECT forum_title, forum_include, forum_id FROM forums WHERE forum_category = %s',('/etikhacking'))
        forums = con.fetchall()
        return render_template('index.html', forums = forums)
    else:
        errTitle = 'KULLANICI KAYNAKLI HATA'
        errDescription = 'Özelliklerden yararlanmak için giriş yapmanız gerekli'
        buttonLink = '/'
        buttonContent = 'GİRİŞ YAP'
        return render_template('error_page.html', errTitle=errTitle, errDescription = errDescription, buttonLink=buttonLink, buttonContent=buttonContent)

@app.route('/android')
def android():
    global auth
    if auth == True:
        con.execute('SELECT forum_title, forum_include, forum_id FROM forums WHERE forum_category = %s',('/android'))
        forums = con.fetchall()
        return render_template('index.html', forums = forums)
    else:
        errTitle = 'KULLANICI KAYNAKLI HATA'
        errDescription = 'Özelliklerden yararlanmak için giriş yapmanız gerekli'
        buttonLink = '/'
        buttonContent = 'GİRİŞ YAP'
        return render_template('error_page.html', errTitle=errTitle, errDescription = errDescription, buttonLink=buttonLink, buttonContent=buttonContent)

@app.route('/ios')
def ios():
    global auth
    if auth == True:
        con.execute('SELECT forum_title, forum_include, forum_id FROM forums WHERE forum_category = %s',('/ios'))
        forums = con.fetchall()
        return render_template('index.html', forums = forums)
    else:
        errTitle = 'KULLANICI KAYNAKLI HATA'
        errDescription = 'Özelliklerden yararlanmak için giriş yapmanız gerekli'
        buttonLink = '/'
        buttonContent = 'GİRİŞ YAP'
        return render_template('error_page.html', errTitle=errTitle, errDescription = errDescription, buttonLink=buttonLink, buttonContent=buttonContent)

@app.route('/linux')
def linux():
    global auth
    if auth == True:
        con.execute('SELECT forum_title, forum_include, forum_id FROM forums WHERE forum_category = %s',('/linux'))
        forums = con.fetchall()
        return render_template('index.html', forums = forums)
    else:
        errTitle = 'KULLANICI KAYNAKLI HATA'
        errDescription = 'Özelliklerden yararlanmak için giriş yapmanız gerekli'
        buttonLink = '/'
        buttonContent = 'GİRİŞ YAP'
        return render_template('error_page.html', errTitle=errTitle, errDescription = errDescription, buttonLink=buttonLink, buttonContent=buttonContent)

@app.route('/windows')
def windows():
    global auth
    if auth == True:
        con.execute('SELECT forum_title, forum_include, forum_id FROM forums WHERE forum_category = %s',('/windows'))
        forums = con.fetchall()
        return render_template('index.html', forums = forums)
    else:
        errTitle = 'KULLANICI KAYNAKLI HATA'
        errDescription = 'Özelliklerden yararlanmak için giriş yapmanız gerekli'
        buttonLink = '/'
        buttonContent = 'GİRİŞ YAP'
        return render_template('error_page.html', errTitle=errTitle, errDescription = errDescription, buttonLink=buttonLink, buttonContent=buttonContent)
    

if __name__ == '__main__':
    app.run(debug=True)
