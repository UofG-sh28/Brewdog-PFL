from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # INFO. PAGES
    path('outline/', views.outline, name="outline"),
    path('scope/', views.scope, name="scope"),
    path("how-it-works", views.how_it_works, name="how-it-works"),
    #
    # LOGIN PAGE
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name='logout'),
    #
    # # ADMIN PAGES
    path('staff/dashboard', views.staff_dash, name='staff_dash'),
    path('staff/admin_report/', views.admin_report, name='admin_report'),
    re_path(r'^staff/report/(?P<year>\d+)/', views.generate_admin_report, name='generate_admin_report'),
    #
    # # REGISTER PAGE
    path('register/', views.register, name='register'),
    path('register/about', views.register2, name='register2'),
    #
    # # USER PAGES

    path('my/dashboard/', views.DashboardViewLoader().dash, name='dash'),
    path('my/calculator/', views.CalculatorLoaderView().calculator, name='calculator'),
    path('my/metrics', views.metrics, name='metrics'),
    path('my/report', views.report, name='report'),
    path('my/pledges', views.PledgeLoaderView().pledges, name='pledges'),
    path('my/pledge-report', views.action_plan, name='action_plan'),
    path('my/profile', views.profile, name='profile'),
    path('my/account', views.account, name='account'),
    path('my/feedback', views.FeedbackLoaderView().feedback, name='feedback'),

    path('my/action-plan', views.ActionPlanDetailLoaderView().action_plan_detail, name='action_plan_detail'),

    re_path(r'^my\/.*$', views.dash_redirect, name='dash_redirect'),


]
