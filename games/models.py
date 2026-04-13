from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class PlayerProfile(models.Model):
    """
    Player profile to track user's gaming statistics.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    total_score = models.IntegerField(default=0)
    games_played = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - Score: {self.total_score}"

    class Meta:
        ordering = ['-total_score']


class GameScore(models.Model):
    """
    Record of individual game scores.
    """
    GAME_CHOICES = [
        ('fizzbuzz', 'FizzBuzz'),
        ('tictactoe', 'TicTacToe'),
        ('chess', 'Chess'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='game_scores')
    game_name = models.CharField(max_length=50, choices=GAME_CHOICES)
    score = models.IntegerField()
    played_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.game_name}: {self.score}"

    class Meta:
        ordering = ['-played_at']


# Signal to automatically create PlayerProfile when a new User is created
@receiver(post_save, sender=User)
def create_player_profile(sender, instance, created, **kwargs):
    if created:
        PlayerProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_player_profile(sender, instance, **kwargs):
    instance.profile.save()
