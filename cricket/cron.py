from django_cron import CronJobBase, Schedule
from cricket.models import *


class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 120  # every 2 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'cricket.my_cron_job'    # a unique code

    def do(self):
        listofalltournaments = CricketTournament.objects.all()
        for select in listofalltournaments:
            tournamentinstance = CricketTournament.objects.get(pk=select.id)
            matchschedulelist = MatchSchedule.objects.filter(
                event=tournamentinstance)
            countervaluechecker = 0
            for select2 in matchschedulelist:
                if select2.status != "ResultAvailable":
                    countervaluechecker = countervaluechecker + 1

                date = "2018-04-05"

            if countervaluechecker < 1:
                pointstableinsance = PointsTable.objects.filter(
                    tournament=tournamentinstance).order_by('-points')
                matchno = tournamentinstance.id

                matchinstance1 = MatchSchedule(event=tournamentinstance, date=date, venue="Gcu ground", matchNo=matchno,
                                               status="Semi Final")
                matchinstance1.save()

                matchinstance2 = MatchSchedule(event=tournamentinstance, date=date, venue="Gcu ground", matchNo=matchno,
                                               status="Semi Final")
                matchinstance2.save()
                counter = 1
                for select in pointstableinsance:
                    teaminstance = CricketTeam.objects.get(user=select.teams)
                    if counter == 1:
                        matchinstance1.teams.add(teaminstance)
                        matchinstance1.save()
                        counter = counter + 1
                    else:
                        if counter == 2:
                            matchinstance1.teams.add(teaminstance)
                            matchinstance1.save()
                            counter = counter + 1

                        else:
                            if counter == 3:
                                matchinstance2.teams.add(teaminstance)
                                matchinstance2.save()
                                counter = counter + 1

                            else:
                                if counter == 4:
                                    matchinstance2.teams.add(teaminstance)
                                    matchinstance2.save()
                                    counter = counter + 1


class MyCronJobFinalMatch(CronJobBase):
    RUN_EVERY_MINS = 120  # every 2 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'cricket.my_cron_job_final_match'    # a unique code

    def do(self):
        listofalltournaments = CricketTournament.objects.all()
        for select in listofalltournaments:
            tournamentinstance = CricketTournament.objects.get(pk=select.id)
            matchschedulelist = MatchSchedule.objects.filter(
                event=tournamentinstance).filter(status="Semi Final Results")
            countervaluechecker = 0
            for select2 in matchschedulelist:
                if select2.status != "Semi Final Results":
                    countervaluechecker = countervaluechecker + 1

            date = "2018-04-05"

            if countervaluechecker < 1:
                pointstableinsance = PointsTable.objects.filter(
                    tournament=tournamentinstance).order_by('points')
                matchno = tournamentinstance.id + 1

                matchinstance = MatchSchedule(event=tournamentinstance, date=date, venue="Gcu ground", matchNo=matchno,
                                              status="Final")
                matchinstance.save()

                counter = 1
                for select in pointstableinsance:
                    teaminstance = CricketTeam.objects.get(user=select.teams)
                    if counter == 1:
                        matchinstance.teams.add(teaminstance)
                        matchinstance.save()
                        counter = counter + 1
                    else:
                        if counter == 2:
                            matchinstance.teams.add(teaminstance)
                            matchinstance.save()
                            counter = counter + 1
