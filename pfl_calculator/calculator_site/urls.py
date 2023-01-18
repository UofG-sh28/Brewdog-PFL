from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # INFO. PAGES
    path('outline/', views.outline, name="outline"),
    path('scope/', views.scope, name="scope"),
    #
    # LOGIN PAGE
    path('login/', views.login, name="login"),
    #
    # # ADMIN PAGES
    # path('admin/dashboard', views.admin_dash, name='admin_dash'),
    #
    # # REGISTER PAGE
    # path('register/', views.register, name='register'),
    # path('register/about', views.about, name='about'),
    #
    # # USER PAGES
    path('my/dashboard/', views.dash, name='dash'),
    path('my/calculator/', views.CalculatorLoaderView().calculator, name='calculator'),
    path('my/metrics', views.metrics, name='metrics'),
    path('my/report', views.report, name='report'),
    path('my/pledges', views.pledges, name='pledges'),
    path('my/action_plan', views.action_plan, name='action_plan'),
    path('my/profile', views.profile, name='profile'),

]
