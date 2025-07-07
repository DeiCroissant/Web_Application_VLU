from flask import Flask,render_template ,request
app = Flask(__name__)
#route 1 display the form
@app.route('/')
def show_from():
    return render_template('Ex3.html')
 
#route 2 receive the form data
@app.route('/submit', methods=['POST'])
def submit_form():
    # use request.form to get the data from input name="name"
    name = request.form.get('name')
    # render template success.html and pass the name variable
    return render_template('success.html', name=name)

if __name__ == '__main__':
    app.run(debug=True)
        
    