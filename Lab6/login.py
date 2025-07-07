from flask import Flask, render_template, request, session, redirect

app = Flask(__name__)
app.secret_key = 'uaisudauwiugbascmm,znc@!'
users = {'admin' : 'secret'} # store user data

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect('/dashboard')
        return 'Invalid credentials'
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/login')
    return 'Logged in succesfully'

if __name__ == '__main__':
    app.run(debug=True)