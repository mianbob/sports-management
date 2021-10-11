from django.contrib import admin
from cricket.models import *

admin.site.register(CustomUser)
admin.site.register(Venue)
admin.site.register(CricketTournament)
admin.site.register(RegisteredTeam)
admin.site.register(MatchSchedule)
admin.site.register(MatchPlayedByTeam)
admin.site.register(PointsTable)
admin.site.register(MatchStatistics)
