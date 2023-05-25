from django.urls import path
from users.views import CreateUserView, VerifyAPIView, GetNewVerification, ChangeUserInfoView, ChangeUserPhotoView, LoginView, LoginRefreshView, LogOutView,ForgotPasswordView

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('login/refresh/', LoginRefreshView.as_view()),
    path('logout/', LogOutView.as_view()),
    path('signup/', CreateUserView.as_view()),
    path('verify/', VerifyAPIView.as_view()),
    path('new-verify/', GetNewVerification.as_view()),
    path('change-user-info/', ChangeUserInfoView.as_view()),
    path('change-user-photo/', ChangeUserPhotoView.as_view()),
    path('forgot-password/', ForgotPasswordView.as_view()),
]