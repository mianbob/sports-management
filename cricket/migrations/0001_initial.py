# Generated by Django 3.2.7 on 2021-10-01 22:41

import cricket.models
import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_cricket_team', models.BooleanField(default=False)),
                ('is_footbal_team', models.BooleanField(default=False)),
                ('is_scorer', models.BooleanField(default=False)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', cricket.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='ContactUS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('subject', models.CharField(max_length=32)),
                ('email', models.CharField(max_length=32)),
                ('query', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='CricketTournament',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('logo', models.ImageField(upload_to='eventlogo')),
                ('venue1', models.CharField(max_length=50)),
                ('venue2', models.CharField(max_length=50)),
                ('venue3', models.CharField(max_length=50)),
                ('deadlineforregistration', models.DateField(default=datetime.date.today, verbose_name='Date')),
                ('criteria', models.CharField(max_length=200)),
                ('overs', models.IntegerField()),
            ],
            options={
                'verbose_name_plural': 'CricketTournmanet',
            },
        ),
        migrations.CreateModel(
            name='MatchPlayedByTeam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='MatchSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matchNo', models.IntegerField()),
                ('date', models.DateTimeField()),
                ('venue', models.CharField(max_length=32)),
                ('status', models.CharField(default='pending', max_length=32)),
                ('tossstatus', models.CharField(default='pending', max_length=32)),
            ],
            options={
                'verbose_name_plural': 'MatchSchedule',
            },
        ),
        migrations.CreateModel(
            name='MatchStatistics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('six', models.BooleanField(default=False)),
                ('four', models.BooleanField(default=False)),
                ('zero', models.BooleanField(default=False)),
                ('one', models.BooleanField(default=False)),
                ('two', models.BooleanField(default=False)),
                ('three', models.BooleanField(default=False)),
                ('runout', models.BooleanField(default=False)),
                ('wicket', models.BooleanField(default=False)),
                ('extra', models.BooleanField(default=False)),
                ('noball', models.BooleanField(default=False)),
                ('wide', models.BooleanField(default=False)),
                ('legalball', models.BooleanField(default=False)),
                ('bowlername', models.CharField(max_length=32)),
                ('batsmanname', models.CharField(max_length=32)),
                ('catchby', models.CharField(max_length=32)),
                ('runoutby', models.CharField(max_length=32)),
                ('innings', models.IntegerField()),
                ('legbye', models.BooleanField(default=False)),
                ('extrarun', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'MatchStatistics',
            },
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32)),
                ('notice', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32)),
                ('notification', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='PointsTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Venue',
            },
        ),
        migrations.CreateModel(
            name='RegisteredTeam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teamname', models.CharField(max_length=32)),
                ('contactno', models.IntegerField(default=0)),
                ('status', models.CharField(default='pending', max_length=32)),
                ('cricketevent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cricket.crickettournament')),
            ],
            options={
                'verbose_name_plural': 'RegisteredTeam',
            },
        ),
    ]