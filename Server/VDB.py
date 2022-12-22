import pinecone
import numpy as np


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


def save_to_vdb(data):      # takes (user_id, embd) --> returns boolen values express succes
    # assert type(embed) == 'list', 'Embbeding sould be a list'


    print(f"active index: {pinecone.list_indexes()}")
    index_query_stats = index_query.describe_index_stats()
    print(f"total_vector_count1:{index_query_stats['total_vector_count']}")
    id = str(index_query_stats['total_vector_count'] + 1)
    print(f"The first id avilable: {id}")
    meta = {'user_id' : data['user_id']}
    embed = data['embed']
    embed = list(embed)
    print('==============================================================================================')

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



if __name__ == '__main__':
    d = {'user_id' : 2 , 'embed' : list(np.zeros((1024,),dtype=float))}
    b = save_to_vdb(d)
    print(f"save to vector db fuction returned {b}")