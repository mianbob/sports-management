from django.contrib.auth.models import AbstractUser, BaseUserManager
from members.models import *
from datetime import date


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email,  password, **extra_fields):
        """Create and save a User with the given email and password."""
        # if not email:
        #     raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user =   self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)
        user.is_cricket = True
        user.save(using=self._db)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return user

    def create_user(self, email, username,  password=None):
        """Create and save a regular User with the given email and password."""
        variable = ""
        # extra_fields.setdefault('is_staff', False)
        # extra_fields.setdefault('is_superuser', False)
        # extra_fields.setdefault('is_patient', True)

        return self._create_user(email, password)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    is_cricket_team = models.BooleanField(default=False)
    is_footbal_team = models.BooleanField(default=False)
    is_scorer = models.BooleanField(default=False)
    username = None
    email = models.EmailField(('email address'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


class Venue(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'Venue'

    def __str__(self):
        return self.name


class CricketTournament(models.Model):
    name = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='eventlogo')
    venue1 = models.CharField(max_length=50)
    venue2 = models.CharField(max_length=50)
    venue3 = models.CharField(max_length=50)
    deadlineforregistration = models.DateField(("Date"), default=date.today)
    criteria = models.CharField(max_length=200)
    overs = models.IntegerField()
    scorer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'CricketTournmanet'

    def __str__(self):
        return '%s%s%s%s%s' % (self.name, self.logo, self.venue1, self.venue2, self.venue3)
#


class RegisteredTeam(models.Model):
    cricketevent = models.ForeignKey(
        CricketTournament, on_delete=models.CASCADE)
    teamname = models.CharField(max_length=32)
    teamid = models.ForeignKey(CricketTeam, on_delete=models.CASCADE)
    contactno = models.IntegerField(default=0)
    status = models.CharField(max_length=32, default='pending')

    class Meta:
        verbose_name_plural = 'RegisteredTeam'

    def __str__(self):
        return '%s%s%s%s' % (self.cricketevent, self.teamname, self.teamid, self.contactno)


class MatchSchedule(models.Model):
    event = models.ForeignKey(CricketTournament, on_delete=models.CASCADE)
    matchNo = models.IntegerField()
    teams = models.ManyToManyField(CricketTeam)
    date = models.DateTimeField()
    venue = models.CharField(max_length=32)
    status = models.CharField(max_length=32, default='pending')
    tossstatus = models.CharField(max_length=32, default='pending')

    class Meta:
        verbose_name_plural = 'MatchSchedule'

    def __str__(self):
        return '%s%s' % (self.matchNo, self.date)


class MatchPlayedByTeam(models.Model):
    matchId = models.ForeignKey(MatchSchedule, on_delete=models.CASCADE)
    Tosswin = models.ForeignKey(
        CricketTeam, null=True, related_name='tosswin', on_delete=models.CASCADE)
    firstteam = models.ForeignKey(
        CricketTeam, null=True, related_name='firstteam', on_delete=models.CASCADE)
    secondteam = models.ForeignKey(
        CricketTeam, null=True, related_name='secondteam', on_delete=models.CASCADE)
    battingteam = models.ForeignKey(
        CricketTeam, null=True, related_name='battingteam', on_delete=models.CASCADE)


class PointsTable(models.Model):
    tournament = models.ForeignKey(CricketTournament, on_delete=models.CASCADE)
    teams = models.ForeignKey(CricketTeam, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)


class MatchStatistics(models.Model):
    six = models.BooleanField(default=False)
    four = models.BooleanField(default=False)
    zero = models.BooleanField(default=False)
    one = models.BooleanField(default=False)
    two = models.BooleanField(default=False)
    three = models.BooleanField(default=False)
    runout = models.BooleanField(default=False)
    wicket = models.BooleanField(default=False)
    extra = models.BooleanField(default=False)
    noball = models.BooleanField(default=False)
    wide = models.BooleanField(default=False)
    legalball = models.BooleanField(default=False)
    matchId = models.ForeignKey(MatchSchedule, on_delete=models.CASCADE)
    bowlername = models.CharField(max_length=32)
    batsmanname = models.CharField(max_length=32)
    catchby = models.CharField(max_length=32)
    runoutby = models.CharField(max_length=32)
    innings = models.IntegerField()
    legbye = models.BooleanField(default=False)
    extrarun = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'MatchStatistics'

    def __str__(self):
        return '%s%s%s%s%s%s%s%s%s%s%s%s%s' % (self.six, self.four, self.one, self.two, self.three, self.runout,
                                               self.wicket, self.extra, self.noball, self.wide, self.bowlername,
                                               self.batsmanname, self.catchby)


class ContactUS(models.Model):
    name = models.CharField(max_length=32)
    subject = models.CharField(max_length=32)
    email = models.CharField(max_length=32)
    query = models.TextField()


class Notice(models.Model):
    title = models.CharField(max_length=32)
    notice = models.TextField()


class Notification(models.Model):
    title = models.CharField(max_length=32)
    notification = models.TextField()
    team = models.ForeignKey(CricketTeam, on_delete=models.CASCADE)
