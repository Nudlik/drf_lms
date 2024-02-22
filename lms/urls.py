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

    path('lessons/', views.LessonListView.as_view(), name='lesson-list'),
    path('lessons/create/', views.LessonCreateView.as_view(), name='lesson-create'),
    path('lessons/<int:pk>/', views.LessonDetailView.as_view(), name='lesson-detail'),
    path('lessons/<int:pk>/update/', views.LessonUpdateView.as_view(), name='lesson-update'),
    path('lessons/<int:pk>/delete/', views.LessonDeleteView.as_view(), name='lesson-delete'),

    path('subs/', views.SubscriptionDetailAPIView.as_view(), name='sub-detail'),
    path('subs/<int:pk>/', views.SubscriptionCreateDeleteAPIView.as_view(), name='sub-create-delete'),
]
