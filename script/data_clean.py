import re
import init_django
from django.conf import settings
from django.db import connection
from DServerAPP.models import HistoryGame, Score

def chg_score_field():
    print("chg_score_field")
    cursor = connection.cursor()
    sql = "alter table DServerAPP_score change `room_id` `room_id` varchar(20) character set utf8 not null;"
    cursor.execute(sql)
    print("chg_score_field done")

def clearcost():
    print("clearcost")
    cursor = connection.cursor()
    sql = "set foreign_key_checks=0;"
    cursor.execute(sql)
    sql = "update DServerAPP_historygameclearcost set history_id=history_id_orgin;"
    cursor.execute(sql)
    sql = "update DServerAPP_playerclearcost set player_id=player_id_orgin;"
    cursor.execute(sql)
    print("clearcost", "end")

def chg_history_room_id():
    print("*****", "chg_history_room_id")
    cursor = connection.cursor()
    sql = "update DServerAPP_historygame set room_id='0' where room_id=''"
    cursor.execute(sql)

    items = HistoryGame.objects.all().values("room_id", "id")
    for item in items:
        room_id = "%s" % item["room_id"]
        mat = re.search("(\D)", room_id)
        if mat:
            id = item["id"]
            newId = re.sub(r'\D', "", room_id)
            sql = "update DServerAPP_historygame set room_id='%s' where id='%s'" % (newId, id)
            cursor.execute(sql)
            print(id, room_id, newId)

    print("chg_history_room_id", "done")

def chg_score_room_id():
    print("*****", "chg_score_room_id")
    cursor = connection.cursor()
    sql = "update DServerAPP_score set room_id='0' where room_id=''"
    cursor.execute(sql)

    items = Score.objects.all().values("room_id", "id")
    for item in items:
        room_id = "%s" % item["room_id"]
        mat = re.search("(\D)", room_id)
        if mat:
            id = item["id"]
            newId = re.sub(r'\D', "", room_id)
            sql = "update DServerAPP_score set room_id='%s' where id='%s'" % (newId, id)
            cursor.execute(sql)
            print(id, room_id, newId)

    print("chg_score_room_id", "done")

def reset_duplicate():
    print("reset_duplicate")
    cursor = connection.cursor()
    sql = "select club_id, room_id, start_time from (select club_id, room_id, start_time, count(*) ct from DServerAPP_historygame group by club_id, room_id, start_time) db where db.ct>1"
    cursor.execute(sql)
    dbs = cursor.fetchall()
    for db in dbs:
        club_id = db[0]
        room_id = db[1]
        start_time = db[2]
        hs = HistoryGame.objects.filter(club_id=club_id, room_id=room_id, start_time=start_time)
        i = 0
        for h in hs:
            print(h.id, club_id, room_id, start_time, i)
            if i != 0:
                h.start_time += "_%s" % i
                h.save()
            i += 1

    print("reset_duplicate", "end")


if __name__ == "__main__":
    chg_score_field()
    chg_history_room_id()
    chg_score_room_id()

    reset_duplicate()

    # clearcost()