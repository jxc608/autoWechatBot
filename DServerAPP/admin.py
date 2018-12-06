from django.contrib import admin

# Register your models here.
from .models import *

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["id", "question_text", "pub_date"]

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ["id", "question", "choice_text", "votes"]

@admin.register(Clubs)
class ClubsAdmin(admin.ModelAdmin):
    list_display = ["uuid", "user_name", "password", "expired_time", "cost_mode", "cost_param", "profit", "refresh_time"]

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ["id", "club", "wechat_id", "wechat_uuid", "wechat_nick_name", "nick_name", "current_score", "history_profit", "history_cost", "introducer",
                    "today_hoster_number", "score_limit", "score_limit_desc", "is_del", "is_bind"]

@admin.register(PlayerClearCost)
class PlayerClearCost(admin.ModelAdmin):
    list_display = ["id", "player_id", "history_cost", "create_time"]

@admin.register(GameID)
class GameIdAdmin(admin.ModelAdmin):
    list_display = ["id", "player", "club", "game_nick_name", "gameid"]

@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ["id", "player", "score", "cost", "is_host", "create_time", "room_id", "refresh_time"]

@admin.register(HistoryGame)
class HistoryGameAdmin(admin.ModelAdmin):
    list_display = ["id", "club", "room_id", "hoster_name", "hoster_id", "round_number", "start_time", "player_data", "create_time", "cost", "score", "refresh_time"]

@admin.register(HistoryGameClearCost)
class HistoryGameClearCostAdmin(admin.ModelAdmin):
    list_display = ["id", "history_id", "cost", "create_time"]

@admin.register(Cdkey)
class CdkeyAdmin(admin.ModelAdmin):
    list_display = ["id", "cdkey", "key_type", "status", "create_time"]

@admin.register(WrongImage)
class WrongImageAdmin(admin.ModelAdmin):
    list_display = ["id", "club_name", "image", "create_time"]

@admin.register(ScoreChange)
class ScoreChangeAdmin(admin.ModelAdmin):
    list_display = ["id", "player", "score", "agent", "ip", "create_time"]

@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ["id", "club", "wechat_nick_name", "nick_name", "create_time"]
