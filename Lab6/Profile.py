from flask import Flask, render_template

app = Flask(__name__)

# Route động: <username> là một biến sẽ nhận giá trị từ URL
@app.route('/profile/<username>')
def profile(username):
    # Render file profile.html và truyền biến 'username' vào cho template
    return render_template('Profile.html', username=username)

if __name__ == '__main__':
    app.run(debug=True)