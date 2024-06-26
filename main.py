from flask import (Flask, request, jsonify, render_template)
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db = SQLAlchemy(app)
app.app_context().push()


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    eating_fre = db.Column(db.String(100))
    momos_var = db.Column(db.String(100))
    addon = db.Column(db.String(100))
    gender = db.Column(db.String(100))
    name = db.Column(db.String(100), nullable=False)
    preffered_time = db.Column(db.String(100))
    age = db.Column(db.Integer)
    place = db.Column(db.String(50))
    occupation = db.Column(db.String(100))
    review = db.Column(db.String)
    substitute = db.Column(db.String)

    def __repr__(self):
        return f"<Customer {self.name}>"


db.create_all()


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route('/submit', methods=['POST'])
def submit_form():
    try:
        data = request.get_json()
        fre = data.get('fre')
        varity = data.get('varity')
        addon = data.get('addon')
        gender = data.get('gender')  # Retrieve other fields as needed
        name = data.get('name')
        pre = data.get('pre')
        age = data.get('age')
        place = data.get('place')
        occu = data.get('occu')
        review = data.get('review')
        substitute = data.get('substitute')
        # Validate fields (example: age must be between 18 and 120)
        if not (18 <= age <= 120):
            raise ValueError("Invalid age. Must be between 18 and 120.")
        menu_dict = {
            "vmomos": "VEG MOMO",
            "chickenmomos": "CHICKEN MOMO",
            "paneermomos": "PANEER MOMO",
            "gravymomos": "GRAVY MOMO",
            "frymomos": "FRY MOMO",
            "sbmomos": "SOYA BOL"
        }
        location_dict = {
            "wom": "WOW MOMO'S HUT",
            "super": "Super Delicious Momos",
            "spicy": "SPICY CHAT & MOMO'S",
            "panda": "Momo Panda",
            "gmomo": "Golu Momos Centre",
            "darjeeling": "Darjeeling Momos Rohit",
            "kmomos": "Krishna Momos",
            "xomo": "MOMO XOMO"
        }

        # Create a new customer record
        new_customer = Customer(
            eating_fre=fre.lower(),
            momos_var=menu_dict[varity].lower(),
            addon=addon.lower(),
            gender=gender.lower(),
            name=name.lower(),
            preffered_time=pre.lower(),
            age=age,
            place=location_dict[place].lower(),
            occupation=occu.lower(),
            review=review,
            substitute=substitute.lower()
        )
        db.session.add(new_customer)
        db.session.commit()
        return jsonify({'message': 'Data saved successfully!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/client')
def proxy_client():
    ip_addr = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    return '<h1> Your IP address is:' + ip_addr


if __name__ == "__main__":
    app.run(debug=True)
