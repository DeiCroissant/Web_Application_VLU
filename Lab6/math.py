from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def calculate_form():
    return render_template('MathPage.html')
@app.route('/calculate', methods=['POST'])
def calculate():
    # Get the number from the form
    num = int(request.form['number'])
    # Calcute the square
    square = num * num
    return render_template('MathResult.html', number=num, square=square)
if __name__ == '__main__':
    app.run(debug=True)