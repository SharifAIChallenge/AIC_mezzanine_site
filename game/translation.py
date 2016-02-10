from modeltranslation.translator import translator, TranslationOptions
from .models import GameTeamSubmit


class TranslatedGameTeamSubmit(TranslationOptions):
    fields = ()

translator.register(GameTeamSubmit, TranslatedGameTeamSubmit)

