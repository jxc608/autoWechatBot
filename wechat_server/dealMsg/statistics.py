#encoding=utf-8
import logging, traceback
import datetime
from DServerAPP.models import ClubOrcCount
from django.db.models import F

logger = logging.getLogger(__name__)

def addClubOrcCount(club):
    curDate = datetime.datetime.now().date()
    ct = ClubOrcCount.objects.filter(club=club, use_date=curDate).first()
    if not ct:
        ct = ClubOrcCount(club=club, use_date=curDate)
        ct.save()
    ct.count = F("count") + 1
    ct.save()

def addClubOrcRepeatCount(club):
    curDate = datetime.datetime.now().date()
    ct = ClubOrcCount.objects.filter(club=club, use_date=curDate).first()
    if not ct:
        ct = ClubOrcCount(club=club, use_date=curDate)
        ct.save()
    ct.repeat_count = F("repeat_count") + 1
    ct.save()

def addClubOrcFailCount(club):
    curDate = datetime.datetime.now().date()
    ct = ClubOrcCount.objects.filter(club=club, use_date=curDate).first()
    if not ct:
        ct = ClubOrcCount(club=club, use_date=curDate)
        ct.save()
    ct.fail_count = F("fail_count") + 1
    ct.save()