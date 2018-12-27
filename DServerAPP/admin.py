from django.contrib import admin
import time
import datetime
import json
# Register your models here.
from .models import *
from daterange_filter.filter import DateRangeForm, clean_input_prefix, FILTER_PREFIX, DateRangeFilter


class DateStampRangeFilter(DateRangeFilter):
    template = 'daterange_filter/filter.html'

    def __init__(self, field, request, params, model, model_admin, field_path):
        self.lookup_kwarg_since = '%s%s__gte' % (FILTER_PREFIX, field_path)
        self.lookup_kwarg_upto = '%s%s__lte' % (FILTER_PREFIX, field_path)
        # 转换为时间戳
        if params.get(self.lookup_kwarg_since):
            self.lookup_kwarg_since_value = int(time.mktime(time.strptime(params[self.lookup_kwarg_since], "%Y-%m-%d")))
        if params.get(self.lookup_kwarg_upto):
            self.lookup_kwarg_upto_value = int(time.mktime(time.strptime(params[self.lookup_kwarg_upto], "%Y-%m-%d")))

        super(DateRangeFilter, self).__init__(
            field, request, params, model, model_admin, field_path)
        self.form = self.get_form(request)

    def choices(self, cl):
        """
        Pop the original parameters, and return the date filter & other filter
        parameters.
        """
        qryParam = {'get_query': cl.params}
        ks = cl.params.pop(self.lookup_kwarg_since, None)
        if ks:
            qryParam['get_query'][self.lookup_kwarg_since] = ks
        ku = cl.params.pop(self.lookup_kwarg_upto, None)
        if ku:
            qryParam['get_query'][self.lookup_kwarg_upto] = ku
        return (qryParam)

    def queryset(self, request, queryset):
        if hasattr(self, "lookup_kwarg_since_value"):
            print(self.lookup_kwarg_since_value)
            queryset = queryset.filter(create_time__gte=self.lookup_kwarg_since_value)
        if hasattr(self, "lookup_kwarg_upto_value"):
            print(self.lookup_kwarg_upto)
            print(self.lookup_kwarg_upto_value)
            queryset = queryset.filter(create_time__lte=self.lookup_kwarg_upto_value)
        return queryset


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["id", "question_text", "pub_date"]
    search_fields = ["question_text"]
    list_filter = [("pub_date", DateRangeFilter)]


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ["id", "question", "choice_text", "votes"]
    search_fields = ["question__question_text", "choice_text"]

@admin.register(Clubs)
class ClubsAdmin(admin.ModelAdmin):
    list_display = ["uuid", "user_name", "password", "password2", "show_expired_time", "cost_mode", "cost_param", "profit", "refresh_time"]
    search_fields = ["uuid", "user_name", "cost_param"]
    list_filter = ["cost_mode"]
    ordering = ["-expired_time"]
    readonly_fields = ["expired_time", "profit", "refresh_time"]

    def show_expired_time(self, obj):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(obj.expired_time))
    show_expired_time.short_description = "过期时间"

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ["id", "club", "wechat_id", "wechat_uuid", "wechat_nick_name", "nick_name", "current_score", "history_profit", "history_cost", "introducer", "today_hoster_number", "score_limit", "score_limit_desc", "is_del", "is_bind"]
    search_fields = ["club__user_name", "wechat_uuid", "wechat_nick_name", "nick_name", "score_limit_desc"]
    list_filter = ["is_del", "is_bind"]
    readonly_fields = ["club", "wechat_id", "wechat_uuid", "wechat_nick_name", "nick_name", "current_score", "history_profit", "history_cost", "introducer", "today_hoster_number", "is_del", "is_bind"]

# @admin.register(PlayerClearCost)
# class PlayerClearCost(admin.ModelAdmin):
#     list_display = ["id", "player_id", "history_cost", "create_time"]

@admin.register(GameID)
class GameIdAdmin(admin.ModelAdmin):
    list_display = ["id", "player", "club", "game_nick_name", "gameid"]
    search_fields = ["player__nick_name", "club__user_name", "game_nick_name", "gameid"]
    readonly_fields = ["player", "club", "game_nick_name", "gameid"]

@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ["id", "player", "score", "cost", "is_host", "create_time", "room_id", "refresh_time"]
    search_fields = ["player__nick_name", "room_id"]
    list_filter = ["is_host"]
    readonly_fields = ["player", "score", "cost", "is_host", "create_time", "room_id", "refresh_time"]
    ordering = ["refresh_time"]

@admin.register(HistoryGame)
class HistoryGameAdmin(admin.ModelAdmin):
    list_display = ["id", "club", "room_id", "hoster_name", "hoster_id", "round_number", "start_time", "create_time", "cost", "score", "refresh_time"]
    search_fields = ["club__user_name", "hoster_name", "hoster_id"]
    readonly_fields = ["club", "room_id", "hoster_name", "hoster_id", "round_number", "start_time", "player_data", "create_time", "cost", "score", "refresh_time"]
    ordering = ["-refresh_time"]

# @admin.register(HistoryGameClearCost)
# class HistoryGameClearCostAdmin(admin.ModelAdmin):
#     list_display = ["id", "history_id", "cost", "create_time"]

@admin.register(Cdkey)
class CdkeyAdmin(admin.ModelAdmin):
    list_display = ["cdkey", "key_type", "status", "show_create_time"]
    search_fields = ["cdkey"]
    list_filter = ["key_type", "status", ("create_time", DateStampRangeFilter)]
    readonly_fields = ["cdkey", "key_type", "status", "create_time"]

    ordering = ("-create_time",)

    def show_create_time(self, obj):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(obj.create_time))
    show_create_time.short_description = "创建时间"

@admin.register(WrongImage)
class WrongImageAdmin(admin.ModelAdmin):
    list_display = ["id", "club_name", "image", "show_create_time"]
    search_fields = ["club_name"]
    readonly_fields = ["club_name", "image", "create_time"]

    def show_create_time(self, obj):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(obj.create_time))

    show_create_time.short_description = "创建时间"

@admin.register(ScoreChange)
class ScoreChangeAdmin(admin.ModelAdmin):
    list_display = ["id", "player", "score", "agent", "ip", "show_create_time"]
    search_fields = ["player__nick_name", "ip"]
    list_filter = ["agent"]
    readonly_fields = ["id", "player", "score", "agent", "ip", "create_time"]
    ordering = ("-create_time",)

    def show_create_time(self, obj):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(obj.create_time))

    show_create_time.short_description = "创建时间"

@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ["id", "club", "wechat_nick_name", "nick_name", "show_create_time"]
    search_fields = ["club__user_name", "wechat_nick_name", "nick_name"]

    readonly_fields = ["create_time"]


    def show_create_time(self, obj):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(obj.create_time))

    show_create_time.short_description = "创建时间"
    # def get_time(self):
    #     return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.create_time))
