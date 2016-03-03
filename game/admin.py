# -*- coding: utf-8 -*-
from django.contrib import admin
from game.models import Game, Competition, GameTeamSubmit, ProgrammingLanguage, DockerContainer, GameConfiguration, \
    TeamScore, Group, GroupTeamSubmit, GamePlace, DoubleEliminationTeamProxy, DoubleEliminationGroup
from mezzanine.core import admin as mezzanineAdmin

admin.site.register(Competition)
admin.site.register(DockerContainer)
admin.site.register(ProgrammingLanguage)
admin.site.register(DoubleEliminationGroup)


class DoubleEliminationTeamProxyAdmin(admin.ModelAdmin):
    list_display = ('group', 'score', 'team')


admin.site.register(DoubleEliminationTeamProxy, DoubleEliminationTeamProxyAdmin)


class SubmitInline(mezzanineAdmin.StackedDynamicInlineAdmin):
    model = GameTeamSubmit


class GameAdmin(admin.ModelAdmin):
    inlines = (SubmitInline,)

    fieldsets = ((None, {"fields": ("title", "pre_games", "log_file", "error_log", "status",
                                    "game_type", "game_config")}),
                 ('advanced', {'fields': (
                     'time', 'place', 'group', 'counted_in_group', 'double_elimination_group',
                     'counted_in_double_elimination_group')}))
    list_display = ("title", "status", "game_type", "game_config", "get_log_link")
    list_display_links = ("title", "status", "game_type", "game_config")
    list_editable = ()
    list_filter = ("status", "game_type", "game_config")
    search_fields = ("title",)


admin.site.register(Game, GameAdmin)

admin.site.register(GamePlace)


class GameTeamSubmitAdmin(admin.ModelAdmin):
    list_display = ('submit', 'game', 'score')


admin.site.register(GameTeamSubmit, GameTeamSubmitAdmin)


class GameConfigurationAdmin(mezzanineAdmin.BaseTranslationModelAdmin):
    fieldsets = ((None, {"fields": ("competition", "config", "description", "is_public")}),)
    list_display = ("competition", "config", "description", "is_public")
    list_display_links = ("competition", "config", "description")
    list_editable = ("is_public",)
    list_filter = ("competition", "config", "description", "is_public")
    search_fields = ("description",)


admin.site.register(GameConfiguration, GameConfigurationAdmin)


class TeamScoreAdmin(admin.ModelAdmin):
    fieldsets = ((None, {"fields": ("team", "score", "game_type")}),)
    list_display = ("team", "score", "game_type")
    list_display_links = ("team", "score", "game_type")
    list_editable = ()
    list_filter = ("team", "score", "game_type")
    search_fields = ("team", "score")


admin.site.register(TeamScore, TeamScoreAdmin)
admin.site.register(Group)
admin.site.register(GroupTeamSubmit)
