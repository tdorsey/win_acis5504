# Create your models here.
from django.db import models
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist



class Person(models.Model):
    person_id = models.AutoField('Person ID', primary_key=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    dob = models.DateField('Date of Birth')
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    region = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=5) 
    country = models.CharField(max_length=2)
    banned_until = models.DateField('Banned Until', blank=True, null=True)
    active_since = models.DateField('Join Date')
    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)
    class Meta:
        abstract = True 

class Pro_Level(models.Model):
	level = models.AutoField('Pro Level', primary_key=True)
	description = models.CharField(max_length=500)
	class Meta:
		verbose_name_plural = "Pro Levels"
class Pro_Level_Admin(admin.ModelAdmin):
	list_display = ('level', 'description')

class Player(Person):
    rank = models.PositiveIntegerField(blank=True, null=True)
    points = models.PositiveIntegerField(default=0)
    lifetime_points = models.PositiveIntegerField(default=0)
    pro_level = models.ForeignKey(Pro_Level, blank=True, null=True)
    def __unicode__(self):
        return u'%s %s - %s' % (self.first_name, self.last_name, self.person_id)

class PlayerAdmin(admin.ModelAdmin):
    list_display = ('person_id', 'last_name', 'first_name')

#Judges explicitly are not people, because then it is not possible to make an existing player a judge without reintering basic info	
class Judge(models.Model):
	def Judge(self):
		p = self.player	
		return "{0}, {1} - {2}".format(p.last_name, p.first_name, p.person_id)  
	def __unicode__(self):
		return self.Judge()
	player = models.OneToOneField(Player)
	level = models.PositiveIntegerField()
	certified_until = models.DateField('Certified Until')

class JudgeAdmin(admin.ModelAdmin):
    list_display = ('Judge', 'level')


class Event_Level(models.Model):
    level = models.IntegerField('Rules Enforcement Level', primary_key=True)
    description = models.CharField(max_length=200)
    points_multiplier = models.PositiveIntegerField()
    required_judge_level = models.PositiveIntegerField()
    def __unicode__(self):
        return u'%s %s' % (self.pk, self.description)
    class Meta:
        verbose_name_plural = "Event Levels"

class Event_Level_Admin(admin.ModelAdmin):
    list_display = ('level', 'description')

class Round(models.Model):
	number = models.IntegerField()
#Use the name of the model class to resolve a circular dependency
#See http://stackoverflow.com/questions/7298326/django-models-mutual-references-between-two-classes-and-impossibility-to-use-fo
	event = models.ForeignKey('Event')
	matches = models.ManyToManyField('Match', related_name="matches_in_round")
	standing = models.ForeignKey('Standing', blank="True", null="True")
	class Meta:
		unique_together = ('event', 'number')
	def __unicode__(self):
		return u'%s' % (self.number)
class Event(models.Model):
	event_id = models.AutoField('Event ID', primary_key=True)
	description = models.CharField(max_length=500)
	date = models.DateField()
	location = models.CharField(max_length=200)
	level = models.ForeignKey(Event_Level)
	num_rounds = models.IntegerField()
	format = models.CharField(max_length=50)
	head_judge = models.ForeignKey(Judge, related_name='head_judge')
	judges = models.ManyToManyField(Judge, related_name='floor_judge', blank=True, null=True)
	def __unicode__(self):
		return u'%s %s' % (self.date, self.description)
#Doing all this work after super.save is equivalent to a post_save event
# See http://www.martin-geber.com/thought/2007/10/29/django-signals-vs-custom-save-method/
	def save(self, *args, **kwargs):
		super(Event, self).save()	
		i = 1
		while i <=  self.num_rounds:
			Round.objects.get_or_create(event=self, number = i)
			i +=1 
class EventAdmin(admin.ModelAdmin):
    list_display = ('event_id', 'date','description')

class Registration(models.Model):
    event = models.ForeignKey(Event)
    player = models.ForeignKey(Player)
    dropped = models.NullBooleanField(blank=True, null=True)
    dropped_round = models.IntegerField(blank=True, null=True)
    def player_is_judging_event(self):
        player_is_head_judge = False
        player_is_floor_judge = False
        eventQS = Event.objects.filter(event_id=self.event.event_id).prefetch_related('head_judge', 'judges')
        event = eventQS.get(event_id=self.event.event_id)
        if (event.head_judge.player_id == self.player.person_id):
            player_is_head_judge = True
        
        #check floor judges
        player_is_floor_judge = event.judges.filter(player_id=self.player.person_id).exists()
        
        return player_is_head_judge or player_is_floor_judge
    
    def __unicode__(self):
        return u'%s %s' % (self.event, self.player)
    def clean(self):
            #Don't allow judges to register for events they run
        if self.player_is_judging_event():
            raise ValidationError(self.player.first_name + " "  + self.player.last_name + " is judging event " + self.event.description)

class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('event', 'player')
class Match(models.Model):
    DRAW = 'Draw'
    PLAYER1 = 'Player 1'
    PLAYER2  = 'Player 2'
    MATCH_RESULT_CHOICES = (
        (0, DRAW),
        (1, PLAYER1),
        (2, PLAYER2),
    )
    result = models.IntegerField(max_length=1,
    choices=MATCH_RESULT_CHOICES)
    match_id = models.AutoField('Match ID', primary_key=True)
    event = models.ForeignKey(Event)	
    round = models.ForeignKey(Round)	
    player1 = models.ForeignKey(Player, related_name='player_1')
    player2 = models.ForeignKey(Player, related_name='player_2')
    player1_wins = models.IntegerField()
    player2_wins = models.IntegerField()
    games = models.IntegerField()	
    def clean(self):
    # Don't allow matches between players not in the event.
        current_registrations = Registration.objects.filter(event=self.event).prefetch_related('player')
        try:
            p = self.player1
            current_registrations.get(player=p)
            p = self.player2
            current_registrations.get(player=p)
        except ObjectDoesNotExist:
            raise ValidationError( p.__unicode__() + ' is not registered for event ' + self.event.__unicode__())
    class Meta:
        verbose_name_plural = "Matches"	
    def save(self, *args, **kwargs):
        if self.player1_wins + self.player2_wins != self.games:
            raise Exception("Combined wins for both players must equal the number of games")
        super(Match, self).save(*args, **kwargs)  

class MatchAdmin(admin.ModelAdmin):
	list_display = ('match_id', 'round', 'player1', 'player2')

class Standing(models.Model):
	player = models.ForeignKey(Player)
	ranking = models.IntegerField()
	points = models.IntegerField()
	opponent_match_win = models.IntegerField()
	game_win = models.IntegerField()
	opponent_game_win = models.IntegerField()

class StandingAdmin(admin.ModelAdmin):
    list_display = ('player', 'ranking')

