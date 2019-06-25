import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session

from model import Donation, Donor

app = Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('all'))

@app.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)

@app.route('/creating/', methods=['GET', 'POST'])
def create():

    # Case statement where form method is "POST"
    if request.method == "POST":
        # Create an instance of the Donor in the Donors
        donor = Donor(name=request.form['name'])
        # Save this information to the Donor's Table
        donor.save()

        # Obtain the value of the donation
        value = int(request.form['donation'])
        # Create a new instance of a donation and save it to the database
        Donation(donor=donor.id, value=value).save()
        
        return render_template('creating.jinja2')
    
    # Case Statement where form method is "GET"
    elif request.method == "GET":
        return render_template('creating.jinja2')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)

