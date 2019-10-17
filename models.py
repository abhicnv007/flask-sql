from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# print(db)


class Bank(db.Model):
    __tablename__ = "banks"

    name = db.Column(db.String)
    id = db.Column(db.Integer, primary_key=True)

    def __init__(self, name, id):
        self.name = name
        self.id = id

    def __repr__(self):
        return f"<bank {self.name}>"

    def serialize(self):
        return {"name": self.name, "id": self.id}


class Branch(db.Model):
    __tablename__ = "branches"

    # id = db.Column(db.Integer, primary_key=True)
    ifsc = db.Column(db.String, primary_key=True)
    bank_id = db.Column(db.Integer)
    branch = db.Column(db.String)
    address = db.Column(db.String)
    city = db.Column(db.String)
    district = db.Column(db.String)
    state = db.Column(db.String)

    def __init__(self, ifsc, bank_id, branch, address, city, district, state):
        self.ifsc = ifsc
        self.bank_id = bank_id
        self.branch = branch
        self.address = address
        self.city = city
        self.district = district
        self.state = state

    def __repr__(self):
        return f"<ifsc {self.ifsc}>"

    def serialize(self):
        return {
            "ifsc": self.ifsc,
            "bank_id": self.bank_id,
            "branch": self.branch,
            "address": self.address,
            "city": self.city,
            "district": self.district,
            "state": self.state,
        }
