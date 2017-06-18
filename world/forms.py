from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from world.models import Tribe
from django.utils.translation import ugettext_lazy as _
from nocaptcha_recaptcha.fields import NoReCaptchaField

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
	subject = forms.CharField(max_length = 50, help_text=_('Subject'))
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

class SetLeader(forms.Form):
	leader = forms.CharField(max_length= 25, help_text=_("Player's name"))
	position = forms.CharField(max_length= 25, help_text=_("Position"))
	mm_rights = forms.BooleanField(help_text=_("Mass message rights"))
	diplomacy_rights = forms.BooleanField(help_text=_("Diplomacy rights"))
	class Meta:
		fields = ('leader','position','mm_rights','diplomacy_rights')
