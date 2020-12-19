from django import forms
from .models import Battle
from home.models import UserProfile


class BattleModelForm(forms.ModelForm):
    class Meta:
        model = Battle
        fields = [
            'player1',
            'player2',
            'max_score',
            'player1_score',
            'player2_score',
            'active'
        ]

    def __init__(self, username=None, *args, **kwargs):
        super(BattleModelForm, self).__init__(*args, **kwargs)
#        if username is not None:
#             self.fields['player1'].queryset = UserProfile.objects.filter(user__username=username)
#             self.fields['player2'].queryset = UserProfile.objects.exclude(user__username=username)

    def clean_max_score(self):
        max_score = self.cleaned_data.get('max_score')

        if max_score <= 1:
            raise forms.ValidationError('Minimum FT2!')
        else:
            return max_score

    def clean(self):
        cleaned_data = super().clean()
        player1_score = cleaned_data.get("player1_score")
        player2_score = cleaned_data.get("player2_score")
        max_score = cleaned_data.get("max_score")
        player2 = cleaned_data.get('player2')
        player1 = cleaned_data.get('player1')
        print('player1', player1)
        print('player2', player2)
        print('max_score', max_score)
        print('player1_score', player1_score)
        print('player2_score', player2_score)

        if player1.user.username == player2.user.username:
            raise forms.ValidationError('Cant fight with yourself!')
        if player1_score > max_score:
            raise forms.ValidationError("Score is bigger than FT")
        if player2_score > max_score:
            raise forms.ValidationError("Score is bigger than FT")
        if player1_score == max_score and player1_score == player2_score:
            raise forms.ValidationError('There can be only one winner!')
