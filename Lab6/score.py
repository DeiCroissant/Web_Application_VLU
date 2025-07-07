from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def show_form():
    return render_template('ScoreForm.html')

@app.route('/submitScore', methods=['POST'])
def submit_score():
    # Get the score from the form
    result_data = request.form
    return render_template('ScoreResult.html', result=result_data)
if __name__ == '__main__':
    app.run(debug=True)
