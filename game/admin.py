# -*- coding: utf-8 -*-
from django.contrib import admin
from game.models import Game, Competition, GameTeamSubmit, ProgrammingLanguage, DockerContainer, GameConfiguration
from mezzanine.core import admin as mezzanineAdmin

admin.site.register(Competition)
admin.site.register(DockerContainer)
admin.site.register(ProgrammingLanguage)


class SubmitInline(mezzanineAdmin.StackedDynamicInlineAdmin):
    model = GameTeamSubmit


class GameAdmin(admin.ModelAdmin):
    inlines = (SubmitInline,)

    fieldsets = ((None, {"fields": ("title", "pre_games")}),)
    list_display = ("title",)
    list_display_links = ("title",)
    list_editable = ()
    list_filter = ("title",)
    search_fields = ("title",)

admin.site.register(Game, GameAdmin)


# class GameInline(admin.StackedInline):
#     model = Game


@admin.register(GameTeamSubmit)
class GameTeamSubmitAdmin(admin.ModelAdmin):
    list_display = ('submit', 'game', 'score')
    # inlines = [GameInline]


class GameConfigurationAdmin(mezzanineAdmin.BaseTranslationModelAdmin):
    fieldsets = ((None, {"fields": ("competition", "config", "description", "is_public")}),)
    list_display = ("competition", "config", "description", "is_public")
    list_display_links = ("competition", "config", "description")
    list_editable = ("is_public", )
    list_filter = ("competition", "config", "description", "is_public")
    search_fields = ("description",)

admin.site.register(GameConfiguration, GameConfigurationAdmin)