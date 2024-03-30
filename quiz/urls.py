from django.urls import path
from . import views

urlpatterns = [
    path('all_quiz/', views.all_quiz, name='all_quiz'),
    path('search/<str:category>', views.search_view, name='search'),
    path('<int:quiz_id>/', views.quiz_view, name='quiz')
]