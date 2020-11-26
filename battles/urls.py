from django.urls import path
from . import views

app_name = 'battles'
urlpatterns = [
    # path('', views.index, name='index'),
    path('create/', views.BattleCreateView.as_view(), name='create-battle'),
    path('<int:id>/', views.BattleDetailView.as_view(), name='battle-detail-id'),
    path('<int:id>/update/', views.BattleUpdateView.as_view(), name='battle-update-id'),

]
