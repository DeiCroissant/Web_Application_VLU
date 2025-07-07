from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)
# Configuration for file upload
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def file_upload():
    return render_template('newfile.html')


@app.route('/uploader', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # get the file from the form
        f = request.files['file']

        #use secure_filename to secure the filename
        filename = secure_filename(f.filename)

        # save the file to the upload folder
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        return f'File: {filename} uploaded successfully!'
if __name__ == '__main__':
    app.run(debug=True)


