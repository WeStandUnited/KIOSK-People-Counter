import csv
from flask import Flask, render_template, request, redirect, send_file
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import ValidationError,AnyOf

def getPins():
    with open('pin.csv', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)

    return data[0]








app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisisasecret!'
class PinForm(FlaskForm):

    pin = StringField('Pin:')
    name = StringField('Name:')

@app.route('/error')
def error():
   return render_template('error.html')

@app.route('/', methods=['GET', 'POST'])
def form():
    form = PinForm()

    if request.method == 'POST':
        if form.pin.data in getPins():
            return '<h1>Hello {}. you have been added!'.format(form.pin.data)
        else:
            return redirect('/error')#<h1>Error {}. not valid'.format(form.pin.data)


    return render_template('form.html', form=form)


@app.route('/facedownload')
def zipdownload():
    if (request.environ.get('HTTP_X_REAL_IP', request.remote_addr) == '127.0.0.1'):#replace with IP of RPI
        path = 'face.zip'
        return send_file(path, as_attachment=True)
    else:
        return render_template('error.html')





if __name__ == '__main__':
    app.run(debug=True)