from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, DetailView
from django.utils.http import urlencode
from django.urls import reverse
from .forms import BattleModelForm
from .models import Battle
from home.models import UserProfile


class BattleDetailView(DetailView):
    def get_object(self, queryset=None):
        id_ = self.kwargs.get('id')
        return get_object_or_404(Battle, id=id_)


class BattleUpdateView(View):
    template_name = 'battles/battle_update.html'

    def get_object(self):
        id = self.kwargs.get('id')
        if id is not None:
            obj = get_object_or_404(Battle, id=id)
        return obj

    def get(self, request, id=None, *args, **kwargs):
        ctx = {}
        obj = self.get_object()
        if obj is not None:
            if obj.active:
                form = BattleModelForm(instance=obj)
                ctx['object'] = obj
                ctx['form'] = form
            else:
                return redirect(obj.get_absolute_url())
        return render(request, self.template_name, ctx)

    def post(self,  request, id=None, *args, **kwargs):
        ctx = {}
        obj = self.get_object()
        if obj is not None:
            fill = {
                'player1': obj.player1,
                'player2': obj.player2,
                'max_score': obj.max_score,
                'player1_score': request.POST['player1_score'],
                'player2_score': request.POST['player2_score'],
            }

            form = BattleModelForm(fill, instance=obj)
            if form.is_valid():
                a = int(fill['max_score'])
                b = int(fill['player1_score'])
                c = int(fill['player2_score'])
                if a == b or a == c:
                    fill['active'] = False
                    fill['winner'] = b > c

                    delta = change_mmr([int(fill['player1_score']), int(fill['player2_score'])])

                    fill['delta'] = delta

                    print('delta ->', delta)
                    p1 = UserProfile.objects.get(user__username=fill['player1'])
                    p2 = UserProfile.objects.get(user__username=fill['player2'])

                    p1.rating = p1.rating+delta
                    p2.rating = p2.rating-delta
                    p1.save()
                    p2.save()
                else:
                    fill['active'] = True
                form = BattleModelForm(fill, instance=obj)
                form.save()
            else:
                ctx['object'] = obj
                ctx['form'] = form
                return render(request, self.template_name, ctx)
        return redirect('home:profile')


class BattleCreateView(View):
    template_name = 'battles/battle_create.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = BattleModelForm(user_name=request.user.username)
            ctx = {'form': form}
            return render(request, self.template_name, ctx)
        else:
            loginurl = reverse('home:login') + '?' + urlencode({'next': request.path})
            return redirect(loginurl)

    def post(self,  request,  *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('home:login'))
        fill = {
            'player1':  request.POST['player1'],
            'player2': request.POST['player2'],
            'max_score': request.POST['max_score'],
            'player1_score': 0,
            'player2_score': 0,
            'active': True
        }
        form = BattleModelForm(fill)

        if form.is_valid():
            form.save()
            return redirect(reverse('home:profile'))
        else:
            return redirect(reverse('battles:create-battle'))


def change_mmr(score):
    # typical win/lose k1
    std_delta = 15
    k1 = 1
    winner = score[0] - score[1] > 0
    if not winner:
        k1 = -k1

    # # mmr difference factor k2
    # max_diff = 500
    # dif = p1 - p2
    # if dif > max_diff:
    #     dif = max_diff
    # if dif < -max_diff:
    #     dif = -max_diff
    # if winner:
    #     k2 = 1 - (dif / (max_diff * 2))
    # else:
    #     k2 = 1 + (dif / (max_diff * 2))

    # ft length factor k3
    ft_max = 10
    ft_min = 3
    ft_len = max(score)
    k3 = 1 + (ft_len - ft_min) / (ft_max - ft_min) / 10

    # mmr difference factor k4
    score_dif = abs(score[0] - score[1])
    if score_dif > 2:
        k4 = 1 + score_dif / (ft_len * 4)
    else:
        k4 = 1

    delta = int(std_delta * k1 * k4 * k3)

    return delta
