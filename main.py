import csv
from flask import Flask, render_template, request, redirect, send_file
from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
from wtforms import StringField
from flask import Flask, request, redirect, render_template
from paramiko import SSHClient
from scp import SCPClient
import os



MAX_BYTE = 8294400

def sendFile(pin,username,host):
    ssh = SSHClient()
    ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
    ssh.connect(host, username=username)
    with SCPClient(ssh.get_transport()) as scp:
        scp.put(pin+".jpeg", '/home/'+username+'/csc380/'+pin+".jpeg")# second parameter is what the name of the sent file is

def getPins():
    with open('/home/cj/PycharmProjects/ImageTransporter/KIOSK-People-Counter/pin.csv', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)

    return data[0]


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisisasecret!'
class PinForm(FlaskForm):

    pin = StringField('Pin:')
    name = StringField('Name:')


def upload_file():
   if request.method == 'POST':

      return 'file uploaded successfully'
@app.route('/error')
def error():
   return render_template('error.html')

@app.route('/', methods=['GET', 'POST'])
def form():
    form = PinForm()


    if request.method == 'POST':
        if form.pin.data in getPins():
            print(form.pin.data)
            f = request.files['file']
            f.save(secure_filename(f.filename))

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


@app.route('/fileupload')
def fileupload():
    return render_template('fileupload.html')


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        return "File saved successfully"


if __name__ == '__main__':
    app.run(debug=True)