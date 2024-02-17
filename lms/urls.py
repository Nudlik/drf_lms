from django.urls import path, include
from rest_framework import routers

from lms import apps
from lms.views.course import CourseViewSet
from lms import views

app_name = apps.LmsConfig.name

router = routers.DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')

urlpatterns = [
    path('', include(router.urls)),

    path('lessons/', views.LessonListCreateView.as_view(), name='lesson_list_or_create'),
    path('lessons/<int:pk>/', views.LessonDetailView.as_view(), name='lesson_detail'),
    path('lessons/<int:pk>/update/', views.LessonUpdateView.as_view(), name='lesson_update'),
    path('lessons/<int:pk>/delete/', views.LessonDeleteView.as_view(), name='lesson_delete'),
]
