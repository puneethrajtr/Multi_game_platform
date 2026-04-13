from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamescore',
            name='game_name',
            field=models.CharField(
                choices=[
                    ('fizzbuzz', 'FizzBuzz'),
                    ('tictactoe', 'TicTacToe'),
                    ('chess', 'Chess'),
                ],
                max_length=50,
            ),
        ),
    ]
