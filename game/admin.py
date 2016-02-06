# -*- coding: utf-8 -*-
from django.contrib import admin
from game.models import Game, Competition, GameTeamSubmit
from mezzanine.core import admin as mezzanineAdmin

admin.site.register(Competition)


class SubmitInline(mezzanineAdmin.StackedDynamicInlineAdmin):
    model = GameTeamSubmit


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    inlines = (SubmitInline,)

    fieldsets = ((None, {"fields": ("title", "competition", "config", "pre_games")}),)
    list_display = ("title", "competition", "config")
    list_display_links = ("title", "competition", "config")
    list_editable = ()
    list_filter = ("title", "competition", "config")
    search_fields = ("title",)


class GameInline(admin.StackedInline):
    model = Game


@admin.register(GameTeamSubmit)
class GameTeamSubmitAdmin(admin.ModelAdmin):
    list_display = ('submit', 'game', 'score')
    inlines = [GameInline]