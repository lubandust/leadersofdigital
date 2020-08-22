import subprocess
import io
import re
import argparse


def to_db(id_request, audio_text):
    import pymysql.cursors

    connection = pymysql.connect(host='novorossiareq.cyjyofsatlzg.eu-north-1.rds.amazonaws.com',
                             user='Smellcode',
                             password='deepdark',
                             db='Novorossia',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            sql = "UPDATE Request SET Request_text='%s' WHERE idRequest=%s" % (str(audio_text), str(id_request))
            cursor.execute(sql)
            connection.commit()

    finally:
        connection.close()


def process(stored_audio):
    proc = subprocess.Popen(['python', '/home/box/kaldi/kaldi/vosk-api/python/example/test_simple.py', stored_audio], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    str = proc.communicate()[0]
    str_utf8 = str.decode('utf8')
    a = re.search(r'\b(text)\b', str_utf8)
    result = str_utf8[a.start()+9:-4]
    return result


parser = argparse.ArgumentParser(description='')
parser.add_argument('--id',  type=int,dest='id_request',  help='an integer for the accumulator')
parser.add_argument('--loc', dest='location', help='sum the integers (default: find the max)')

args = parser.parse_args()
stored_audio = '/tmp/speech_dataset/пожар/record_online_voice_recorder_tools_diktorov_net_1598080381.wav'
audio_text=process(stored_audio)
to_db(args.id_request, audio_text)
