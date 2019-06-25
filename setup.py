import random

from model import db, Donor, Donation 
#from passlib.hash import pbkdf2_sha256

db.connect()

# This line will allow you "upgrade" an existing database by
# dropping all existing tables from it.
db.drop_tables([Donor, Donation])

db.create_tables([Donor, Donation])

alice = Donor(name="Alice", password="password")
alice.save()

bob = Donor(name="Bob", password="password2")
bob.save()

charlie = Donor(name="Charlie",password="password3")
charlie.save()

donors = [alice, bob, charlie]



for x in range(30):
    donor = random.choice(donors)
    Donation(donor=donor.id, value=random.randint(100, 10000)).save()
