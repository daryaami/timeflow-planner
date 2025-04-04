from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .apis import TaskViewSet, CategoryViewSet, TimeLogViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'timelogs', TimeLogViewSet, basename='timelog')