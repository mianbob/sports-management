from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from cricket.models import *
from django.http import JsonResponse
try:
    import json
except:
    import django.utils.simplejson as json

def ballbyball(request, matchid):
    matchinstance = MatchSchedule.objects.get(pk=matchid)
    matchplayedby = MatchPlayedByTeam.objects.get(matchId=matchinstance.id)
    eventno = matchinstance.event
    eventinstance = CricketTournament.objects.get(pk=eventno.id)
    eventballs = eventinstance.overs * 6
    firstteam = matchplayedby.firstteam
    secondteam = matchplayedby.secondteam
    battingteam = matchplayedby.battingteam
    if battingteam == firstteam:
        firstinningsteam = firstteam
        secondinningsteam = secondteam
    else:
        firstinningsteam = secondteam
        secondinningsteam = firstteam
    teaminstance1 = CricketTeam.objects.get(pk=firstinningsteam)
    teaminstance2 = CricketTeam.objects.get(pk=secondinningsteam)
    latestover = 1
    latestball = 1
    if matchinstance.status == 'pending':
        totalball = MatchStatistics.objects.filter(matchId=matchinstance).filter(legalball=True).filter(innings=1)
        totalballs = len(totalball)
        if (totalballs >= eventballs):
            matchinstance.status = 'secondinnings'
            matchinstance.save()
        overno = totalballs/6
        convertingint = int(overno)
        latestover = convertingint + 1
        ballno = totalballs%6
        latestball = ballno+1

    if matchinstance.status == 'secondinnings':
        totalball = MatchStatistics.objects.filter(matchId=matchinstance).filter(legalball=True).filter(innings=2)
        totalballs = len(totalball)
        overno = totalballs/6
        convertingint = int(overno)
        latestover = convertingint + 1
        ballno = totalballs%6
        latestball = ballno+1



    if latestball != 1:
        matchstatisticschecker = MatchStatistics.objects.all().last()
        bowlername = matchstatisticschecker.bowlername
    else:
        bowlername = ""

    context = {
        'match':matchinstance,
        'firstteam':firstteam,
        'secondteam':secondteam,
        'teamins1':teaminstance1,
        'teamins2':teaminstance2,
        'overno':latestover,
        'ballno':latestball,
        'bowlername':bowlername
    }
    return render(request, 'cricket/ball.html', context)

def index(request):
    return render(request, 'cricket/base.html')

def matchstatitics(request, matchid):
    matchstats = MatchStatistics.objects.filter(matchId=matchid)

    firstiningplayerswicket = MatchStatistics.objects.filter(matchId=matchid).filter(innings=1).filter\
        (wicket=True).filter(legalball=True)
    firstinninglbw = MatchStatistics.objects.filter(matchId=matchid).filter(innings=1).filter \
        (extra=True).filter(legalball=False).filter(legbye=True)
    firstinningwide = MatchStatistics.objects.filter(matchId=matchid).filter(innings=1).filter \
        (extra=True).filter(wide=True).filter(legalball=False)

    totalballsinfirstinning = MatchStatistics.objects.filter(matchId=matchid).filter(innings=1).filter(legalball=True)
    oversfirstcheck = int(len(totalballsinfirstinning) / 6)
    oversfirstagaincheck = int(len(totalballsinfirstinning) - (oversfirstcheck*6))
    stringtotalfirstinning = str(len(firstiningplayerswicket))+" wickets, " \
                             + str(oversfirstcheck) + "." + str(oversfirstagaincheck) + " overs"
    stringextrafirstinning = 'lbw'+str(len(firstinninglbw))+" ,w"+str(len(firstinningwide))

    firstinningextras = MatchStatistics.objects.filter(matchId=matchid).filter(innings=1).filter\
        (extra=True).filter(legalball=False)
    totalextrarun = len(firstinningextras)

    one = len(firstinningextras.filter(one=True))
    two = len(firstinningextras.filter(two=True))
    three = len(firstinningextras.filter(three=True))
    four = len(firstinningextras.filter(four=True))
    six = len(firstinningextras.filter(six=True))

    totalfirstextra = ((one * 1) + (two * 2) + (three * 3) + (four * 4) + (six * 6)) + totalextrarun

    firstplayerslist = []
    firstinning = MatchStatistics.objects.filter(matchId=matchid).filter(innings=1)

    for select in firstinning:
        newvariable = select.batsmanname
        if newvariable not in firstplayerslist:
            firstplayerslist.append(select.batsmanname)

    firstscorerunlist = []
    counter = 1
    for select in firstplayerslist:
        firstobj = MatchStatistics.objects.filter(matchId=matchid).filter(innings=1).filter(
        batsmanname=select).filter(wicket=False).filter(wide=False).filter(extra=False).\
        filter(legbye=False).filter(legalball=True)

        one = len(firstobj.filter(one=True))
        two = len(firstobj.filter(two=True))
        three= len(firstobj.filter(three=True))
        four = len(firstobj.filter(four=True))
        six = len(firstobj.filter(six=True))

        if MatchStatistics.objects.filter(matchId=matchid).filter(innings=1).filter(batsmanname=select).filter(wicket=True).exists():
            if MatchStatistics.objects.filter(matchId=matchid).filter(innings=1).filter(batsmanname=select).filter(
                wicket=True).filter(runout=True).exists():
                    runout = MatchStatistics.objects.filter(matchId=matchid).filter(innings=1).filter(batsmanname=select).filter(
                    wicket=True).filter(runout=True)
                    if runout[0].runoutby != "":
                        obj = runout[0].runoutby
                    else:
                        obj = ''
                    stringv = "runout by "+str(obj)+""
            if MatchStatistics.objects.filter(matchId=matchid).filter(innings=1).filter(batsmanname=select).filter(
                wicket=True).filter(catchby=True).exists():
                catout = MatchStatistics.objects.filter(matchId=matchid).filter(innings=1).filter(
                    batsmanname=select).filter(wicket=True).filter(catchby=True)
                if catout[0].catchby != "":
                    obj = catout[0].catchby
                else:
                    obj = ''
                if catout[0].bowlername != "":
                    obj2 = catout[0].bowlername
                else:
                    obj2 = ''
                stringv = "c " + str(obj) + "b " + str(obj2) + ""
            if MatchStatistics.objects.filter(matchId=matchid).filter(innings=1).filter(batsmanname=select).filter(
                wicket=True).exists():
                out = MatchStatistics.objects.filter(matchId=matchid).filter(innings=1).filter(
                batsmanname=select).filter(wicket=True)
                if out[0].bowlername != "":
                    obj2 = out[0].bowlername
                else:
                    obj2 = ''
                stringv = "b " + str(obj2) + ""
        else:
            stringv = 'Not Out'
        totalballs = len(firstobj)

        firstscorerunlist.append([counter,select,stringv,
                             ((one*1) + (two*2) + (three*3) + (four*4) + (six*6)),0,
                             totalballs,four,six])
        counter = counter + 1
    totaloffirstinning = 0
    for select in firstscorerunlist:
        totaloffirstinning = totaloffirstinning + select[3]
    totaloffirstinningfinal = totaloffirstinning + totalfirstextra
    averagefirstinningvariable = int(totaloffirstinningfinal / oversfirstcheck)
    stringaveragerun = str(averagefirstinningvariable) + ".0 runs per over"


    # bowling table first innings
    firstinningbowlerslist = []
    firstinningbowling = MatchStatistics.objects.filter(matchId=matchid).filter(innings=1)
    for select in firstinningbowling:
        newvariable = select.bowlername
        if newvariable not in firstinningbowlerslist:
            firstinningbowlerslist.append(select.bowlername)

    firstbowlertabledatalist = []
    for select in firstinningbowlerslist:
        firstobj = MatchStatistics.objects.filter(matchId=matchid).filter(innings=1).filter(bowlername=select)
        totallegalballs = len(firstobj.filter(legalball=True))
        overcheck = int(totallegalballs / 6)
        overcheckagain = int(totallegalballs - (overcheck * 6))
        stringv = str(overcheck) + "." + str(overcheckagain)

        one = len(firstobj.filter(one=True))
        two = len(firstobj.filter(two=True))
        three= len(firstobj.filter(three=True))
        four = len(firstobj.filter(four=True))
        six = len(firstobj.filter(six=True))
        wide = len(firstobj.filter(wide=True))
        wickets = len(firstobj.filter(wicket=True).filter(legalball=True))
        noball = len(firstobj.filter(noball=True).filter(legalball=False))


        firstbowlertabledatalist.append([select,stringv,0,
                             ((one*1) + (two*2) + (three*3) + (four*4) + (six*6)),wickets,wide,noball])



    # details of second innings
    secondiningplayerswicket = MatchStatistics.objects.filter(matchId=matchid).filter(innings=2).filter \
        (wicket=True).filter(legalball=True)
    secondinninglbw = MatchStatistics.objects.filter(matchId=matchid).filter(innings=2).filter \
        (extra=True).filter(legalball=False).filter(legbye=True)
    secondinningwide = MatchStatistics.objects.filter(matchId=matchid).filter(innings=2).filter \
        (extra=True).filter(wide=True).filter(legalball=False)

    totalballsinsecondinning = MatchStatistics.objects.filter(matchId=matchid).filter(innings=2).filter(legalball=True)
    oversecondcheck = int(len(totalballsinsecondinning)/6)
    oversecondagaincheck = int(len(totalballsinsecondinning)-(oversecondcheck*6))
    stringtotalsecondinning = str(len(secondiningplayerswicket)) + " wickets, " + str(oversecondcheck)+"."\
                              +str(oversecondagaincheck) + " overs"
    stringextrasecondinning = 'lbw' + str(len(secondinninglbw)) + " ,w" + str(len(secondinningwide))

    secondinningextras = MatchStatistics.objects.filter(matchId=matchid).filter(innings=2).filter \
        (extra=True).filter(legalball=False)
    totalextrarunsecond = len(secondinningextras)

    one = len(secondinningextras.filter(one=True))
    two = len(secondinningextras.filter(two=True))
    three = len(secondinningextras.filter(three=True))
    four = len(secondinningextras.filter(four=True))
    six = len(secondinningextras.filter(six=True))

    totalsecondextra = ((one * 1) + (two * 2) + (three * 3) + (four * 4) + (six * 6)) + totalextrarunsecond

    secondplayerslist = []
    secondinning = MatchStatistics.objects.filter(matchId=matchid).filter(innings=2)

    for select in secondinning:
        newvariable = select.batsmanname
        if newvariable not in secondplayerslist:
            secondplayerslist.append(select.batsmanname)

    secondscorerunlist = []
    counter = 1
    for select in secondplayerslist:
        firstobj = MatchStatistics.objects.filter(matchId=matchid).filter(innings=2).filter(
            batsmanname=select).filter(wicket=False).filter(wide=False).filter(extra=False). \
            filter(legbye=False).filter(legalball=True)

        one = len(firstobj.filter(one=True))
        two = len(firstobj.filter(two=True))
        three = len(firstobj.filter(three=True))
        four = len(firstobj.filter(four=True))
        six = len(firstobj.filter(six=True))

        if MatchStatistics.objects.filter(matchId=matchid).filter(innings=2).filter(batsmanname=select).filter(
                wicket=True).exists():
            if MatchStatistics.objects.filter(matchId=matchid).filter(innings=2).filter(batsmanname=select).filter(
                    wicket=True).filter(runout=True).exists():
                runout = MatchStatistics.objects.filter(matchId=matchid).filter(innings=2).filter(
                    batsmanname=select).filter(
                    wicket=True).filter(runout=True)
                if runout[0].runoutby != "":
                    obj = runout[0].runoutby
                else:
                    obj = ''
                stringv = "runout by " + str(obj) + ""
            if MatchStatistics.objects.filter(matchId=matchid).filter(innings=2).filter(batsmanname=select).filter(
                    wicket=True).filter(catchby=True).exists():
                catout = MatchStatistics.objects.filter(matchId=matchid).filter(innings=2).filter(
                    batsmanname=select).filter(wicket=True).filter(catchby=True)
                if catout[0].catchby != "":
                    obj = catout[0].catchby
                else:
                    obj = ''
                if catout[0].bowlername != "":
                    obj2 = catout[0].bowlername
                else:
                    obj2 = ''
                stringv = "c " + str(obj) + "b " + str(obj2) + ""
            if MatchStatistics.objects.filter(matchId=matchid).filter(innings=2).filter(batsmanname=select).filter(
                    wicket=True).exists():
                out = MatchStatistics.objects.filter(matchId=matchid).filter(innings=2).filter(
                    batsmanname=select).filter(wicket=True)
                if out[0].bowlername != "":
                    obj2 = out[0].bowlername
                else:
                    obj2 = ''
                stringv = "b " + str(obj2) + ""
        else:
            stringv = 'Not Out'
        totalballs = len(firstobj)

        secondscorerunlist.append([counter, select, stringv,
                                  ((one * 1) + (two * 2) + (three * 3) + (four * 4) + (six * 6)), 0,
                                  totalballs, four, six])
        counter = counter + 1
    totalofsecondinning = 0
    for select in secondscorerunlist:
        totalofsecondinning = totalofsecondinning + select[3]
    totalofsecondinningfinal = totalofsecondinning + totalsecondextra
    averagesecondinningvariable = float(totalofsecondinningfinal / oversecondcheck)
    stringaveragerunsecond = str(averagesecondinningvariable) + " runs per over"

    # bowling table second innings
    secondinningbowlerslist = []
    secondinningbowling = MatchStatistics.objects.filter(matchId=matchid).filter(innings=2)
    for select in secondinningbowling:
        newvariable = select.bowlername
        if newvariable not in secondinningbowlerslist:
            secondinningbowlerslist.append(select.bowlername)

    secondbowlertabledatalist = []
    for select in secondinningbowlerslist:
        firstobj = MatchStatistics.objects.filter(matchId=matchid).filter(innings=2).filter(bowlername=select)
        totallegalballs = len(firstobj.filter(legalball=True))
        overcheck = int(totallegalballs / 6)
        overcheckagain = int(totallegalballs - (overcheck * 6))
        stringv = str(overcheck) + "." + str(overcheckagain)

        one = len(firstobj.filter(one=True))
        two = len(firstobj.filter(two=True))
        three = len(firstobj.filter(three=True))
        four = len(firstobj.filter(four=True))
        six = len(firstobj.filter(six=True))
        wide = len(firstobj.filter(wide=True))
        wickets = len(firstobj.filter(wicket=True).filter(legalball=True))
        noball = len(firstobj.filter(noball=True).filter(legalball=False))

        secondbowlertabledatalist.append([select, stringv, 0,
                                         ((one * 1) + (two * 2) + (three * 3) + (four * 4) + (six * 6)), wickets, wide,
                                         noball])

    context = {

        # first inning data
        'matchstats':matchstats,
        'scorelist':firstscorerunlist,
        'totalscorefirstinning':totaloffirstinningfinal,
        'totalextrafirstinning':totalextrarun,
        'extrastringfirstinning':stringextrafirstinning,
        'overwicketstringfirstinning':stringtotalfirstinning,
        'stringaveragerunfirstinning':stringaveragerun,
        'firstinningbowlingdata':firstbowlertabledatalist,

    #     second inning data
        'scorelistsecond': secondscorerunlist,
        'totalscoresecondinning': totalofsecondinningfinal,
        'totalextrasecondinning': totalextrarunsecond,
        'extrastringsecondinning': stringextrasecondinning,
        'overwicketsecondinning': stringtotalsecondinning,
        'stringaveragerunsecondinning': stringaveragerunsecond,
        'secondinningbowlingdata': secondbowlertabledatalist,

    }

    return render(request, 'cricket/matchstatistcs.html', context)

@user_passes_test(lambda u: u.is_staff ,login_url='members:login', redirect_field_name=None)
def teamapproval(request,tournamentid):
    currentevent = CricketTournament.objects.get(pk=tournamentid)
    allteams = RegisteredTeam.objects.filter(cricketevent=currentevent).filter(status="pending")
    context = {
        'allteams':allteams
    }
    return render(request, 'cricket/teamapprovalpage.html',context)

def handler404(request,expection,template_name='members/alertpage.html'):
    return render(request,template_name)

def handler500(request, *args, **argv):
    return render(request, 'members/alertpage.html', status=500)

def approvaltry(request):
    teamname = request.GET.get('teamname', None)
    teaminstance = CricketTeam.objects.get(teamname=teamname)
    eventinstance = CricketTournament.objects.last()
    datainstance = RegisteredTeam.objects.filter(cricketevent=eventinstance).filter(teamid=teaminstance)
    print(len(datainstance));
    for select in datainstance:
        select.status = "passed"
        select.save()
    registeredteampoints = PointsTable.objects.create(tournament=eventinstance, teams=teaminstance)
    registeredteampoints.save()
    data = {

        }
    return JsonResponse(data,safe=False)

def rejectiontry(request):
    teamname = request.GET.get('teamname', None)
    teaminstance = CricketTeam.objects.get(teamname=teamname)
    eventinstance = CricketTournament.objects.last()
    datainstance = RegisteredTeam.objects.filter(cricketevent=eventinstance).filter(teamid=teaminstance)
    for select in datainstance:
        select.status = "failed"
        select.save()
    data = {

        }
    return JsonResponse(data,safe=False)

def matchentry(request):
    if request.method == 'POST':
        matchno = request.POST['match']
        event = request.POST['event']
        team1 = request.POST['team1']
        team2 = request.POST['team2']
        date = request.POST['date']
        venue = request.POST['venue']
        eventinstance = CricketTournament.objects.get(name=event)
        userid1 = CustomUser.objects.get(email=team1)
        userid2 = CustomUser.objects.get(email=team2)
        team1instance = CricketTeam.objects.get(user=userid1)
        team2instance = CricketTeam.objects.get(user=userid2)
        if team1instance == "":
            print ("Ali")


        if ( team1 != '' and team2 != '' and date !='' and venue != ""):
            if (team1 != team2):
                matchinstance = MatchSchedule(event=eventinstance,date=date,venue=venue,matchNo=matchno)
                matchinstance.save()
                matchinstance.teams.add(team1instance)
                matchinstance.save()
                matchinstance.teams.add(team2instance)
                matchinstance.save()
                title = "New Match"
                notification = "Your Match Is Conducted With "+str(team1instance.teamname)+" at "+str(date)
                notificationinstance = Notification(title=title, notification=notification, team=team2instance)
                notificationinstance.save()

                notification = "Your Match Is Conducted With " + str(team2instance.teamname) + " at " + str(date)
                notificationinstance = Notification(title=title, notification=notification, team=team1instance)
                notificationinstance.save()

                data = {
                            'message':'Match Is Entered'
                    }
                return JsonResponse(data,safe=False)
            else:
                data = {
                    'message': 'Sorry Please Provide All Fields'
                }
                return JsonResponse(data, safe=False)
        else:
            data = {
                'message': 'Sorry Please Provide All Fields'
            }
            return JsonResponse(data, safe=False)

def tournament(request, tournamentid):
    matches = MatchSchedule.objects.filter(event=tournamentid)
    cricketevent = CricketTournament.objects.get(id=tournamentid)
    teamsinstance = RegisteredTeam.objects.filter(cricketevent=cricketevent).filter(status="passed")


    semifinalchecker = MatchSchedule.objects.filter(event=tournamentid).filter(status="Semi Final")
    if semifinalchecker.exists():
        checker = "Semi Final Exists"
    else:
        checker = "Dont Exists"

    context = {
        'semifinalvalues':semifinalchecker,
        'matches':matches,
        'teams':teamsinstance,
        'cricket':cricketevent,
        'semifinalchecker':checker
    }
    return render(request, 'cricket/tournament.html', context)

def matchschedule(request, tournamentid):
    cricketevent = CricketTournament.objects.get(id=tournamentid)
    teamsinstance = RegisteredTeam.objects.filter(cricketevent=cricketevent).filter(status="passed")
    matchcount = MatchSchedule.objects.filter(event=tournamentid).count()
    addedno = matchcount+1

    context = {
        'teams':teamsinstance,
        'cricketevent':cricketevent,
        'matchcount': addedno
    }
    return render(request, 'cricket/matchschedule.html', context)

def eventdisplay(request):
    cricketevent = CricketTournament.objects.all().order_by('-id')
    context = {
        'cricketevent':cricketevent
    }
    return render(request, 'cricket/EventDisplaypage.html', context)

def editevent(request):
    eventid = request.GET.get('eventid', None)
    eventinstance = CricketTournament.objects.get(pk=eventid)
    data = {
            'eventname':eventinstance.name,
            'eventdate':eventinstance.deadlineforregistration,
            'eventvenue':eventinstance.venue1,
            'eventid':eventid
        }
    return JsonResponse(data,safe=False)

def updatematch(request):
    matchid = request.GET.get('matchid', None)
    team1 = request.GET.get('team1', None)
    team2 = request.GET.get('team2', None)
    date = request.GET.get('date', None)
    venue = request.GET.get('venue', None)
    userid1 = CustomUser.objects.get(email=team1)
    userid2 = CustomUser.objects.get(email=team2)
    team1instance = CricketTeam.objects.get(user=userid1.id)
    team2instance = CricketTeam.objects.get(user=userid2.id)


    if (team1 != '' and team2 != '' and date != '' and venue != ""):
        if (team1 != team2):
            matchinstance = MatchSchedule.objects.get(pk=matchid)
            counter = 0
            for select in matchinstance.teams.all():
                matchinstance.teams.remove(select)

            matchinstance.teams.add(team1instance)
            matchinstance.save()
            matchinstance.teams.add(team2instance)
            matchinstance.save()
            matchinstance.date = date
            matchinstance.save()
            matchinstance.venue = venue
            matchinstance.save()

            data = {
                'message': 'Match Is Updated'
            }
            return JsonResponse(data, safe=False)
        else:
            data = {
                'message': 'Sorry Please Provide All Fields'
            }
            return JsonResponse(data, safe=False)
    else:
        data = {
            'message': 'Sorry Please Provide All Fields'
        }
        return JsonResponse(data, safe=False)

def updateevent(request):
    eventid = request.GET.get('eventid', None)
    eventname = request.GET.get('eventname', None)
    eventdate = request.GET.get('edate', None)
    eventven = request.GET.get('even', None)
    eventinstance = CricketTournament.objects.get(pk=eventid)
    if eventname == "":
        eventname = eventinstance.name
    if eventdate == "":
        eventdate = eventinstance.deadlineforregistration
    if eventven == "":
        eventven = eventinstance.venue1

    eventinstance.name = eventname
    eventinstance.save()
    eventinstance.deadlineforregistration=eventdate
    eventinstance.save()
    eventinstance.venue1=eventven
    eventinstance.save()
    data = {

        }
    return JsonResponse(data,safe=False)

def ballentry(request):
    if request.method == 'POST':
        selectedtype = request.POST['selectedtype']
        try:
            scorerun = request.POST['scorerun']
        except:
            scorerun = ''
        try:
            scorebat = request.POST['scorebat']
        except:
            scorebat = ''
        try:
            extrafirst = request.POST['extrafirst']
        except:
            extrafirst = ''
        try:
            extrabye = request.POST['extrabye']
        except:
            extrabye = ''
        try:
            extrawide = request.POST['extrawide']
        except:
            extrawide = ''
        extranobat = request.POST['extranobat']
        try:
            extranorun = request.POST['extranorun']
        except:
            extranorun = ''
        try:
            wickettype = request.POST['wicketype']
        except:
            wickettype = ''
        try:
            wicketrunoutbat = request.POST['wicketrunoutbat']
        except:
            wicketrunoutbat = ''
        try:
            wicketrunoutball = request.POST['wicketrunoutball']
        except:
            wicketrunoutball = ''
        try:
            wicketcatbat = request.POST['wicketcatbat']
        except:
            wicketcatbat = ''
        try:
            wicketcatball = request.POST['wicketcatball']
        except:
            wicketcatball = ''
        try:
            wicketbat = request.POST['wicketbat']
        except:
            wicketbat = ''
        matchidi = request.POST['matchid']
        matchid = MatchSchedule.objects.get(pk=matchidi)
        eventno = matchid.event
        eventinstance = CricketTournament.objects.get(pk=eventno.id)
        eventballs = eventinstance.overs * 6
        totalball = MatchStatistics.objects.filter(matchId=matchid).filter(legalball=True)
        totalballs = len(totalball)
        inning = 1
        if (totalballs > eventballs):
            matchid.status = 'secondinnings'
            inning = 2

        bowler = request.POST['bowler']
        if selectedtype == '1':
            instanc = MatchStatistics.objects.create(matchId=matchid,legalball=True,batsmanname=scorebat,
                                                     innings=inning,bowlername=bowler)
            instanc.save()
            if scorerun == '0':
                instanc.zero = True
                instanc.save()
            if scorerun == '1':
                instanc.one = True
                instanc.save()
            if scorerun == '2':
                instanc.two = True
                instanc.save()
            if scorerun == '3':
                instanc.three = True
                instanc.save()
            if scorerun == '4':
                instanc.four = True
                instanc.save()
            if scorerun == '6':
                instanc.six = True
                instanc.save()
            data = {
                'message': 'Entered'
            }
            return JsonResponse(data, safe=False)

        if selectedtype == '2':
            if extrafirst == '1':
                instanc = MatchStatistics.objects.create(matchId=matchid,
                                                         innings=inning, bowlername=bowler,
                                                         legbye = True,extra=True)
                instanc.save()
                if extrabye == '0':
                    instanc.zero = True
                    instanc.save()
                if extrabye == '1':
                    instanc.one = True
                    instanc.save()
                if extrabye == '2':
                    instanc.two = True
                    instanc.save()
                if extrabye == '3':
                    instanc.three = True
                    instanc.save()
                if extrabye == '4':
                    instanc.four = True
                    instanc.save()
                if extrabye == '6':
                    instanc.six = True
                    instanc.save()
                data = {
                    'message': 'Entered'

                }
                return JsonResponse(data, safe=False)

            if extrafirst == '3':
                instanc = MatchStatistics.objects.create(matchId=matchid,
                                                         innings=inning, bowlername=bowler,
                                                         wide = True, extra=True, extrarun=1)
                instanc.save()
                if extrawide == '0':
                    instanc.zero = True
                    instanc.save()
                if extrawide == '1':
                    instanc.one = True
                    instanc.save()
                if extrawide == '2':
                    instanc.two = True
                    instanc.save()
                if extrawide == '3':
                    instanc.three = True
                    instanc.save()
                if extrawide == '4':
                    instanc.four = True
                    instanc.save()
                if extrawide == '6':
                    instanc.six = True
                    instanc.save()
                data = {
                    'message': 'Entered'

                }
                return JsonResponse(data, safe=False)

            if extrafirst == '2':
                instanc = MatchStatistics.objects.create(matchId=matchid,
                                                         innings=inning, bowlername=bowler,
                                                         noball = True, extra=True, extrarun=1,
                                                         batsmanname = extranobat)
                instanc.save()
                if extranorun == '0':
                    instanc.zero = True
                    instanc.save()
                if extranorun == '1':
                    instanc.one = True
                    instanc.save()
                if extranorun == '2':
                    instanc.two = True
                    instanc.save()
                if extranorun == '3':
                    instanc.three = True
                    instanc.save()
                if extranorun == '4':
                    instanc.four = True
                    instanc.save()
                if extranorun == '6':
                    instanc.six = True
                    instanc.save()
                data = {
                    'message': 'Entered'

                }
                return JsonResponse(data, safe=False)

        if selectedtype == '3':
            if wickettype == '1':
                instanc = MatchStatistics.objects.create(matchId=matchid,
                                                         innings=inning, bowlername=bowler,
                                                         wicket=True, catchby=wicketcatball,
                                                         batsmanname=wicketcatbat, legalball=True)
                instanc.save()
                data = {
                    'message': 'Entered'

                }
                return JsonResponse(data, safe=False)
            if wickettype == '2':
                instanc = MatchStatistics.objects.create(matchId=matchid,
                                                         innings=inning, bowlername=bowler,
                                                         wicket=True,batsmanname=wicketbat, legalball=True)
                instanc.save()
                data = {
                    'message': 'Entered'

                }
                return JsonResponse(data, safe=False)
            if wickettype == '3':
                instanc = MatchStatistics.objects.create(matchId=matchid,
                                                         innings=inning, bowlername=bowler,
                                                         wicket=True, runoutby=wicketrunoutball,
                                                         batsmanname=wicketrunoutbat, legalball=True)
                instanc.save()
                data = {
                    'message': 'Entered'

                }
                return JsonResponse(data, safe=False)

def tossupdate(request):
    matchid = request.GET.get('matchid', None)
    teamsel = request.GET.get('teamsel', None)
    toss = request.GET.get('tossupdate', None)

    userid1 = CustomUser.objects.get(email=teamsel)
    teamselinstance = CricketTeam.objects.get(user=userid1.id)

    matchinstance = MatchSchedule.objects.get(pk=matchid)
    teamlist = []
    for select in matchinstance.teams.all():
        teamlist.append(select.user)

    matchplayedinstance = MatchPlayedByTeam(matchId=matchinstance)
    matchplayedinstance.save()

    matchinstance.tossstatus = 'done'
    matchinstance.save()

    firstteaminstance = CricketTeam.objects.get(user=teamlist[0])
    secondteaminstance = CricketTeam.objects.get(user=teamlist[1])

    matchplayedinstance.firstteam = firstteaminstance
    matchplayedinstance.save()
    matchplayedinstance.secondteam = secondteaminstance
    matchplayedinstance.save()

    if teamselinstance == firstteaminstance:
        if toss == 'Batting':
            matchplayedinstance.battingteam = firstteaminstance
            matchplayedinstance.save()
        if toss == 'Fielding':
            matchplayedinstance.battingteam = secondteaminstance
            matchplayedinstance.save()

    if teamselinstance == secondteaminstance:
        if toss == 'Batting':
            matchplayedinstance.battingteam = secondteaminstance
            matchplayedinstance.save()
        if toss == 'Fielding':
            matchplayedinstance.battingteam = firstteaminstance
            matchplayedinstance.save()

    data = {

    }

    return JsonResponse(data, safe=False)

def finishinnings(request):
    if request.method == "POST":
        matchid = request.POST['matchid']
        matchinstance = MatchSchedule.objects.get(pk=matchid)
        matchinstance.status = "ResultAvailable"
        matchinstance.save()

        eventinstance = CricketTournament.objects.get(pk=matchinstance.event.id)

        firstinningextras = MatchStatistics.objects.filter(matchId=matchid).filter(innings=1).filter \
            (extra=True).filter(legalball=False)
        totalextrarun = len(firstinningextras)

        one = len(firstinningextras.filter(one=True))
        two = len(firstinningextras.filter(two=True))
        three = len(firstinningextras.filter(three=True))
        four = len(firstinningextras.filter(four=True))
        six = len(firstinningextras.filter(six=True))

        totalfirstextra = ((one * 1) + (two * 2) + (three * 3) + (four * 4) + (six * 6)) + totalextrarun

        firstplayerslist = []
        firstinning = MatchStatistics.objects.filter(matchId=matchid).filter(innings=1)

        for select in firstinning:
            newvariable = select.batsmanname
            if newvariable not in firstplayerslist:
                firstplayerslist.append(select.batsmanname)

        firstscorerunlist = []
        for select in firstplayerslist:
            firstobj = MatchStatistics.objects.filter(matchId=matchid).filter(innings=1).filter(
                batsmanname=select).filter(wicket=False).filter(wide=False).filter(extra=False). \
                filter(legbye=False).filter(legalball=True)

            one = len(firstobj.filter(one=True))
            two = len(firstobj.filter(two=True))
            three = len(firstobj.filter(three=True))
            four = len(firstobj.filter(four=True))
            six = len(firstobj.filter(six=True))

            firstscorerunlist.append([select,
                                      ((one * 1) + (two * 2) + (three * 3) + (four * 4) + (six * 6))])
        totaloffirstinning = 0
        for select in firstscorerunlist:
            totaloffirstinning = totaloffirstinning + select[1]
        totaloffirstinningfinal = totaloffirstinning + totalfirstextra


        secondinningextras = MatchStatistics.objects.filter(matchId=matchid).filter(innings=2).filter \
            (extra=True).filter(legalball=False)
        totalextrarunsecond = len(secondinningextras)

        one = len(secondinningextras.filter(one=True))
        two = len(secondinningextras.filter(two=True))
        three = len(secondinningextras.filter(three=True))
        four = len(secondinningextras.filter(four=True))
        six = len(secondinningextras.filter(six=True))

        totalsecondextra = ((one * 1) + (two * 2) + (three * 3) + (four * 4) + (six * 6)) + totalextrarunsecond

        secondplayerslist = []
        secondinning = MatchStatistics.objects.filter(matchId=matchid).filter(innings=2)

        for select in secondinning:
            newvariable = select.batsmanname
            if newvariable not in secondplayerslist:
                secondplayerslist.append(select.batsmanname)

        secondscorerunlist = []
        for select in secondplayerslist:
            firstobj = MatchStatistics.objects.filter(matchId=matchid).filter(innings=2).filter(
                batsmanname=select).filter(wicket=False).filter(wide=False).filter(extra=False). \
                filter(legbye=False).filter(legalball=True)

            one = len(firstobj.filter(one=True))
            two = len(firstobj.filter(two=True))
            three = len(firstobj.filter(three=True))
            four = len(firstobj.filter(four=True))
            six = len(firstobj.filter(six=True))

            secondscorerunlist.append([select,
                                       ((one * 1) + (two * 2) + (three * 3) + (four * 4) + (six * 6))])
        totalofsecondinning = 0
        for select in secondscorerunlist:
            totalofsecondinning = totalofsecondinning + select[1]
        totalofsecondinningfinal = totalofsecondinning + totalsecondextra

        if totaloffirstinningfinal > totalofsecondinningfinal:
            instancegetter = MatchPlayedByTeam.objects.get(matchId=matchinstance)
            winningteam = instancegetter.battingteam
            teaminstance = CricketTeam.objects.get(pk=winningteam)
            pointvalue = 0
            try:
                pointsinstance = PointsTable.objects.filter(teams=teaminstance).filter(tournament=eventinstance)
                for select in pointsinstance:
                    pointvalue = (pointvalue) + select.points
                    pointvalue = pointvalue + 2
                    pointsinstanceagin = PointsTable.objects.get(pk=select.id)
                    pointsinstanceagin.points = pointvalue
                    pointsinstanceagin.save()
            except:
                pointvalue = 2
                pointstableinstance = PointsTable.objects.create(tournament=eventinstance, points=pointvalue,
                                                                 teams=teaminstance)
                pointstableinstance.save()
        else:
            instancegetter = MatchPlayedByTeam.objects.get(matchId=matchinstance)
            winningteam = instancegetter.battingteam
            if instancegetter.firstteam == winningteam:
                teamcheckervariable = instancegetter.secondteam
            else:
                teamcheckervariable = instancegetter.firstteam
            teaminstance = CricketTeam.objects.get(pk=teamcheckervariable)
            pointvalue = 0
            try:
                pointsinstance = PointsTable.objects.filter(teams=teaminstance).filter(tournament=eventinstance)
                for select in pointsinstance:
                    pointvalue = pointvalue + select.points
                pointvalue = pointvalue + 2
            except:
                pointvalue = 2

            pointstableinstance = PointsTable.objects.create(tournament=eventinstance, points=pointvalue,
                                                             teams=teaminstance)
            pointstableinstance.save()

        return redirect('cricket:eventdisplay')

def noticedisplay(request):
    notices = Notice.objects.all()
    context = {
        'notice':notices
    }
    return render(request, 'cricket/noticedisplay.html', context)

def searchevent(request):
    if request.method == "POST":
        name = request.POST['eventname']
        cricketevent = CricketTournament.objects.filter(name=name)
        if cricketevent.exists():
            context = {
                'cricketevent': cricketevent
            }
        else:
            context = {
                'message':"Sorry No Event Found"
            }
        return render(request, 'cricket/searchresults.html', context)
    return render(request, 'cricket/searchresults.html')
