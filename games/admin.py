from django.contrib import admin
from .models import PlayerProfile, GameScore

@admin.register(PlayerProfile)
class PlayerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_score', 'games_played')
    search_fields = ('user__username',)

@admin.register(GameScore)
class GameScoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'game_name', 'score', 'played_at')
    list_filter = ('game_name', 'played_at')
    search_fields = ('user__username',)
