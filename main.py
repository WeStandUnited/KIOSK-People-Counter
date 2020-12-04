import csv
from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
from wtforms import StringField
from flask import Flask, request, redirect, render_template
from paramiko import SSHClient
from scp import SCPClient
import os
import random
from PIL import Image
from waitress import serve


PHOTO_DIRECTORY ="/Photos/"
CSV_DIRECTORY ="pin.csv"


def generate_new_pin():
    """
    Generate a new pin by finding a random number between 10000->99999
    While checking pin.csv to make sure it hasn't already been used
    """
    new_pin = random.randint(10000, 99999)
    file = os.path.abspath(CSV_DIRECTORY)
    with open(file, 'r') as r_file:
        reader = csv.reader(r_file)
        for row in reader:
            for pin in row:
                if str(new_pin) == pin:
                    new_pin = generate_new_pin()
                break
    r_file.close()
    return new_pin


def write_pin_to_csv(new_pin):
    """
    Given a unique pin, add it to the csv
    """
    file = os.path.abspath(CSV_DIRECTORY)
    with open(file, 'a', newline='') as w_file:
        writer = csv.writer(w_file)
        writer.writerow([new_pin])

    w_file.close()



app = Flask(__name__)
app.config['SECRET_KEY'] = 'shh'
class PinForm(FlaskForm):

    name = StringField('Name:')

@app.route('/error')
def error():
   return render_template('error.html')

@app.route('/registered')
def registered():
   return render_template('registered.html')

@app.route('/aboutus')
def aboutus():
   return render_template('about.html')

@app.route('/', methods=['GET', 'POST'])
def form():
    form = PinForm()

    if request.method == 'POST' and request.form['name'] is not '' and request.files['file'].filename is not '':
            f = request.files['file']
            print(f.filename)
            print(f.filename.split("."))
            new_pin = str(generate_new_pin())
            write_pin_to_csv(new_pin)
            file_ext = f.filename.split(".")[1]
            imagename = new_pin+form.name.data+"."+file_ext
            f.save(PHOTO_DIRECTORY+secure_filename(imagename))
            if (file_ext is "png" or "jpeg"):
                im1 = Image.open(PHOTO_DIRECTORY+"/"+imagename)
                im1.convert('RGB').save(PHOTO_DIRECTORY+imagename.split(".")[0]+".jpg")
                os.system("rm "+PHOTO_DIRECTORY+"*.jpeg")
                os.system("rm " + PHOTO_DIRECTORY + "*.png")



            return redirect('/registered')


    return render_template('form.html', form=form)
if __name__ == '__main__':
    #app.run(debug=True)
    print("This process has the PID:", os.getpid())
