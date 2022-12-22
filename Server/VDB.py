import pinecone
import numpy as np

FAKE_EMBED = list(np.zeros((1024,),dtype=float))
RAND_EMBED = [np.random.rand() for _ in range(1024)]
PIENCONE_API_KEY_QUERY_INDEX = "f666fbf4-53bd-4f5f-ba64-6656e426ab8c"
pinecone.init(PIENCONE_API_KEY_QUERY_INDEX, environment='us-west1-gcp')
index_query_name = 'query-index'

if index_query_name not in pinecone.list_indexes():
    # assert False, f"The pinecone index {index_query_name}: IS NOT VALID"
    print(f"The pinecone index {index_query_name}: IS NOT VALID")
    pinecone.create_index(
    index_query_name,
    dimension=1024,
    metric='dotproduct'
    )
    print(f"The pinecone index {index_query_name}: Created")

index_query = pinecone.Index(index_query_name)

def get_closer_queries(query_emb):
    # PIENCONE_API_KEY_QUERIES = "f666fbf4-53bd-4f5f-ba64-6656e426ab8c"
    # pinecone.init(PIENCONE_API_KEY_QUERIES, environment='us-west1-gcp')
    # index_name = 'query-index'
    # # connect to index
    # index_query = pinecone.Index(index_name)
    res = index_query.query(query_emb, top_k=5, include_metadata=True)
    users = []
    for match in res['matches'] :
        dic = {}
        dic['user_id']= match['metadata']['user_id']
        dic['score']= match['score']
        users.append(dic)
    return users


def save_to_vdb(data):      # takes (user_id, embd, text) --> returns boolen values express succes
    print(f"active index: {pinecone.list_indexes()}")
    index_query_stats = index_query.describe_index_stats()

    print(f"total_vector_count1:{index_query_stats['total_vector_count']}")
    id = str(index_query_stats['total_vector_count'] + 1)
    print(f"The first id avilable: {id}")

    meta = {'user_id' : data['user_id'], 'text' : data['text']}
    embed = data['embed']
    embed = list(embed)
    try:
        index_query.upsert(vectors=[(id, embed, meta)])
        print('=============================== mission success ==============================================')
    except Exception as e:
        print(f"The Exception : \n{e}")
        print('=============================== mission failed =============================================')
        print(f"active index: {pinecone.list_indexes()}")
        return False
    print(f"total_vector_count3:{index_query_stats['total_vector_count']}")
    # print(pinecone.delete_index("query-index"))
    return True

def query_vdb_by_user_id(user_id):
    print(f"active index: {pinecone.list_indexes()}")
    res = index_query.query(RAND_EMBED, top_k=5,
     include_metadata=True, include_values=True,
    filter={'user_id' : {'$eq' : user_id}})

    embeds = []                 # [[]]
    queries = []
    for match in res['matches']:
        print(f"{match['score']:.2f}: {match['id']}")
        embeds.append(match['values'])
        queries.append(match['metadata']['text'])
    return embeds, queries

if __name__ == '__main__':
    d = {'user_id' : 3, 'embed' : RAND_EMBED, 'text' : 'hello world!'}
    b = save_to_vdb(d)
    print('==============================================================================================')
    print(query_vdb_by_user_id(3))
    print(f"save to vector db fuction returned {b}")