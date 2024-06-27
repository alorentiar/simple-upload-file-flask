from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired

from flask import Flask, jsonify, request
import json,logging,time

from datetime import date

app = Flask(__name__)
app.config['SECRET_KEY'] = 'verysecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'



class UploadFileForm(FlaskForm):
    file = FileField("File",validators=[InputRequired()])
    submit = SubmitField("Upload File")

@app.route('/',methods=['GET','POST'])
@app.route('/home', methods=['GET','POST'])

def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))) #save file
        return "File uploaded"
    return render_template('index.html', form=form)

@app.route('/submitdata', methods=['POST'])
def upload_file():
    counter=0
    print(request.json)
    logging.info("Request : ",request.json)
    # d1 = datetime.datetime.now()
    dateToday=date.today()
    filename1 = "request"+str(dateToday)+".txt"
    with open(filename1,'w') as file:
        file.write(str(request.json))
    
    return jsonify(request.json),201

if __name__ == '__main__':
    app.run(debug=True)
    # from waitress import serve
    # serve(app, host="0.0.0.0", port=80)
