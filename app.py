from flask import Flask, jsonify
from webargs import fields
from webargs.flaskparser import use_args
from flask_jwt import JWT, jwt_required, current_identity

from models import db, Branch, Bank
from auth import authenticate, identity

import datetime

app = Flask(__name__)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["DEBUG"] = True
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://postgres:postgres@localhost/"
app.config["SECRET_KEY"] = "super-secret"
app.config["JWT_AUTH_URL_RULE"] = "/a"
app.config["JWT_EXPIRATION_DELTA"] = datetime.timedelta(days=5)

db.init_app(app)


# dummy authentication that always returns true, and identity of user as default user
jwt = JWT(app, authenticate, identity)


@app.route("/bank_details")
@jwt_required()
@use_args({"ifsc_code": fields.Str(required=True)})
def get_bank_details(args):
    branch, bank = (
        db.session()
        .query(Branch, Bank)
        .filter(Branch.ifsc == args["ifsc_code"].upper())
        .filter(Branch.bank_id == Bank.id)
        .first()
    )

    return jsonify(bank.serialize())


@app.route("/branch_details")
@jwt_required()
@use_args(
    {
        "bank_name": fields.Str(required=True),
        "city": fields.Str(required=True),
        "limit": fields.Int(missing=10),
        "offset": fields.Int(missing=0),
    }
)
def get_branch_details(args):
    branches = []
    for _, branch in (
        db.session()
        .query(Bank, Branch)
        .filter(Bank.name == args["bank_name"].upper())
        .filter(Branch.city == args["city"].upper())
        .filter(Branch.bank_id == Bank.id)
        .limit(args["limit"])
        .offset(args["offset"])
        .all()
    ):
        branches.append(branch.serialize())

    return jsonify(branches)


@app.errorhandler(422)
def error_handler(err):
    headers = err.data.get("headers", None)
    messages = err.data.get("messages", ["Invalid request."])
    if headers:
        return jsonify({"errors": messages}), err.code, headers
    return jsonify({"erros": messages}), err.code, headers


if __name__ == "__main__":
    app.run()
