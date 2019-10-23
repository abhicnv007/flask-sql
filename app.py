import os

from flask import Flask, jsonify
from webargs import fields
from webargs.flaskparser import use_args
from flask_jwt import JWT, jwt_required

from models import db, Branch, Bank
from auth import authenticate, identity

import config

app = Flask(__name__)

if os.environ.get("PRODUCTION"):
    app.config.from_object(config.ProductionConfig)
else:
    app.config.from_object(config.DevelopmentConfig)

db.init_app(app)

jwt = JWT(app, authenticate, identity)


@app.route("/")
def index():
    return 'Hello, visit <a href="https://github.com/abhicnv007/flask-sql" target="_blank">here</a> to learn more'


@app.route("/bank_details", methods=["GET"])
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


@app.route("/branch_details", methods=["GET"])
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
