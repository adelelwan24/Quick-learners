import pinecone
import numpy as np

FORMAT_PRINT_WIDTH = 90
FAKE_EMBED = list(np.zeros((1024,),dtype=float))
RAND_EMBED = [np.random.rand() for _ in range(1024)]

PIENCONE_API_KEY_QUERY_INDEX = "f666fbf4-53bd-4f5f-ba64-6656e426ab8c"
pinecone.init(PIENCONE_API_KEY_QUERY_INDEX, environment='us-west1-gcp')
index_query_name = 'query-index'

if index_query_name not in pinecone.list_indexes():
    print(f"The pinecone index {index_query_name}: IS NOT VALID")
    pinecone.create_index(
    index_query_name,
    dimension=1024,
    metric='dotproduct'
    )
    print(f"The pinecone index {index_query_name}: Created")

index_query = pinecone.Index(index_query_name)



import sys
def save_to_vdb(data):
    index_query_stats = index_query.describe_index_stats()

    # print(f"total_vector_count1:{index_query_stats['total_vector_count']}")
    id = str(index_query_stats['total_vector_count'] + 1)

    meta = {'user_id' : data['user_id'], 'text' : data['text']}
    embed = data['embed']
    embed = list(embed)
    try:
        index_query.upsert(vectors=[(id, embed, meta)])
        print(f' mission success '.center(FORMAT_PRINT_WIDTH, "="))
    except Exception as e:
        print(f"The Exception : \n{e}")
        print(f' The called function: {sys._getframe().f_code.co_name} '.center(FORMAT_PRINT_WIDTH, "="))
        print(f' mission failed '.center(FORMAT_PRINT_WIDTH, "="))
        return False
    return True

def query_vdb_by_user_id(user_id, num):
    res = index_query.query(RAND_EMBED, top_k=num,
     include_metadata=True, include_values=True,
    filter={'user_id' : {'$eq' : user_id}})

    embeds = []
    queries = []
    for match in res['matches']:
        print(f"{match['score']:.2f}: {match['id']}")
        embeds.append(match['values'])
        queries.append(match['metadata']['text'])
    print(f' mission success in {sys._getframe().f_code.co_name} '.center(FORMAT_PRINT_WIDTH, "="))
    return embeds, queries

if __name__ == '__main__':
    d = {'user_id' : 3, 'embed' : RAND_EMBED, 'text' : 'hello world!'}
    b = save_to_vdb(d)
    print('==============================================================================================')
    print(query_vdb_by_user_id(3))
    print(f"save to vector db fuction returned {b}")