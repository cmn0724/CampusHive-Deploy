# courses/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin # Ensure user is logged in
from django.contrib import messages
from .models import Course, Enrollment, CourseMaterial 
from .models import Assignment, Submission
from .forms import CourseForm
from .forms import CourseCreationForm # Phase 3
from .forms import CourseMaterialForm
from .forms import AssignmentForm #, SubmissionForm (later)
from .forms import EnrollmentGradeFormSet
from .forms import SubmissionForm
from .forms import GradeSubmissionForm
from .forms import CourseCreationForm
from users.mixins import TeacherRequiredMixin, StudentRequiredMixin # 从阶段三复用
from users.models import User # 确保 User 模型导入
from django.views import View
from .filters import CourseFilter
# from .forms import EnrollmentGradeModelFormSet



class CourseListView(LoginRequiredMixin, ListView): # All logged-in users can see courses
    model = Course
    template_name = 'courses/course_list.html' # Path to your template
    context_object_name = 'courses' # Name to use in the template for the list of courses
    paginate_by = 10 # Optional: for pagination

    def get_queryset(self):
        # Optionally, filter courses, e.g., by active status, semester, etc.
        queryset = super().get_queryset() 
        # 使用 request.GET 中的参数来初始化 FilterSet，并用它来筛选 queryset
        self.filterset = CourseFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs.order_by('code') # Or any other ordering
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 将 filterset 实例传递给模板，以便在模板中渲染筛选表单
        context['filterset'] = self.filterset
        return context
    
class CourseCreateViewActual(LoginRequiredMixin, TeacherRequiredMixin, CreateView):
    model = Course
    form_class = CourseCreationForm # 指定用于创建课程的表单
    template_name = 'courses/course_form.html' # 用于创建/编辑课程的模板
    success_url = reverse_lazy('courses:course_list') # 创建成功后重定向到课程列表
    
    def form_valid(self, form):
        # 在保存表单之前，将当前登录的教师用户设置为课程的创建者
        form.instance.instructor = self.request.user
        messages.success(self.request, f"Course '{form.instance.title}' created successfully.")
        return super().form_valid(form)
    
    def get_form_kwargs(self):
        """Pass the request.user to the form if your form needs it."""
        kwargs = super().get_form_kwargs()
        kwargs['request_user'] = self.request.user # 如果 CourseCreationForm 需要 request.user
        return kwargs
    # model = Assignment
    # form_class = AssignmentForm
    # template_name = 'courses/create_assignment.html' # 这是我们之前创建的模板
    # def setup(self, request, *args, **kwargs):
    #     """在视图处理开始前，获取 course 对象。"""
    #     super().setup(request, *args, **kwargs)
    #     # 从 URL 关键字参数中获取 course_id
    #     self.course = get_object_or_404(Course, id=self.kwargs['course_id'])
    # def test_func(self):
    #     """
    #     TeacherRequiredMixin 检查用户是否是教师。
    #     这里我们进一步检查该教师是否是当前课程的授课教师。
    #     """
    #     # TeacherRequiredMixin 已经执行了 is_teacher 检查
    #     # self.course 是在 setup 方法中设置的
    #     return self.request.user == self.course.instructor
    # def form_valid(self, form):
    #     """如果表单有效，保存关联的课程并设置创建者（如果需要）。"""
    #     form.instance.course = self.course # 将作业与当前课程关联
    #     # 如果 Assignment 模型有 'created_by' 或类似字段，可以在这里设置:
    #     # form.instance.created_by = self.request.user
    #     messages.success(self.request, f"Assignment '{form.instance.title}' created successfully for {self.course.title}.")
    #     return super().form_valid(form)
    # def get_success_url(self):
    #     """创建成功后，重定向到课程详情页面。"""
    #     return reverse('courses:course_detail', kwargs={'pk': self.course.pk})
    # def get_context_data(self, **kwargs):
    #     """将 course 对象添加到模板上下文中，以便在模板中使用（例如显示课程标题）。"""
    #     context = super().get_context_data(**kwargs)
    #     context['course'] = self.course # 将 course 实例传递给模板
    #     # context['page_title'] = f"Create Assignment for {self.course.title}" # 可选：设置页面标题
    #     return context

class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        user = self.request.user

        # 检查当前用户是否已选修此课程 (如果是学生)
        if user.is_authenticated and user.is_student: # 假设 User 模型有 is_student 属性
            context['is_enrolled'] = Enrollment.objects.filter(student=user, course=course).exists()
            # 如果允许退选，可以获取 enrollment_id
            if context['is_enrolled']:
                try:
                    enrollment = Enrollment.objects.get(student=user, course=course)
                    context['enrollment_id'] = enrollment.id
                except Enrollment.DoesNotExist:
                    pass # Should not happen if is_enrolled is True

        # (稍后添加) 获取课程资料列表
        # context['materials'] = course.materials.all() # 假设 related_name='materials'

        # (稍后添加) 获取作业列表
        # context['assignments'] = course.assignments.all() # 假设 related_name='assignments'

        # 获取选课学生列表 (仅授课教师或管理员可见)
        if user.is_teacher and course.instructor == user: # 假设 User 模型有 is_teacher 属性
            context['enrolled_students'] = User.objects.filter(enrollments__course=course, role=User.ROLE_STUDENT)
        
        return context

class CourseUpdateView(LoginRequiredMixin, TeacherRequiredMixin, UpdateView):
    model = Course
    form_class = CourseCreationForm # Reuse the form from create view
    template_name = 'courses/course_form.html' # Reuse the template from create view
    # success_url = reverse_lazy('courses:course_list') # Or redirect to course_detail

    def get_success_url(self):
        return reverse('courses:course_detail', kwargs={'pk': self.object.pk})

    def test_func(self):
        # Override TeacherRequiredMixin's test_func if needed for more specific permission
        # e.g., only the course instructor or a superuser can edit
        course = self.get_object()
        return super().test_func() and (self.request.user == course.instructor or self.request.user.is_superuser)

class CourseDeleteView(LoginRequiredMixin, TeacherRequiredMixin, DeleteView):
    model = Course
    template_name = 'courses/course_confirm_delete.html'
    success_url = reverse_lazy('courses:course_list')

    def test_func(self):
        course = self.get_object()
        return super().test_func() and (self.request.user == course.instructor or self.request.user.is_superuser)

    def post(self, request, *args, **kwargs):
        messages.success(request, f"Course '{self.get_object().title}' has been deleted.")
        return super().post(request, *args, **kwargs)
    
class EnrollCourseView(LoginRequiredMixin, StudentRequiredMixin, View):
    def post(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        student = request.user

        # Check if already enrolled
        if Enrollment.objects.filter(student=student, course=course).exists():
            messages.warning(request, f"You are already enrolled in '{course.title}'.")
        else:
            # TODO: Add any other enrollment conditions (e.g., course capacity, prerequisites)
            Enrollment.objects.create(student=student, course=course)
            messages.success(request, f"You have successfully enrolled in '{course.title}'.")
        return redirect('courses:course_detail', pk=course_id)

class DropCourseView(LoginRequiredMixin, StudentRequiredMixin, View):
    def post(self, request, enrollment_id): # Or use course_id and find enrollment
        enrollment = get_object_or_404(Enrollment, id=enrollment_id, student=request.user)
        course_id_for_redirect = enrollment.course.id
        course_title = enrollment.course.title
        
        # TODO: Add any conditions for dropping (e.g., deadline)
        enrollment.delete()
        messages.success(request, f"You have successfully dropped '{course_title}'.")
        return redirect('courses:course_detail', pk=course_id_for_redirect)

class GradeEnrollmentsView(LoginRequiredMixin, TeacherRequiredMixin, View):
    template_name = 'courses/grade_enrollments.html'

    def get(self, request, course_id):
        course = get_object_or_404(Course, id=course_id, instructor=request.user) # Ensure only instructor can grade
        # Get enrollments for this course
        # enrollments_qs = Enrollment.objects.filter(course=course).select_related('student')
        # formset = EnrollmentGradeFormSet(instance=course)
        formset = EnrollmentGradeFormSet(instance=course, queryset=Enrollment.objects.filter(course=course).select_related('student'))
        return render(request, self.template_name, {'course': course, 'formset': formset})

    def post(self, request, course_id):
        course = get_object_or_404(Course, id=course_id, instructor=request.user)
        # enrollments_qs = Enrollment.objects.filter(course=course).select_related('student')

        # --- BEGIN DEBUG ---
        enrollments_for_course = Enrollment.objects.filter(course=course)
        print(f"Course: {course.title}")
        if not enrollments_for_course.exists():
            print("No enrollments found for this course.")
        for enrollment in enrollments_for_course:
            print(f"  Enrollment ID: {enrollment.id}, Student: {enrollment.student}, Student ID: {enrollment.student_id}, Grade: {enrollment.grade}")
        # --- END DEBUG ---
        
        # formset = EnrollmentGradeFormSet(request.POST, request.FILES, instance=course)
        formset = EnrollmentGradeFormSet(request.POST, request.FILES, instance=course, queryset=Enrollment.objects.filter(course=course).select_related('student'))

        if formset.is_valid():
            formset.save()
            messages.success(request, f"Grades for '{course.title}' have been updated.")
            return redirect('courses:grade_enrollments', course_id=course.id)
        else:
            print("Formset errors:", formset.errors)
            for form in formset:
                print(f"Form {form.prefix} errors:", form.errors)
            messages.error(request, "Please correct the errors below.")
        
        return render(request, self.template_name, {'course': course, 'formset': formset})

# Phase 4
class UploadMaterialView(LoginRequiredMixin, TeacherRequiredMixin, CreateView):
    model = CourseMaterial
    form_class = CourseMaterialForm
    template_name = 'courses/upload_material_form.html'
    # success_url will be set dynamically

    def setup(self, request, *args, **kwargs):
        """Get course_id from URL to associate material with course."""
        super().setup(request, *args, **kwargs)
        self.course = get_object_or_404(Course, id=self.kwargs['course_id'])

    def test_func(self):
        # Ensure only the instructor of this course can upload
        return super().test_func() and self.request.user == self.course.instructor

    def form_valid(self, form):
        form.instance.course = self.course
        form.instance.uploaded_by = self.request.user
        messages.success(self.request, f"Material '{form.instance.title}' uploaded successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('courses:course_detail', kwargs={'pk': self.course.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = self.course
        return context

class DeleteMaterialView(LoginRequiredMixin, TeacherRequiredMixin, DeleteView):
    model = CourseMaterial
    template_name = 'courses/material_confirm_delete.html' # Create this template
    context_object_name = 'material'

    def get_success_url(self):
        # Redirect back to the course detail page after deletion
        material = self.get_object()
        return reverse('courses:course_detail', kwargs={'pk': material.course.pk})

    def test_func(self):
        material = self.get_object()
        return super().test_func() and self.request.user == material.course.instructor

    def post(self, request, *args, **kwargs):
        messages.success(request, f"Material '{self.get_object().title}' has been deleted.")
        return super().post(request, *args, **kwargs)

class CreateAssignmentViewActual(LoginRequiredMixin, TeacherRequiredMixin, CreateView):
    model = Assignment
    form_class = AssignmentForm
    template_name = 'courses/create_assignment.html'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.course = get_object_or_404(Course, id=self.kwargs['course_id'])

    def test_func(self):
        return super().test_func() and self.request.user == self.course.instructor

    def form_valid(self, form):
        form.instance.course = self.course
        messages.success(self.request, f"Assignment '{form.instance.title}' created.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('courses:course_detail', kwargs={'pk': self.course.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = self.course
        return context

class UpdateAssignmentView(LoginRequiredMixin, TeacherRequiredMixin, UpdateView):
    model = Assignment
    form_class = AssignmentForm
    template_name = 'courses/assignment_form.html'
    context_object_name = 'assignment' # For template

    def test_func(self):
        assignment = self.get_object()
        return super().test_func() and self.request.user == assignment.course.instructor

    def get_success_url(self):
        return reverse('courses:assignment_detail', kwargs={'assignment_id': self.object.pk})

    def get_context_data(self, **kwargs): # Pass course to template for breadcrumbs/links
        context = super().get_context_data(**kwargs)
        context['course'] = self.get_object().course 
        return context

class DeleteAssignmentView(LoginRequiredMixin, TeacherRequiredMixin, DeleteView):
    model = Assignment
    template_name = 'courses/assignment_confirm_delete.html' # Create this
    context_object_name = 'assignment'

    def get_success_url(self):
        assignment = self.get_object()
        return reverse('courses:course_detail', kwargs={'pk': assignment.course.pk})
    
    def test_func(self):
        assignment = self.get_object()
        return super().test_func() and self.request.user == assignment.course.instructor
    
    def post(self, request, *args, **kwargs):
        messages.success(request, f"Assignment '{self.get_object().title}' has been deleted.")
        return super().post(request, *args, **kwargs)

class AssignmentDetailView(LoginRequiredMixin, DetailView):
    model = Assignment
    template_name = 'courses/assignment_detail.html'
    context_object_name = 'assignment'
    pk_url_kwarg = 'assignment_id' # If URL uses assignment_id instead of pk

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        assignment = self.get_object()
        user = self.request.user

        if user.is_student:
            # Check if student has already submitted for this assignment
            existing_submission = Submission.objects.filter(assignment=assignment, student=user).first()
            context['existing_submission'] = existing_submission
            if not existing_submission:
                context['submission_form'] = SubmissionForm() # Form for new submission
            # else:
                # Optionally, allow editing submission if form is for update
                # context['submission_form'] = SubmissionForm(instance=existing_submission)
        
        elif user.is_teacher and user == assignment.course.instructor:
            # Get all submissions for this assignment for the instructor to view
            context['submissions'] = assignment.submissions.all().select_related('student').order_by('student__username')
        
        return context

class SubmitAssignmentView(LoginRequiredMixin, StudentRequiredMixin, CreateView):
    model = Submission
    form_class = SubmissionForm
    template_name = 'courses/assignment_detail.html' # Or a dedicated submission template

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.assignment = get_object_or_404(Assignment, id=self.kwargs['assignment_id'])

    def dispatch(self, request, *args, **kwargs):
        # Prevent resubmission if already submitted
        if Submission.objects.filter(assignment=self.assignment, student=request.user).exists():
            messages.warning(request, "You have already submitted this assignment.")
            return redirect('courses:assignment_detail', assignment_id=self.assignment.id)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.assignment = self.assignment
        form.instance.student = self.request.user
        messages.success(self.request, f"Your submission for '{self.assignment.title}' has been received.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('courses:assignment_detail', kwargs={'assignment_id': self.assignment.id})

    # If using assignment_detail.html, need to pass assignment to context for the form action URL
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['assignment'] = self.assignment
        return context

class GradeSubmissionView(LoginRequiredMixin, TeacherRequiredMixin, UpdateView):
    model = Submission
    form_class = GradeSubmissionForm
    template_name = 'courses/grade_submission_form.html' # Create this
    context_object_name = 'submission'
    pk_url_kwarg = 'submission_id'

    def test_func(self):
        submission = self.get_object()
        return super().test_func() and self.request.user == submission.assignment.course.instructor

    def get_success_url(self):
        return reverse('courses:assignment_detail', kwargs={'assignment_id': self.object.assignment.id})

    def form_valid(self, form):
        messages.success(self.request, f"Grade and feedback for {form.instance.student.username}'s submission have been saved.")
        return super().form_valid(form)

class TeacherCourseManagementView(LoginRequiredMixin, TeacherRequiredMixin, ListView):
    model = Course
    template_name = 'courses/manage_teacher_courses.html' # *** 需要创建这个模板 ***
    context_object_name = 'courses'
    paginate_by = 10
    def get_queryset(self):
        # 只显示当前登录教师创建的课程
        return Course.objects.filter(instructor=self.request.user).order_by('-created_at') # 或者其他排序
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Manage My Courses"
        return context