from django.urls import path, include
from cv import views
from rest_framework.routers import SimpleRouter


router = SimpleRouter()

router.register('templates', views.ResumeTemplateViewset, basename='templates')
router.register("", views.ResumeViewset, basename="resume")

urlpatterns = [
    path("download/<int:pk>/", views.ResumePDFView.as_view()),
] + router.urls
