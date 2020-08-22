# -*- coding: utf-8 -*-
import subprocess
import io
import re
import argparse
import pymysql

def get_theme(id_request, audio_text):
    count_words = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index_themes = ['Сельское хозяйство', 'Транспорт и дорожное хозяйство', 'Социальная сфера', 'Безопасность', 'Экономика', 'Культура', 'Благоустройство', 'ЖКХ', 'Государство', 'Инфраструктура', 'Политика и Общество']
    themes = [['ферма', 'засуха', 'комбайн', 'урожай', 'нехватка', 'пожар', 'агро', 'сельское хозяйство', 'огород', 'поле', 'поля', 'урожай', 'птиц', 'насеком', 'испортили', 'рост', 'парник', 'влажность', 'животн', 'коров', 'коз', 'куриц', 'яиц', 'яйц', 'петух', 'сельск', 'село'],
    ['машин', 'авто', 'мотоцик', 'светофор', 'авари', 'столкнул', 'пешеход', 'дорог', 'яма', 'ямы', 'впадин', 'трещин', 'асфальт', 'тротуар', 'свет', 'освещен', 'троллейб', 'маршрут', 'карет', 'трамв'],
    ['медицин', 'образован', 'лечен', 'универ', 'музе', 'библиотек', 'школ', 'воспитат', 'учите', 'колледж', 'несовершеннолетн', 'неблагонад', 'льгот', 'прав', 'инвалид', 'соцпакет', 'обществ', 'субботник'],
    ['взрыв', 'пожар', 'теракт', 'огон', 'потоп', 'преступ', 'мошенн', 'боюс', 'стра', 'убий', 'педоф', 'вор', 'краж', 'украл', 'пьян', 'бух', 'алкогол', 'бьет', 'избив', 'безопас', 'опасн', 'угроз', 'псих', 'опас', 'сумашед', 'сумасшед', 'псих'],
    ['подорож', 'подешев', 'упал', 'качест', 'курс', 'евро', 'бензин', 'рубль', 'доллар', 'пенс', 'начислен', 'налог', 'деньг', 'цен', 'магаз', 'банк'],
    ['музе', 'театр', 'представлен', 'обществ', 'мероприят', 'картин', 'выставк', 'экскурс', 'обзор', 'истор', 'картин', 'стат', 'скульпт', 'памятн', 'искусст', 'искус', 'выступл', 'спорт', 'соревнован', 'представл', 'культур', 'зоопар', 'парк', 'лес', 'площад'],
    ['двор', 'стен', 'дом', 'высот', 'этаж', 'фонтан', 'яма', 'гряз', 'не убира', 'собак', 'бездомн', 'бродяч', 'сад', 'безопасн',  'ремонт', 'закрас', 'испорт', 'граф', 'рисун', 'сломал', 'подвал', 'клетк', 'шум', 'громк', 'чист', 'лестн'],
    ['вод', 'трубы', 'квартир', 'комнат', 'сосед', 'коммуналк', 'свет', 'электричеств' ,'счетчик', 'газ', 'телефон', 'счет', 'интернет', 'откл', 'квитанц'],
    ['бюдже', 'Кризис', 'экономик', 'лидер', 'оппозиц', 'выбор', 'дум', 'регион', 'стран', 'бюллетень', 'билютень', 'фальсифи', 'отравлен', 'заказн', 'устранен' 'сми', 'политик'],
    ['светофор', 'кольцевая', 'развязка', 'шоссе', 'ввп', 'инвестиции', 'развитие', 'автобан', 'трасса', 'полотно', 'движение', 'загруженность', 'канализация', 'инвестиции'],
    ['митинг', 'спич', 'пикет', 'забастовка', 'бунт', 'закон', 'предложен', 'госдум', 'проект', 'агитац']]
    for i in range(len(themes)):
        for j in range(len(themes[i])):
            if themes[i][j] in audio_text:
                count_words[i] = count_words[i]+1
    idx = count_words.index(max(count_words)) 
    theme = index_themes[idx]
    connection = pymysql.connect(host='novorossiareq.cyjyofsatlzg.eu-north-1.rds.amazonaws.com',
                             user='Smellcode',
                             password='deepdark',
                             db='Novorossia',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            sql = "SELECT Request_Text FROM Requests WHERE ID_Request=%s" % str(id_request)
            cursor.execute(sql)
            connection.commit()

        with connection.cursor() as cursor:
            sql = "UPDATE Requests SET Theme_Request='%s' WHERE ID_Request=%s" % (str(theme), str(id_request))
            cursor.execute(sql)
            connection.commit()

    finally:
        connection.close()



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
            sql = "UPDATE Requests SET Request_Text='%s' WHERE ID_Request=%s" % (str(audio_text), str(id_request))
            cursor.execute(sql)
            connection.commit()

    finally:
        connection.close()


def process(stored_audio):
    proc = subprocess.Popen(['python', '/home/box/kaldi/kaldi/vosk-api/python/example/test_simple.py', stored_audio], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    str = proc.communicate()[0]
    str_utf8 = str.decode('utf8')
    print(str_utf8)
    a = re.search(r'\b(text)\b', str_utf8)
    result = str_utf8[a.start()+9:-4]
    return result


parser = argparse.ArgumentParser(description='')
parser.add_argument('--id',  type=int,dest='id_request',  help='an integer for the accumulator')
parser.add_argument('--loc', dest='location', help='sum the integers (default: find the max)')

args = parser.parse_args()
#stored_audio = '/tmp/speech_dataset/пожар/record_online_voice_recorder_tools_diktorov_net_1598080381.wav'
audio_text=process(args.location)
to_db(args.id_request, audio_text)
get_theme(args.id_request, audio_text)
