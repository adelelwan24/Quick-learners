from youtube_transcript_api import YouTubeTranscriptApi
import googleapiclient.discovery 
import cohere
import numpy as np
import pinecone
import time

DEVELOPER_KEY = "AIzaSyBLhYAAmyHCKfHyMu9MahZpa3fuIrCHTgE"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def playlist_to_captions(playlist_id):
    
    youtube = googleapiclient.discovery.build(YOUTUBE_API_SERVICE_NAME,
                    YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)
    
    res = youtube.playlistItems().list(part="snippet",
                                        playlistId=playlist_id,
                                        maxResults="50"
                                        ).execute()

    nextPageToken = res.get('nextPageToken')
    
    while ('nextPageToken' in res):
        nextPage = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlist_id,
        maxResults="50",
        pageToken=nextPageToken
        ).execute()
        res['items'] = res['items'] + nextPage['items']

        if 'nextPageToken' not in nextPage:
            res.pop('nextPageToken', None)
        else:
            nextPageToken = nextPage['nextPageToken']

    captions = []
    # [{'video_id': 'nfWlot6h_JM', 'video_title': 'title'},  ]

    for v in res["items"]:
        dic = {}
        vid = v['snippet']["resourceId"]['videoId']
        dic["video_id"] = vid
        caps , done = video_to_captions(vid)        
        if(done):
            dic["video_captions"] = caps[0]["video_captions"]
        else:
            continue
        captions.append(dic)
        
    return captions
    
          

def video_to_captions(video_id):
    done = 0
    captions = {}
    try:
        srt = YouTubeTranscriptApi.get_transcript(video_id)
        captions["video_id"] = video_id
        captions["video_captions"] = srt
        done = 1
    except:
        done = 0
        
    return [captions] , done 

def captions_processing(caps):
    for cap in caps:
        it = 0 
        length = len(cap['video_captions'])
        new = []
        i = 0
        while(i < length): 

            cap['video_captions'][i]['text'] =  cap['video_captions'][i]['text'].replace("\n"," ")

            if cap['video_captions'][i]["text"][-1] == '.' or cap['video_captions'][i]["text"][-1] == "?":
                dic={}
                dic['start'] = cap['video_captions'][it]['start']
                dic['duration'] = cap['video_captions'][it]['duration']
                dic['text'] = cap['video_captions'][it]['text']
                for j in range(it+1,i+1): 
                    dic['text'] += " " + cap['video_captions'][j]['text']
                    dic['duration'] += cap['video_captions'][j]['duration']

                cap['video_captions'][it] = dic 

                for j in range(it+1,i+1): 
                    cap['video_captions'].pop(it+1)


                i = it
                it +=1
                length = len(cap['video_captions'])
                if i >= length :
                    break
            i+=1     
    return caps
    
def captions_to_embeddings(videos_captions):
    api_key = 'SrLBFEol9tRK7n7LY9FRRcHuN9QT5MLIzLmBSziT'
    # Create and retrieve a Cohere API key from os.cohere.ai
    co = cohere.Client(api_key)
    all_embeds = []
    no_texts = 0
    for captions in videos_captions :
        embeds = []
        texts = []
        for caption in captions['video_captions'] :
            dic = {}
            dic['start'] = caption['start']
            dic['text'] = caption['text']
            dic['video_id'] = captions['video_id']
            texts.append(caption['text'])
            dic['embedding'] = []  
            embeds.append(dic)
            
        if(len(texts) > 1600):
            chunk_size = 1600
            i = 0 
            video_embeddings = []
            while(i*chunk_size < len(texts)):
                video_embeddings += co.embed(texts[i*chunk_size : min(len(texts),(i+1)*chunk_size)],model="small").embeddings
                i+=1
                time.sleep(60)
        else:
            if((no_texts+len(texts)) > 1600 ):
                no_texts = 0 
                time.sleep(60)
            no_texts += len(texts)
            video_embeddings = co.embed(texts,model="small").embeddings
        
        for i in range(len(embeds)):
            embeds[i]['embedding'] =  video_embeddings[i]
        
        all_embeds.append(embeds)
          
    return all_embeds






# def embeddings_to_vdb(embeddings):
# #    [ [{start:--- , video_id:--- , embedding:--- }   ,] ,[  ],[  ] ,]
#     pass
def Piencone_indexing(collection):    #    -> [[{}]]  -> [[ {start:--- , video_id:--- , embedding:--- }   ,]]
    PIENCONE_API_KEY = "3d2006de-95b3-4e7d-9ec1-54133c34001e"
    
    list_dic_data = collection[0]
    shape = np.array(list_dic_data[0]["embedding"]).shape       # (1024,)
    num_embeds = len(list_dic_data)
    print(shape)



    pinecone.init(PIENCONE_API_KEY, environment='us-west1-gcp')

    index_name = 'first-index'

    # if the index does not exist, we create it
    if index_name not in pinecone.list_indexes():
        pinecone.create_index(
            index_name,
            dimension=shape[0],
            metric='dotproduct'
        )

    # connect to index
    index = pinecone.Index(index_name)



    batch_size = 128

    ids = [str(i) for i in range(num_embeds + 1)]
    # create list of metadata dictionaries
    embeds = []
    meta_data = []
    for dic_data in list_dic_data:
        meta = {}
        for key in dic_data.keys():
            if key == 'embedding':
                embeds.append(dic_data[key])
            else:
                meta[key] = dic_data[key]
        meta_data.append(meta)
        
    print(meta_data)

# meta = [{'text': text} for text in trec['text']]

    # create list of (id, vector, metadata) tuples to be upserted
    to_upsert = list(zip(ids, embeds, meta_data))

    for i in range(0, shape[0]+1, batch_size):
        i_end = min(i+batch_size, shape[0])
        a = to_upsert[i:i_end]
        if(len(a) == 0):
            break
        
        index.upsert(vectors=a)

    # let's view the index statistics
    print(index.describe_index_stats())

    return None


def playlist_to_vdb(playlist_id):
    captions = playlist_to_captions(playlist_id)
    captions = captions_processing(captions)
    embeddings = captions_to_embeddings(captions)
    Piencone_indexing(embeddings)
    
    
    
    
