# users/views.py
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import ListView,  DetailView
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login # To log in the user immediately after registration
# from .forms import SignUpForm, UserProfileForm
from .forms import CustomUserCreationForm
from .models import User, Department
from courses.models import Enrollment
from .mixins import StudentRequiredMixin, TeacherRequiredMixin


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home') # Redirect to home after successful registration
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        # Log the user in after successful registration
        login(self.request, self.object)
        return response

class StudentDashboardView(LoginRequiredMixin, StudentRequiredMixin, ListView):
    model = Enrollment # We are listing enrollments
    template_name = 'users/student_dashboard.html'
    context_object_name = 'enrollments'

    def get_queryset(self):
        # Get enrollments for the current logged-in student
        return Enrollment.objects.filter(student=self.request.user).select_related('course').order_by('course__title')

class StudentScheduleView(LoginRequiredMixin, StudentRequiredMixin, ListView): # 或者 TemplateView
    model = Enrollment # 如果你想列出课程安排
    template_name = 'users/student_schedule.html' # *** 需要创建这个模板 ***
    context_object_name = 'enrollments_for_schedule' # 或者其他你需要的上下文变量
    def get_queryset(self):
        # 获取当前学生已选的课程，可以进一步处理以生成课表视图
        # 例如，如果 Course 模型有 time/day 字段，可以在这里筛选和排序
        return Enrollment.objects.filter(student=self.request.user).select_related('course', 'course__instructor').order_by('course__code') # 示例
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "My Schedule"
        # 你可能还需要传递额外的数据来帮助渲染课表，比如一周的天数、时间段等
        return context

class UserProfileView(LoginRequiredMixin, DetailView):
    model = User  # 我们要显示 User 模型的信息
    template_name = 'users/user_profile.html'  # 指定模板文件
    context_object_name = 'profile_user'  # 在模板中使用的上下文变量名
    def get_object(self, queryset=None):
        """
        这个方法返回视图将要显示的对象。
        在这里，我们希望显示当前登录用户的个人资料。
        """
        return self.request.user