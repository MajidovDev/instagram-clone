from django.urls import path
from users.views import CreateUserView, VerifyAPIView, GetNewVerification, ChangeUserInfoView, ChangeUserPhotoView

urlpatterns = [
    path('signup/', CreateUserView.as_view()),
    path('verify/', VerifyAPIView.as_view()),
    path('new-verify/', GetNewVerification.as_view()),
    path('change-user-info/', ChangeUserInfoView.as_view()),
    path('change-user-photo/', ChangeUserPhotoView.as_view()),
]