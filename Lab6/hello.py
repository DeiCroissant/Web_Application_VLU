from flask import Flask, render_template

#Initialize the Flask application
app = Flask(__name__)

@app.route('/')

def hello_world():
    return render_template('hello.html')

@app.route('/about')
def about():
    return render_template('Ex2.html')

if __name__ == '__main__':
    app.run(debug=True)