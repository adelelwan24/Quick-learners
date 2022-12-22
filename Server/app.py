import cohere
import pinecone
import numpy as np

from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify, session
from flask_moment import Moment
from flask_bcrypt import Bcrypt
import os

from models import *
from VDB import save_to_vdb # , index_query, index_query_name

# Paste your API key here. Remember to not share publicly
COHERE_API_KEY = 'rImV4bTb4stL21jKzhFZi6PNF5a4Sv5g7FKulaSW'

# Create and retrieve a Cohere API key from os.cohere.ai
co = cohere.Client(COHERE_API_KEY)


PIENCONE_API_KEY_INDEX = "3d2006de-95b3-4e7d-9ec1-54133c34001e"
# pinecone_1 = pinecone
pinecone.init(PIENCONE_API_KEY_INDEX, environment='us-west1-gcp')


index_name = 'first-index'
# connect to index
index = pinecone.Index(index_name)

# if the index does not exist, we raise assertion
if index_name not in pinecone.list_indexes():
    assert False, f"The pinecone index {index_name}: IS NOT VALID"

# if index_query_name not in pinecone.list_indexes():
#     assert False, f"The pinecone index {index_query_name}: IS NOT VALID"
    

app = Flask(__name__)
app.config.from_object('config')
bcrypt = Bcrypt(app)
moment = Moment(app)
db.init_app(app)

# # used once to create the tables in the database shouldn't be used again
# with app.app_context():
#     db.create_all()
#     print("All tables are created")


@app.route('/query', methods=["POST"])
def query():
    print('========================================================================')
    data = request.get_json()
    print(data)
    query = data['query']
    print(query)
    print('========================================================================')
    # create the query embedding
    xq = co.embed(
        texts=[query],
        model='small',
        truncate='LEFT'
    ).embeddings[0]

    print(np.array(xq).shape)

    # query, returning the top 5 most similar results
    res = index.query(xq, top_k=5, include_metadata=True)

    data = []
    for match in res['matches']:
        print(f"{match['score']:.2f}: {match['metadata']['text']}")
        dic = {}
        dic['video_id'] = match['metadata']['video_id']
        dic['start'] = match['metadata']['start']
        dic['text'] = match['metadata']['text']
        data.append(dic)
    print(data)

    return jsonify(data)
    

@app.route('/api/register', methods=["POST"])
def insert_user():
    data = request.json
    hashed_password = bcrypt.generate_password_hash(data["password"])

    user_exists = User.query.filter_by(email=data["email"], user_name=data["user_name"]).first() is not None

    if user_exists:
        return jsonify({"logged_in": False}), 409
    
    try:
        new = User(
        name = data["name"],
        user_name = data["user_name"],
        email = data["email"],
        password = hashed_password
        )
        print(new)
        db.session.add(new)
        db.session.commit()
        print('============================================= mission success =============================================')
    except:
        db.session.rollback()
        print('============================================= mission failed =============================================')
        return jsonify({"logged_in": False})

    session["user_id"] = new.id

    return jsonify({"logged_in": True})
    
@app.route("/api/login", methods=["POST"])
def login_user():
    email = request.json["email"]
    password = request.json["password"]

    user = User.query.filter_by(email=email).first()

    if user is None:
        return jsonify({"logged_in": False}), 401

    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"logged_in": False}), 401
    
    session["user_id"] = user.id

    return jsonify({"logged_in": True})

@app.route("/api/logout")
def log_out():
    session['user_id'] = None
    return jsonify({'logged_in' : False})

@app.route('/api/get_users')
def get_users():
    try:
        users = User.query.all()
        print('============================================= mission success =============================================')
    except:
        db.session.rollback()
        print('============================================= mission failed =============================================')


    return jsonify([object_as_dict(new) for new in users])


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 2000))
    app.run(host='0.0.0.0', port=port, debug=True)



