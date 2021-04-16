from django.urls import path

from . import views 

app_name = 'jegkan'
urlpatterns = [
# ex: /jegkan/
    path('', views.jk_views.index, name='index'),
    
    
    
    
    # category
    path('category/<int:topic_id>/', views.jk_views.categorydetails, name='topicdetails'),
    path('category/edit/<int:topic_id>/', views.jk_views.manage_questions, name='manage_questions'),
    path('category/results/<int:topic_id>/', views.jk_views.category_results, name='cat_results'),
    path("surveys/<int:topic_id>/", views.jk_views.submit, name="survey-submit"),
    path('mypage', views.jk_views.student_overview, name="min-side"),
    path("signup/", views.auth.register, name="register"),
    path("login/", views.auth.logg_inn, name="login"),
    path("logout/", views.auth.logout_request, name="logged-out"),
]