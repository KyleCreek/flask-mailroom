import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session
#from passlib.hash import pbkdf2_sha256
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

        # Case statement where the user DOES NOT already exists in the Database
        if request.form['name'] not in users_list:

            return redirect(url_for('create_user'))
        
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

@app.route('/create_user/', methods=['GET', 'POST'])
def create_user():

    # Case statement to handle user input
    if request.method == "POST":
        # Obtain the new Donor Name and Password
        new_donor_name = request.form['name'].title()
        new_donor_password = request.form['password']

        # Case Statement ensures that values are entered for the User
        if len(new_donor_name) == 0 or len(new_donor_password) == 0:
            print("Substance Required!")

            return render_template('create_user.jinja2')
        
        # Case statement where sufficient data is provided
        else:
            ### Check to Make sure the user name isn't already chosen!
            
            # Create a list of all the existing Donors in the database
            users_list = [user.name for user in Donor.select()]
            if new_donor_name in users_list:
                print("that name is chosen")
                return redirect(url_for('create_user_error'))
            else:
                # If the Name isn't in the list of donors, Create it!
                donor = Donor(name=new_donor_name, password=(new_donor_password)).save()

            return redirect(url_for('all'))
    # Case statement to handle a 'GET' Request
    else:
        return render_template('create_user.jinja2')

@app.route('/create_user_error', methods=['GET', 'POST'])
def create_user_error():

    if request.method == "POST":
        return redirect(url_for('create_user'))
    else:
        return render_template('create_user_error.jinja2')

@app.route('/single_donor/', methods=['GET', 'POST'])
def single_donor():

    if request.method =="POST":
        pass

    elif request.method == "GET":
        return render_template('single_donor.jinja2')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)