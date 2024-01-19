# Generated by Django 5.0 on 2024-01-18 23:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Section',
            fields=[
                ('section_id', models.AutoField(primary_key=True, serialize=False)),
                ('section_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Tile',
            fields=[
                ('tile_id', models.AutoField(primary_key=True, serialize=False)),
                ('text', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Board',
            fields=[
                ('board_id', models.AutoField(primary_key=True, serialize=False)),
                ('board_name', models.CharField(max_length=20)),
                ('dimension', models.IntegerField(default=5)),
                ('active', models.BooleanField(default=True)),
                ('expiry_date', models.DateTimeField(default=False)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BingoBackend.section')),
            ],
        ),
        migrations.CreateModel(
            name='BoardTile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BingoBackend.board')),
                ('tile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BingoBackend.tile')),
            ],
        ),
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('username', models.CharField(max_length=100)),
                ('num_wins', models.IntegerField(default=0)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BingoBackend.section')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BoardTileUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position_row', models.IntegerField()),
                ('position_col', models.IntegerField()),
                ('selected', models.BooleanField(default=False)),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BingoBackend.board')),
                ('tile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BingoBackend.tile')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='boardtile',
            constraint=models.UniqueConstraint(fields=('board_id', 'tile_id'), name='unique_board_tile_combination'),
        ),
    ]
