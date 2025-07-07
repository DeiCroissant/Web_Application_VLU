from flask import Flask, render_template

# Initialize the Flask application
app = Flask(__name__)

@app.route('/')
def Hi():
    return render_template('Ex2.html')


if __name__ == '__main__':
    app.run(debug=True)