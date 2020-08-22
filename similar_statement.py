from sentence_transformers import SentenceTransformer, util
import numpy as np
import scipy.spatial
import pymysql.cursors
import argparse

def get_db_data(user_id):
    connection = pymysql.connect(host='novorossiareq.cyjyofsatlzg.eu-north-1.rds.amazonaws.com',
                             user='Smellcode',
                             password='deepdark',
                             db='Novorossia',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

    try:
        corpus = []
        with connection.cursor() as cursor:
            sql = "SELECT idRequest, Request_text FROM `Request` WHERE Identifier=%s"%(user_id)
            cursor.execute(sql)
            result = cursor.fetchall()
            print(result)

            for row in result:
                corpus.append(row['Request_text'])
    finally:
        connection.close()
    return corpus




parser = argparse.ArgumentParser(description='')
parser.add_argument('--user_id', type=int, dest='user_id', help='')

args = parser.parse_args()

corpus = get_db_data(args.user_id)

embedder = SentenceTransformer('blinoff-fine-tuned-last-14')

##Queries - последнее по дате обращение от пользователя

queries = ['Прекратился патруль улиц']

closest_n = 5

query_embeddings = embedder.encode(queries)

for query, query_embedding in zip(queries, query_embeddings):
    distances = scipy.spatial.distance.cdist([query_embedding], corpus_embeddings, "cosine")[0]

    results = zip(range(len(distances)), distances)
    results = sorted(results, key=lambda x: x[1])

    print("\n\n======================\n\n")
    print("Новое обращение:", query)
    print("\nСортировка по схожести ображения с предыдущими обращениями пользователя::")

    for idx, distance in results[0:closest_n]:
        print(corpus[idx].strip(), "(Score: %.4f)" % (1-distance))
