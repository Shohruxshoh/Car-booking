from django.urls import path
from .views import RegisterView, LoginView, CustomTokenRefreshView, LogoutView, ChangePasswordView, UserListView, \
    UserResetPasswordView, UserApiView, JobCreateView, CompanyCreateListView, CompanyUpdateDeleteView, JobListView, \
    JobUpdateDeleteView

urlpatterns = [
    path('', UserApiView.as_view(), name='user-get'),
    path('admin/', UserListView.as_view(), name='list'),
    path('job-create/', JobCreateView.as_view(), name='job-create'),
    path('jobs/', JobListView.as_view(), name='jobs'),
    path('job/<int:pk>/', JobUpdateDeleteView.as_view(), name='job'),
    # login and register
    path('login/', LoginView.as_view(), name='login'),
    path('login/refresh/', CustomTokenRefreshView.as_view(), name="token_refresh"),
    path("register/", RegisterView.as_view(), name="register"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('admin/reset-password/<int:pk>', UserResetPasswordView.as_view(), name='reset-password'),

    # Company
    path("company/", CompanyCreateListView.as_view()),
    path("company/<int:pk>/", CompanyUpdateDeleteView.as_view()),
]
