import cohere
import pinecone
import numpy as np

from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify, session
from flask_moment import Moment
from flask_bcrypt import Bcrypt
import os

from models import *
from VDB import save_to_vdb, query_vdb_by_user_id, get_closer_queries # , index_query, index_query_name

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








def update_rec(query_emb , user_id):
    close_users = get_closer_queries(query_emb)

    for user in close_users:
        if user_id == user['user_id']:
            continue
        users_conn = Rec.query.filter(or_(and_(Rec.user_1_id==user_id, Rec.user_2_id==user['user_id']),
                                            and_(Rec.user_2_id==user_id, Rec.user_1_id==user['user_id']))).first() 
        if users_conn != None :
            try:
                users_conn.score = (users_conn.score+user['score'])/2 + 5
                db.session.commit()
            except Exception as e:
                print(f"There is an Exception in updating rec: {e}")
                db.session.rollback()
        else:
            try:
                new_users_conn = Rec( user_1_id=user['user_id'], user_2_id=user_id, score=user['score']) 
                db.session.add(new_users_conn)
                db.session.commit()
            except Exception as e:
                print(f"There is an Exception in creating rec: {e}")
                db.session.rollback()

@app.route('/query', methods=["POST"])
def query():
    data = request.get_json()
    query = data['query']
    user_id = session['user_id']
    print(query)
    print('========================================================================')
    # create the query embedding
    embed = co.embed(
        texts=[query],
        model='small',
        truncate='LEFT'
    ).embeddings[0]

    print(np.array(embed).shape)

    # query, returning the top 5 most similar results
    res = index.query(embed, top_k=5, include_metadata=True)

    data = []
    for match in res['matches']:
        print(f"{match['score']:.2f}: {match['metadata']['text']}")
        dic = {}
        dic['video_id'] = match['metadata']['video_id']
        dic['start'] = match['metadata']['start']
        dic['text'] = match['metadata']['text']
        data.append(dic)

    if user_id:
        text = query
        data_to_vdb = {user_id, embed, text}
        status = save_to_vdb(data_to_vdb)      # # takes (user_id, embd) --> returns boolen values express succes

    update_rec(embed, user_id)

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

@app.route("api/logged_in")
def is_logged_in():
    if session['user_id']:
        return jsonify({"logged_in": True})
    return jsonify({"logged_in": False})

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



@app.route("/api/user_rec", methods=["GET"])
def get_user_rec():
    user_id = session['user_id']
    if user_id == None :
        return jsonify({"logged_in": False,"users_data": []})
    users_conn = Rec.query.filter(or_(Rec.user_1_id==user_id, Rec.user_2_id==user_id)).order_by(Rec.score.desc()).limit(5)
    users_data = []
    for conn in users_conn :
        dic = {}
        if conn.user_1_id == user_id :
            other_user = User.query.filter(User.id == conn.user_2_id).first()
            dic['name'] = other_user.name
            dic['username'] = other_user.username

        elif conn.user_2_id == user_id :
            other_user = User.query.filter(User.id == conn.user_1_id).first()
            dic['name'] = other_user.name
            dic['username'] = other_user.username
        users_data.append(dic)
    return jsonify({"logged_in": True,"users_data": users_data})


@app.route("/api/post_rec", methods=["GET"]) 
def post_recommindation(): 
    user_id = session['user_id'] 
    if user_id == None : 
        return jsonify({"logged_in": False,"posts": []}) 
    users = Rec.query.filter(or_(Rec.user_1_id==user_id, Rec.user_2_id==user_id)).order_by(Rec.score.desc()).limit(4) 
    embeddings = []
    queries = [] 
    len_users = len(users) 
    for i in range(len_users) : 
        dic = {} 
        if users[i].user_1_id == user_id : 
            e, q = query_vdb_by_user_id(users[i].user_2_id, len_users-i) 
            embeddings += e
            queries += q
        elif users[i].user_2_id == user_id : 
            e, q = query_vdb_by_user_id(users[i].user_1_id, len_users-i) 
            embeddings += e
            queries += q

    pinecone.init(PIENCONE_API_KEY_INDEX, environment='us-west1-gcp') 
    index_name = 'first-index' 
    # connect to index 
    index = pinecone.Index(index_name) 
 
    for i in range(len(embeddings)): 
        res = index.query(embeddings[i], top_k=1, include_metadata=True)
        data = [] 
        for match in res['matches']: 
            print(f"{match['score']:.2f}: {match['metadata']['text']}") 
            dic = {} 
            dic['video_id']= match['metadata']['video_id'] 
            dic['start']= match['metadata']['start'] 
            dic['text'] = match['metadata']['text']
            dic['query'] = queries[i]
            data.append(dic) 
     
    return jsonify({"logged_in": True,"posts": data})



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 2000))
    app.run(host='0.0.0.0', port=port, debug=True)



