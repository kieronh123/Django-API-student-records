from django.urls import path
from . import views
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'Professor', views.ProfessorsViewSet)

urlpatterns = [
    path('register/', views.create_user, name='create_user'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.logout_request, name='logout_request'),
    path('professor/', views.GetProfessors, name='get_professor'),
    path('rate/', views.rate_professor, name='rate_professor'),
    path('', include(router.urls)),
    path('average/', views.get_ratings_for_professor, name='get_ratings_for_professor'),
    path('view/', views.view_professors_ratings, name='view_professors_ratings'),
    path('list/', views.list_professors, name='list_professors')

]
