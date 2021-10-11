from django.shortcuts import render, redirect
from members.forms import *
from django.views.generic import CreateView
from cricket.models import *
from members.models import *
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.http import JsonResponse
from django.contrib.auth import logout
import time
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages


class signupofcricketteam(CreateView):
    model = CustomUser
    form_class = cricketteamsignupform
    template_name = 'members/teamregistration.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'cricket'
        return super(signupofcricketteam, self).get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        cricketteaminstance = CricketTeam.objects.create(user=user)
        cricketteaminstance.teamname = form.cleaned_data.get('teamname')
        if form.cleaned_data.get('teamlogo') != "":
            cricketteaminstance.logo = form.cleaned_data.get('teamlogo')
        cricketteaminstance.captain_name = form.cleaned_data.get('captainname')
        cricketteaminstance.contactno = form.cleaned_data.get('mobileno')
        cricketteaminstance.save()
        return redirect('members:home')


def home(request):
    tournament = CricketTournament.objects.last()
    pointsinstance = PointsTable.objects.filter(tournament=tournament)

    context = {
        'pointstabledata': pointsinstance
    }
    return render(request, 'members/dashboard.html', context)


@user_passes_test(lambda u: u.is_staff, login_url='members:login', redirect_field_name=None)
def createvent(request):
    scorer_users = CustomUser.objects.filter(is_scorer=True)
    context = {
        'scorerlist': scorer_users
    }
    return render(request, 'members/createevent.html', context)


def teamprofile(request):
    user = request.user
    teamid = CricketTeam.objects.get(user=user)
    context = {
        'team': teamid
    }
    return render(request, 'members/profile2.html', context)


def registerforevent(request):
    currentevent = CricketTournament.objects.last()
    date = time.strftime("%Y-%m-%d")
    if date > str(currentevent.deadlineforregistration):
        content = "Sorry Registration Is Closed For This Event"
        context = {
            'alert': content
        }
        return render(request, 'members/alertpage.html', context)
    else:
        user = request.user
        crickettournamentinstance = CricketTeam.objects.get(user=user)
        context = {
            'currentevent': currentevent,
            'team': crickettournamentinstance
        }
        return render(request, 'members/registerforevent.html', context)


def evententry(request):
    if request.method == 'POST':
        eventnamevalue = request.POST['eventname']
        venenuname1 = request.POST['venue1']
        venenuname2 = request.POST['venue2']
        venenuname3 = request.POST['venue3']
        date = request.POST['date']
        rulesarea = request.POST['rulesarea']
        cricketovers = request.POST['cricketovers']
        scorer = request.POST['eventscorer']
        scorerinstance = CustomUser.objects.get(pk=scorer)

        try:
            logoimage = request.FILES['eventlogo']
        except MultiValueDictKeyError:
            logoimage = False

        if venenuname2 == "":
            venenuname2 = ""
        if venenuname3 == "":
            venenuname3 = ""
        if date == "":
            date = "2018-04-12"
        if rulesarea == "":
            rulesarea = ""
        entringquery = CricketTournament(name=eventnamevalue, logo=logoimage, venue1=venenuname1,
                                         venue2=venenuname2, venue3=venenuname3, deadlineforregistration=date,
                                         criteria=rulesarea, overs=cricketovers, scorer=scorerinstance)
        entringquery.save()
    return redirect('members:home')


def loginuser(request):
    if request.POST:
        username = request.POST['email']
        print(username)
        password = request.POST['password']
        print(password)
        user = authenticate(username=username, password=password)
        if user is not None:
            print("user is auth")
            if user.is_active:
                # if user.is_cricket:
                login(request, user)
                return redirect('members:home')
        else:
            print("user is not auth")
            messages.error(request, "Error")
            # message = "Sorry username and password combination is not valid"
    return render(request, 'members/login.html')


def logoutuser(request):
    logout(request)
    return redirect('members:home')


def registered(request):
    user = request.user
    teamname = request.POST['teamname']
    eventname = request.POST['evename']
    email = request.POST['email']
    contact = request.POST['contact']
    teamid = CricketTeam.objects.get(user=user)
    eventinstance = CricketTournament.objects.get(name=eventname)
    allvalues = RegisteredTeam.objects.filter(
        cricketevent=eventinstance).filter(teamid=teamid)

    if allvalues.exists():
        content = "You Have Already Registered To This Event"
        context = {
            'alert': content
        }
        return render(request, 'members/alertpage.html', context)
    else:
        if teamname == "":
            teamname = ""
        if contact == "":
            contact = ""

        entringinstance = RegisteredTeam(cricketevent=eventinstance, teamname=teamname, teamid=teamid,
                                         contactno=contact)
        entringinstance.save()
        return redirect('members:home')


def ajaxvalidation(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': CustomUser.objects.filter(email__iexact=username).exists()
    }
    return JsonResponse(data)


def updateprofile(request):
    user = request.user
    if request.method == 'POST':
        player1name = request.POST['player1']
        player1category = request.POST['category1']
        player2name = request.POST['player2']
        player2category = request.POST['category2']
        player3name = request.POST['player3']
        player3category = request.POST['category3']
        player4name = request.POST['player4']
        player4category = request.POST['category4']
        player5name = request.POST['player5']
        player5category = request.POST['category5']
        player6name = request.POST['player6']
        player6category = request.POST['category6']
        player7name = request.POST['player7']
        player7category = request.POST['category7']
        player8name = request.POST['player8']
        player8category = request.POST['category8']
        player9name = request.POST['player9']
        player9category = request.POST['category9']
        player10name = request.POST['player10']
        player10category = request.POST['category10']
        player11name = request.POST['player11']
        player11category = request.POST['category11']
        player12name = request.POST['player12']
        player12category = request.POST['category12']
        teamid = CricketTeam.objects.get(user=user)
        if player1name != "":
            if player1category != "":
                participant1 = Participant(
                    name=player1name, speciality=player1category)
                participant1.save()
                teamid.participant.add(participant1)
                teamid.save()
            else:
                participant1 = Participant(
                    name=player1name, speciality=player1category)
                participant1.save()
                teamid.participant.add(participant1)
                teamid.save()

        if player2name != "":
            if player2category != "":
                participant2 = Participant(
                    name=player2name, speciality=player2category)
                participant2.save()
                teamid.participant.add(participant2)
                teamid.save()
            else:
                participant1 = Participant(
                    name=player1name, speciality=player1category)
                participant1.save()
                teamid.participant.add(participant1)
                teamid.save()

        if player3name != "":
            if player3category != "":
                participant3 = Participant(
                    name=player3name, speciality=player3category)
                participant3.save()
                teamid.participant.add(participant3)
                teamid.save()
            else:
                participant1 = Participant(
                    name=player1name, speciality=player1category)
                participant1.save()
                teamid.participant.add(participant1)
                teamid.save()

        if player4name != "":
            if player4category != "":
                participant4 = Participant(
                    name=player4name, speciality=player4category)
                participant4.save()
                teamid.participant.add(participant4)
                teamid.save()
            else:
                participant1 = Participant(
                    name=player1name, speciality=player1category)
                participant1.save()
                teamid.participant.add(participant1)
                teamid.save()

        if player5name != "":
            if player5category != "":
                participant5 = Participant(
                    name=player5name, speciality=player5category)
                participant5.save()
                teamid.participant.add(participant5)
                teamid.save()
            else:
                participant1 = Participant(
                    name=player1name, speciality=player1category)
                participant1.save()
                teamid.participant.add(participant1)
                teamid.save()

        if player6name != "":
            if player6category != "":
                participant6 = Participant(
                    name=player6name, speciality=player6category)
                participant6.save()
                teamid.participant.add(participant6)
                teamid.save()
            else:
                participant1 = Participant(
                    name=player1name, speciality=player1category)
                participant1.save()
                teamid.participant.add(participant1)
                teamid.save()

        if player7name != "":
            if player7category != "":
                participant7 = Participant(
                    name=player7name, speciality=player7category)
                participant7.save()
                teamid.participant.add(participant7)
                teamid.save()
            else:
                participant1 = Participant(
                    name=player1name, speciality=player1category)
                participant1.save()
                teamid.participant.add(participant1)
                teamid.save()

        if player8name != "":
            if player8category != "":
                participant8 = Participant(
                    name=player8name, speciality=player8category)
                participant8.save()
                teamid.participant.add(participant8)
                teamid.save()
            else:
                participant1 = Participant(
                    name=player1name, speciality=player1category)
                participant1.save()
                teamid.participant.add(participant1)
                teamid.save()

        if player9name != "":
            if player9category != "":
                participant9 = Participant(
                    name=player9name, speciality=player9category)
                participant9.save()
                teamid.participant.add(participant9)
                teamid.save()
            else:
                participant1 = Participant(
                    name=player1name, speciality=player1category)
                participant1.save()
                teamid.participant.add(participant1)
                teamid.save()

        if player10name != "":
            if player10category != "":
                participant10 = Participant(
                    name=player10name, speciality=player10category)
                participant10.save()
                teamid.participant.add(participant10)
                teamid.save()
            else:
                participant1 = Participant(
                    name=player1name, speciality=player1category)
                participant1.save()
                teamid.participant.add(participant1)
                teamid.save()

        if player11name != "":
            if player11category != "":
                participant10 = Participant(
                    name=player10name, speciality=player12category)
                participant10.save()
                teamid.participant.add(participant10)
                teamid.save()
            else:
                participant11 = Participant(name=player11name)
                participant11.save()
                teamid.participant.add(participant11)
                teamid.save()

        if player12name != "":
            if player12category != "":
                participant12 = Participant(
                    name=player12name, speciality=player12category)
                participant12.save()
                teamid.participant.add(participant12)
                teamid.save()
            else:
                participant12 = Participant(name=player12name)
                participant12.save()
                teamid.participant.add(participant12)
                teamid.save()

    return redirect('members:teamprofile')


def scorersignup(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = CustomUser.objects.create(
                email=email, first_name=name, is_scorer=True)
            user.save()
            user.set_password(password)
            user.save()
            return redirect('members:home')
        except:
            context = {
                'alertmessage': "Sorry Email Address Already Exists"
            }
            return render(request, 'members/scorer_registration.html', context)
    else:
        return render(request, 'members/scorer_registration.html')


def askquery(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        query = request.POST['query']
        contactus = ContactUS.objects.create(
            name=name, email=email, subject=subject, query=query)
        contactus.save()
        return redirect('members:home')

    else:
        return render(request, 'members/contact.html')


def notice(request):
    if request.method == "POST":
        title = request.POST["title"]
        notice = request.POST["notice"]
        noticeinstance = Notice.objects.create(title=title, notice=notice)
        noticeinstance.save()
        return redirect("members:home")
    else:
        return render(request, 'members/notice.html')


def notifications(request, userid):
    uservalue = userid
    userinstance = CricketTeam.objects.get(user=uservalue)
    notifications = Notification.objects.filter(team=userinstance)
    context = {
        'notifications': notifications
    }
    return render(request, 'members/notifications.html', context)


def queries(request):
    queries = ContactUS.objects.all()
    context = {
        'queries': queries
    }
    return render(request, 'members/queries_display.html', context)

def training(request):
    return render(request, 'members/training.html')