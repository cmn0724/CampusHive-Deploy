# users/urls.py
from django.urls import path
from .views import SignUpView
from .views import StudentDashboardView
from .views import StudentScheduleView, UserProfileView
from django.contrib.auth import views as auth_views
from .forms import CustomLoginForm # 导入自定义登录表单

app_name = 'users'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('dashboard/student/', StudentDashboardView.as_view(), name='student_dashboard'),
    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html', # 登录模板路径
        authentication_form=CustomLoginForm      # 指定使用自定义表单
    ), name='login'),
    path('my-schedule/', StudentScheduleView.as_view(), name='student_schedule'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
]

