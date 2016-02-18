from modeltranslation.translator import translator, TranslationOptions
from .models import GameTeamSubmit, GameConfiguration


class TranslatedGameTeamSubmit(TranslationOptions):
    fields = ()

translator.register(GameTeamSubmit, TranslatedGameTeamSubmit)


class TranslatedGameConfiguration(TranslationOptions):
    fields = ('description', )

translator.register(GameConfiguration, TranslatedGameConfiguration)

