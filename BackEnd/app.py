# Install Cohere for embeddings, Umap to reduce embeddings to 2 dimensions, 
# Altair for visualization, Annoy for approximate nearest neighbor search
# pip install cohere umap-learn altair datasets tqdm annoy

import cohere
import numpy as np
import re
import pandas as pd
from tqdm import tqdm
# from datasets import load_dataset
# import umap
import altair as alt
# from sklearn.metrics.pairwise import cosine_similarity
from annoy import AnnoyIndex
import warnings
warnings.filterwarnings('ignore')
pd.set_option('display.max_colwidth', None)


from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify

import json
# Paste your API key here. Remember to not share publicly
api_key = 'rImV4bTb4stL21jKzhFZi6PNF5a4Sv5g7FKulaSW'

# Create and retrieve a Cohere API key from os.cohere.ai
co = cohere.Client(api_key)


embeds = np.zeros((1000,1000))              # np.array of the 
# Let's now use Annoy to build an index that stores the embeddings in a way that is optimized for fast search.
# This approach scales well to a large number of texts (other options include Faiss, ScaNN, and PyNNDescent).
# Create the search index, pass the size of embedding
search_index = AnnoyIndex(embeds.shape[1], 'angular')
# Add all the vectors to the search index
for i in range(len(embeds)):
    search_index.add_item(i, embeds[i])

search_index.build(10) # 10 trees
search_index.save('test.ann')


app = Flask(__name__)

@app.route('/')
def index():
	return render_template('pages/home.html')


@app.route('/query', methods=["POST"])
def query():
    query = request.data
    print(query)
    # # Get the query's embedding
    # query_embed = co.embed(texts=[query],
    #                 model="large",
    #                 truncate="LEFT").embeddings

    # # Retrieve the nearest neighbors
    # similar_item_ids = search_index.get_nns_by_vector(query_embed[0],10,
    #                                                 include_distances=True)
    # # Format the results
    # results = pd.DataFrame(data={'texts': df.iloc[similar_item_ids[0]]['text'], 
    #                             'distance': similar_item_ids[1]})


    # print(f"Query:'{query}'\nNearest neighbors:\n{results}")

    return jsonify({"id": 'gdGiGT-t_uw', 'time': '2000'})
    

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


# Default port:
# if __name__ == '__main__':
#     app.run()

# Or specify port manually:
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 2000))
    app.run(host='0.0.0.0', port=port)

