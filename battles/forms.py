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
            'active',
            'delta',
            'winner'
        ]

    def __init__(self, *args, **kwargs):

        if 'user_name' in kwargs:
            value = kwargs['user_name']
            del kwargs['user_name']
            super(BattleModelForm, self).__init__(*args, **kwargs)
            self.fields['player1'].queryset = UserProfile.objects.filter(user__username=value)
            self.fields['player2'].queryset = UserProfile.objects.exclude(user__username=value)
            self.fields['max_score'].widget.attrs['min'] = 2

        else:
            super(BattleModelForm, self).__init__(*args, **kwargs)
            self.fields['max_score'].widget.attrs['min'] = 2

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

        if max_score <= 1:
            raise forms.ValidationError('Minimum FT2!')
        if player1.user.username == player2.user.username:
            raise forms.ValidationError('Can\'t fight with yourself!')
        if player1_score > max_score:
            raise forms.ValidationError("Score is bigger than FT")
        if player2_score > max_score:
            raise forms.ValidationError("Score is bigger than FT")
        if player1_score == max_score and player1_score == player2_score:
            raise forms.ValidationError('There can be only one winner!')
