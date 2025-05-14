# courses/views.py
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin # Ensure user is logged in
from .models import Course
from .forms import CourseForm 
from users.mixins import TeacherRequiredMixin 
# from users.mixins import StudentRequiredMixin, TeacherRequiredMixin # If you want role specific list views

class CourseListView(LoginRequiredMixin, ListView): # All logged-in users can see courses
    model = Course
    template_name = 'courses/course_list.html' # Path to your template
    context_object_name = 'courses' # Name to use in the template for the list of courses
    paginate_by = 10 # Optional: for pagination

    def get_queryset(self):
        # Optionally, filter courses, e.g., by active status, semester, etc.
        return Course.objects.all().order_by('code') # Or any other ordering
    
class CourseCreateView(LoginRequiredMixin, TeacherRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm # 指定用于创建课程的表单
    template_name = 'courses/course_form.html' # 用于创建/编辑课程的模板
    success_url = reverse_lazy('courses:course_list') # 创建成功后重定向到课程列表
    def form_valid(self, form):
        # 在保存表单之前，将当前登录的教师用户设置为课程的创建者
        form.instance.instructor = self.request.user
        return super().form_valid(form)