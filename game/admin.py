# -*- coding: utf-8 -*-
from django.contrib import admin
from game.models import Game, Competition, GameTeamSubmit, ProgrammingLanguage, DockerContainer
from mezzanine.core import admin as mezzanineAdmin

admin.site.register(Competition)
admin.site.register(DockerContainer)
admin.site.register(ProgrammingLanguage)


class SubmitInline(mezzanineAdmin.StackedDynamicInlineAdmin):
    model = GameTeamSubmit


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    inlines = (SubmitInline,)

    fieldsets = ((None, {"fields": ("title", "competition", "pre_games")}),)
    list_display = ("title", "competition")
    list_display_links = ("title", "competition")
    list_editable = ()
    list_filter = ("title", "competition")
    search_fields = ("title",)


# class GameInline(admin.StackedInline):
#     model = Game


@admin.register(GameTeamSubmit)
class GameTeamSubmitAdmin(admin.ModelAdmin):
    list_display = ('submit', 'game', 'score')
    # inlines = [GameInline]