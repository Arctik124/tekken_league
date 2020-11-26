from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, CreateView, DetailView, UpdateView
from django.utils.http import urlencode
from django.urls import reverse
from .forms import BattleModelForm
from .models import Battle


class BattleDetailView(DetailView):
    # queryset = Article.objects.all()

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
            battle = Battle(player1=request.user.userprofile)
            form = BattleModelForm(instance=battle)
            ctx = {'form': form}
            return render(request, self.template_name, ctx)
        else:
            loginurl = reverse('home:login') + '?' + urlencode({'next': request.path})
            return redirect(loginurl)

    def post(self,  request,  *args, **kwargs):
        fill = {
            'player1': request.user.userprofile,
            'player2': request.POST['player2'],
            'max_score': request.POST['max_score'],
            'player1_score': 0,
            'player2_score': 0,
        }
        form = BattleModelForm(fill)

        if form.is_valid():
            form.save()
            return redirect(reverse('home:profile'))
        else:
            form = BattleModelForm(fill)
            ctx = {'form': form}
            return render(request, self.template_name, ctx)
        # battle_page_url = reverse('battles:battle-detail-id', kwargs={'id': form.cleaned_data['pk']})
        # return render(request, self.template_name, ctx)