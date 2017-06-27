from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from world.models import Tribe
from django.utils.translation import ugettext_lazy as _
from nocaptcha_recaptcha.fields import NoReCaptchaField
from models import *
from troops import models as tm
from datetime import datetime, timedelta

class SignUpForm(UserCreationForm):
	ne = 'ne'
	nw = 'nw'
	se = 'se'
	sw = 'sw'
	location_choices = (
		(ne, _('North East')),
		(nw , _('North West')),
		(se , _('South East')),
		(sw , _('South West')),
	)
	partisan = 'Partisans'
	russian = 'Russians'
	american = 'Americans' 
	brits = 'Brittish' 
	german = 'Germans' 
	japs = 'Japanese'
	options = (
		(partisan , _('Partisans')), # Def + raiding + bouns if attacked (between gauls and teuts)
		(russian , _('Russians')), # Cheap attack + raiding (teutons like)
		(american , _('Americans')), # Hard to start, easy to end (romans like)
		(brits , _('Brittish')), # Strong def, medium wall and strong navy (between gauls and romans)
		(german , _('Germans')), # Strong attack, weak def + medium speed. Weak wall (somewhere between teuts and romans)
		(japs , _('Japanese')) # Strong in tight battles. Kamikaze (Not defined yet)
	)
	email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
	select_tribe = forms.ChoiceField(choices = options)
	start_location = forms.ChoiceField(choices = location_choices)
	captcha = NoReCaptchaField()
	class Meta:
		model = User
		fields = ('username', 'email', 'password1', 'password2', 'select_tribe', 'start_location', )

class MessageForm(forms.Form):
	recipent = forms.CharField(max_length=55, help_text=_('To:'))
	subject = forms.CharField(max_length = 50, help_text=_('Subject'), required = False)
	message = forms.CharField(max_length = 10*10, help_text = _('Message'), widget=forms.Textarea)
	class Meta:
		fields = ('recipent', 'subject', 'message')

class AllyForm(forms.Form):
	name = forms.CharField(max_length= 25, help_text=_('Alliance name'))
	short_name = forms.CharField(max_length= 5, help_text=_('Alliance shortname'))
	class Meta:
		fields = ('name', 'short_name')
		
class InviteForm(forms.Form):
	player = forms.CharField(max_length= 25, help_text=_('Invite player:'))
	class Meta:
		fields = ('player')

class LeaderForm(forms.Form):
	leader = forms.CharField(max_length= 25, help_text=_("Player's name"), required = False)
	position = forms.CharField(max_length= 25, help_text=_("Position"), required = False)
	mm_rights = forms.BooleanField(help_text=_("Mass message rights"), required = False)
	diplomacy_rights = forms.BooleanField(help_text=_("Diplomacy rights"), required = False)
	invite = forms.BooleanField(help_text=_("Can invite new member"), required = False)
	set_leader = forms.BooleanField(help_text=_("Can change leaders"), required = False)
	profile = forms.BooleanField(help_text=_("Can change profile"), required = False)
	kick = forms.BooleanField(help_text=_("Can kick member from alliance"), required = False)
	class Meta:
		fields = ('leader','position','mm_rights','diplomacy_rights', 'invite','set_leader', 'profile', 'kick')
		
class ProfileForm(forms.Form):
	profile = forms.CharField(max_length= 2505, help_text=_('Profile:'),  widget=forms.Textarea, required = False)
	class Meta:
		fields = ('profile')
		
class LeaderEditForm(forms.Form):
	position = forms.CharField(max_length= 25, help_text=_("Position"), required = False)
	mm_rights = forms.BooleanField(help_text=_("Mass message rights"), required = False)
	diplomacy_rights = forms.BooleanField(help_text=_("Diplomacy rights"), required = False)
	invite = forms.BooleanField(help_text=_("Can invite new member"), required = False)
	set_leader = forms.BooleanField(help_text=_("Can change leaders"), required = False)
	profile = forms.BooleanField(help_text=_("Can change profile"), required = False)
	kick = forms.BooleanField(help_text=_("Can kick member from alliance"), required = False)
	class Meta:
		fields = ('position','mm_rights','diplomacy_rights', 'invite','set_leader', 'profile', 'kick')
		
class ConfirmationForm(forms.Form):
	password = forms.CharField(help_text = _('Confirm your identity with password'), max_length = 50, widget=forms.PasswordInput())
	class Meta:
		fields = ('password')

def time(nex, lvl):
	seconds = int(nex.second) + int(nex.minute)*60 + int(nex.hour)*3600
	seconds = int(seconds * 0.9**lvl)
	return str(str(int(seconds/3600)%24)+':'+ str(int((seconds%3600)/60)).zfill(2)+':'+str(int((seconds%60))).zfill(2))

class CampForm(forms.Form):
	def __init__(self,*args,**kwargs):
		self.player_id = kwargs.pop('player_id')
		self.lvl = kwargs.pop('lvl')
		super(CampForm,self).__init__(*args,**kwargs)
		player = Player.objects.get(id = int(self.player_id))
		if player.tribe.name == 'Partisans':
			army = Partisan_troops.objects.get(id = 1)
		elif player.tribe.name == 'Russians':
			army = Russian_troops.objects.get(id = 1)
		elif player.tribe.name == 'Americans':
			army = American_troops.objects.get(id = 1)
		elif player.tribe.name == 'Brittish':
			army = Brittish_troops.objects.get(id = 1)
		elif player.tribe.name == 'Germans':
			army = German_troops.objects.get(id = 1)
		elif player.tribe.name == 'Japanese':
			army = Japanese_troops.objects.get(id = 1)
		self.fields['t0'].label = army.t0.troop.name 
		self.fields['t1'].label = army.t1.troop.name
		self.fields['t0'].help_text ='<br> <img src="' + army.t0.troop.image.url+'" class="margin-bottom" style="max-width: 60px" alt=""> <br>' + ' Oil: ' + str(army.t0.troop.training_cost.oil) + ' Iron: ' + str(army.t0.troop.training_cost.iron) + ' Wood: ' + str(army.t0.troop.training_cost.wood) + ' Food: ' + str(army.t0.troop.training_cost.food) + ' Costs: ' + str(army.t0.troop.consumption) + '<br> Training time: '+time(army.t0.troop.training_time, self.lvl)
		self.fields['t1'].help_text = '<br> <img src="' + army.t1.troop.image.url+'" class="margin-bottom" style="max-width: 60px" alt=""> <br>' + ' Oil: ' + str(army.t1.troop.training_cost.oil) + ' Iron: ' + str(army.t1.troop.training_cost.iron) + ' Wood: ' + str(army.t1.troop.training_cost.wood) + ' Food: ' + str(army.t1.troop.training_cost.food) + ' Costs: ' + str(army.t1.troop.consumption) + '<br> Training time: '+time(army.t1.troop.training_time, self.lvl)
		if player.last_village.army.t1.count == -1:
			self.fields['t1'].widget = form.HiddenInput()
	t0 = forms.IntegerField(required = False, min_value=1)
	t1 = forms.IntegerField(required = False, min_value=1)
	class Meta:
		fields = ('t0', 't1')
	
class HangarForm(forms.Form):
	def __init__(self,*args,**kwargs):
		self.player_id = kwargs.pop('player_id')
		self.lvl = kwargs.pop('lvl')
		super(HangarForm,self).__init__(*args,**kwargs)
		player = Player.objects.get(id = int(self.player_id))
		if player.tribe.name == 'Partisans':
			army = Partisan_troops.objects.get(id = 1)
		elif player.tribe.name == 'Russians':
			army = Russian_troops.objects.get(id = 1)
		elif player.tribe.name == 'Americans':
			army = American_troops.objects.get(id = 1)
		elif player.tribe.name == 'Brittish':
			army = Brittish_troops.objects.get(id = 1)
		elif player.tribe.name == 'Germans':
			army = German_troops.objects.get(id = 1)
		elif player.tribe.name == 'Japanese':
			army = Japanese_troops.objects.get(id = 1)
		self.fields['t2'].label = army.t2.troop.name 
		self.fields['t3'].label = army.t3.troop.name
		self.fields['t4'].label = army.t4.troop.name
		self.fields['t2'].help_text ='<br> <img src="' + army.t2.troop.image.url+'" class="margin-bottom" style="max-width: 60px" alt=""> <br>' + ' Oil: ' + str(army.t2.troop.training_cost.oil) + ' Iron: ' + str(army.t2.troop.training_cost.iron) + ' Wood: ' + str(army.t2.troop.training_cost.wood) + ' Food: ' + str(army.t2.troop.training_cost.food) + ' Costs: ' + str(army.t2.troop.consumption) + '<br> Training time: '+time(army.t2.troop.training_time, self.lvl)
		self.fields['t3'].help_text = '<br> <img src="' + army.t3.troop.image.url+'" class="margin-bottom" style="max-width: 60px" alt=""> <br>' + ' Oil: ' + str(army.t3.troop.training_cost.oil) + ' Iron: ' + str(army.t3.troop.training_cost.iron) + ' Wood: ' + str(army.t3.troop.training_cost.wood) + ' Food: ' + str(army.t3.troop.training_cost.food) + ' Costs: ' + str(army.t3.troop.consumption) + '<br> Training time: '+time(army.t3.troop.training_time, self.lvl)
		self.fields['t4'].help_text ='<br> <img src="' + army.t4.troop.image.url+'" class="margin-bottom" style="max-width: 60px" alt=""> <br>' + ' Oil: ' + str(army.t4.troop.training_cost.oil) + ' Iron: ' + str(army.t4.troop.training_cost.iron) + ' Wood: ' + str(army.t4.troop.training_cost.wood) + ' Food: ' + str(army.t4.troop.training_cost.food) + ' Costs: ' + str(army.t4.troop.consumption) + '<br> Training time: '+time(army.t4.troop.training_time, self.lvl)
		if player.last_village.army.t2.count == -1:
			self.fields['t2'].widget = form.HiddenInput()
		if player.last_village.army.t3.count == -1:
			self.fields['t3'].widget = form.HiddenInput()
		if player.last_village.army.t4.count == -1:
			self.fields['t4'].widget = form.HiddenInput()
	t2 = forms.IntegerField(required = False, min_value=1)
	t3 = forms.IntegerField(required = False, min_value=1)
	t4 = forms.IntegerField(required = False, min_value=1)
	class Meta:
		fields = ('t2', 't3', 't4')	

class PortForm(forms.Form):
	def __init__(self,*args,**kwargs):
		self.player_id = kwargs.pop('player_id')
		self.lvl = kwargs.pop('lvl')
		super(PortForm,self).__init__(*args,**kwargs)
		player = Player.objects.get(id = int(self.player_id))
		if player.tribe.name == 'Partisans':
			army = Partisan_troops.objects.get(id = 1)
		elif player.tribe.name == 'Russians':
			army = Russian_troops.objects.get(id = 1)
		elif player.tribe.name == 'Americans':
			army = American_troops.objects.get(id = 1)
		elif player.tribe.name == 'Brittish':
			army = Brittish_troops.objects.get(id = 1)
		elif player.tribe.name == 'Germans':
			army = German_troops.objects.get(id = 1)
		elif player.tribe.name == 'Japanese':
			army = Japanese_troops.objects.get(id = 1)
		self.fields['t5'].label = army.t5.troop.name 
		self.fields['t6'].label = army.t6.troop.name
		self.fields['t7'].label = army.t7.troop.name
		self.fields['t5'].help_text ='<br> <img src="' + army.t5.troop.image.url+'" class="margin-bottom" style="max-width: 60px" alt=""> <br>' + ' Oil: ' + str(army.t5.troop.training_cost.oil) + ' Iron: ' + str(army.t5.troop.training_cost.iron) + ' Wood: ' + str(army.t5.troop.training_cost.wood) + ' Food: ' + str(army.t5.troop.training_cost.food) + ' Costs: ' + str(army.t5.troop.consumption) + '<br> Training time: '+time(army.t5.troop.training_time, self.lvl)
		self.fields['t6'].help_text = '<br> <img src="' + army.t6.troop.image.url+'" class="margin-bottom" style="max-width: 60px" alt=""> <br>' + ' Oil: ' + str(army.t6.troop.training_cost.oil) + ' Iron: ' + str(army.t6.troop.training_cost.iron) + ' Wood: ' + str(army.t6.troop.training_cost.wood) + ' Food: ' + str(army.t6.troop.training_cost.food) + ' Costs: ' + str(army.t6.troop.consumption) + '<br> Training time: '+time(army.t6.troop.training_time, self.lvl)
		self.fields['t7'].help_text ='<br> <img src="' + army.t7.troop.image.url+'" class="margin-bottom" style="max-width: 60px" alt=""> <br>' + ' Oil: ' + str(army.t7.troop.training_cost.oil) + ' Iron: ' + str(army.t7.troop.training_cost.iron) + ' Wood: ' + str(army.t7.troop.training_cost.wood) + ' Food: ' + str(army.t7.troop.training_cost.food) + ' Costs: ' + str(army.t7.troop.consumption) + '<br> Training time: '+time(army.t7.troop.training_time, self.lvl)
		if player.last_village.army.t5.count == -1:
			self.fields['t5'].widget = form.HiddenInput()
		if player.last_village.army.t6.count == -1:
			self.fields['t6'].widget = form.HiddenInput()
		if player.last_village.army.t7.count == -1:
			self.fields['t7'].widget = form.HiddenInput()
	t5 = forms.IntegerField(required = False, min_value=1)
	t6 = forms.IntegerField(required = False, min_value=1)
	t7 = forms.IntegerField(required = False, min_value=1)
	class Meta:
		fields = ('t5', 't6', 't7')	

class ArtileryForm(forms.Form):
	def __init__(self,*args,**kwargs):
		self.player_id = kwargs.pop('player_id')
		self.lvl = kwargs.pop('lvl')
		super(PortForm,self).__init__(*args,**kwargs)
		player = Player.objects.get(id = int(self.player_id))
		if player.tribe.name == 'Partisans':
			army = Partisan_troops.objects.get(id = 1)
		elif player.tribe.name == 'Russians':
			army = Russian_troops.objects.get(id = 1)
		elif player.tribe.name == 'Americans':
			army = American_troops.objects.get(id = 1)
		elif player.tribe.name == 'Brittish':
			army = Brittish_troops.objects.get(id = 1)
		elif player.tribe.name == 'Germans':
			army = German_troops.objects.get(id = 1)
		elif player.tribe.name == 'Japanese':
			army = Japanese_troops.objects.get(id = 1)
		self.fields['t8'].label = army.t8.troop.name 
		self.fields['t9'].label = army.t9.troop.name
		self.fields['t10'].label = army.t10.troop.name
		self.fields['t11'].label = army.t11.troop.name
		self.fields['t8'].help_text ='<br> <img src="' + army.t8.troop.image.url+'" class="margin-bottom" style="max-width: 60px" alt=""> <br>' + ' Oil: ' + str(army.t8.troop.training_cost.oil) + ' Iron: ' + str(army.t8.troop.training_cost.iron) + ' Wood: ' + str(army.t8.troop.training_cost.wood) + ' Food: ' + str(army.t8.troop.training_cost.food) + ' Costs: ' + str(army.t8.troop.consumption) + '<br> Training time: '+time(army.t8.troop.training_time, self.lvl)
		self.fields['t9'].help_text = '<br> <img src="' + army.t9.troop.image.url+'" class="margin-bottom" style="max-width: 60px" alt=""> <br>' + ' Oil: ' + str(army.t9.troop.training_cost.oil) + ' Iron: ' + str(army.t9.troop.training_cost.iron) + ' Wood: ' + str(army.t9.troop.training_cost.wood) + ' Food: ' + str(army.t9.troop.training_cost.food) + ' Costs: ' + str(army.t9.troop.consumption) + '<br> Training time: '+time(army.t9.troop.training_time, self.lvl)
		self.fields['t10'].help_text ='<br> <img src="' + army.t10.troop.image.url+'" class="margin-bottom" style="max-width: 60px" alt=""> <br>' + ' Oil: ' + str(army.t10.troop.training_cost.oil) + ' Iron: ' + str(army.t10.troop.training_cost.iron) + ' Wood: ' + str(army.t10.troop.training_cost.wood) + ' Food: ' + str(army.t10.troop.training_cost.food) + ' Costs: ' + str(army.t10.troop.consumption) + '<br> Training time: '+time(army.t10.troop.training_time, self.lvl)
		self.fields['t11'].help_text ='<br> <img src="' + army.t11.troop.image.url+'" class="margin-bottom" style="max-width: 60px" alt=""> <br>' + ' Oil: ' + str(army.t11.troop.training_cost.oil) + ' Iron: ' + str(army.t11.troop.training_cost.iron) + ' Wood: ' + str(army.t11.troop.training_cost.wood) + ' Food: ' + str(army.t11.troop.training_cost.food) + ' Costs: ' + str(army.t11.troop.consumption) + '<br> Training time: '+time(army.t11.troop.training_time, self.lvl)
		if player.last_village.army.t8.count == -1:
			self.fields['t8'].widget = form.HiddenInput()
		if player.last_village.army.t9.count == -1:
			self.fields['t9'].widget = form.HiddenInput()
		if player.last_village.army.t10.count == -1:
			self.fields['t10'].widget = form.HiddenInput()
		if player.last_village.army.t11.count == -1:
			self.fields['t11'].widget = form.HiddenInput()
	t8 = forms.IntegerField(required = False, min_value=1)
	t9 = forms.IntegerField(required = False, min_value=1)
	t10 = forms.IntegerField(required = False, min_value=1)
	t11 = forms.IntegerField(required = False, min_value=1)
	class Meta:
		fields = ('t8', 't9', 't10', 't11')	

class ParliForm(forms.Form):
	def __init__(self,*args,**kwargs):
		self.player_id = kwargs.pop('player_id')
		self.lvl = kwargs.pop('lvl')
		super(CampForm,self).__init__(*args,**kwargs)
		player = Player.objects.get(id = int(self.player_id))
		if player.tribe.name == 'Partisans':
			army = Partisan_troops.objects.get(id = 1)
		elif player.tribe.name == 'Russians':
			army = Russian_troops.objects.get(id = 1)
		elif player.tribe.name == 'Americans':
			army = American_troops.objects.get(id = 1)
		elif player.tribe.name == 'Brittish':
			army = Brittish_troops.objects.get(id = 1)
		elif player.tribe.name == 'Germans':
			army = German_troops.objects.get(id = 1)
		elif player.tribe.name == 'Japanese':
			army = Japanese_troops.objects.get(id = 1)
		self.fields['t12'].label = army.t12.troop.name 
		self.fields['t13'].label = army.t13.troop.name
		self.fields['t12'].help_text ='<br> <img src="' + army.t12.troop.image.url+'" class="margin-bottom" style="max-width: 60px" alt=""> <br>' + ' Oil: ' + str(army.t12.troop.training_cost.oil) + ' Iron: ' + str(army.t12.troop.training_cost.iron) + ' Wood: ' + str(army.t12.troop.training_cost.wood) + ' Food: ' + str(army.t12.troop.training_cost.food) + ' Costs: ' + str(army.t12.troop.consumption) + '<br> Training time: '+time(army.t12.troop.training_time, self.lvl)
		self.fields['t13'].help_text = '<br> <img src="' + army.t13.troop.image.url+'" class="margin-bottom" style="max-width: 60px" alt=""> <br>' + ' Oil: ' + str(army.t13.troop.training_cost.oil) + ' Iron: ' + str(army.t13.troop.training_cost.iron) + ' Wood: ' + str(army.t13.troop.training_cost.wood) + ' Food: ' + str(army.t13.troop.training_cost.food) + ' Costs: ' + str(army.t13.troop.consumption) + '<br> Training time: '+time(army.t13.troop.training_time, self.lvl)
		if player.last_village.army.t12.count == -1:
			self.fields['t12'].widget = form.HiddenInput()
		if player.last_village.army.t13.count == -1:
			self.fields['t13'].widget = form.HiddenInput()
	t12 = forms.IntegerField(required = False, min_value=1)
	t13 = forms.IntegerField(required = False, min_value=1)
	class Meta:
		fields = ('t12', 't13')
