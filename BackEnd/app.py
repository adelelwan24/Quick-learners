import cohere
import pinecone
import numpy as np

from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify

import os

# Paste your API key here. Remember to not share publicly
COHERE_API_KEY = 'rImV4bTb4stL21jKzhFZi6PNF5a4Sv5g7FKulaSW'

# Create and retrieve a Cohere API key from os.cohere.ai
co = cohere.Client(COHERE_API_KEY)


PIENCONE_API_KEY = "3d2006de-95b3-4e7d-9ec1-54133c34001e"
pinecone.init(PIENCONE_API_KEY, environment='us-west1-gcp')

index_name = 'first-index'
# connect to index
index = pinecone.Index(index_name)

app = Flask(__name__)


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
    

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 2000))
    app.run(host='0.0.0.0', port=port, debug=True)

