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
        ### Note: There is room to improve this, by checking case
        # sensitivities

        # Create a list of all the existing Donors in the database
        users_list = [user.name for user in Donor.select()]

        # Case statement where the user already exists in the Database
        if request.form['name'] not in users_list:
            # Create an instance of the Donor in the Donors
            donor = Donor(name=request.form['name'])
            # Save this information to the Donor's Table
            donor.save()

            # Obtain the value of the donation
            value = int(request.form['donation'])
            # Create a new instance of a donation and save it to the database
            Donation(donor=donor.id, value=value).save()
            
            # After Donation is added, user is re-directed to the Home Page
            return redirect(url_for('all'))
        
        # Case statement where the user IS Currently in the database.
        elif request.form['name'] in users_list:
            print("User is IN in the list")
            # Select donor's information from the databse where that name exists
            # and instantiate a model object of it!
            donor = Donor.select().where(Donor.name == request.form['name']).get()

            # Obtain the value of the donation
            value = int(request.form['donation'])
            # Update the Database to include the User's Donation
            Donation(donor=donor.id, value=value).save()
            return redirect(url_for('all'))
    
    # Case Statement where form method is "GET"
    elif request.method == "GET":
        return render_template('creating.jinja2')

@app.route('/single_donor/', methods=['GET', 'POST'])
def single_donor():

    if request.method =="POST":
        pass

    elif request.method == "GET":
        return render_template('single_donor.jinja2')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)

