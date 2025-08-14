# courses/admin.py
from django.contrib import admin
# Register your models here.
from django.utils.translation import gettext_lazy as _ # 导入翻译函数
from .models import Class, Course, Enrollment # 导入所有需要管理的模型
from users.models import StudentProfile

# 定义 StudentProfile 的内联管理类
# 这个内联是专门为 Class 模型设计的，通过 StudentProfile 的 assigned_class 字段关联
class StudentInClassInline(admin.TabularInline): # TabularInline 适合表格形式，StackedInline 适合堆叠形式
    model = StudentProfile
    fk_name = 'assigned_class' # 指定 StudentProfile 中哪个外键指向 Class
    extra = 1 # 默认显示 1 个空表单行，方便添加新学生
    fields = ('user', 'student_id_number', 'enrollment_date') # 你想在内联中显示的 StudentProfile 字段
    # 如果你不想让用户在 Class 页面直接创建新的 User，可以设置为 readonly_fields
    # 或者将 'user' 字段设置为只读，并提供一个链接到 User 编辑页
    # readonly_fields = ('user',)

@admin.register(Class) # 注册 Class 模型
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'academic_year', 'advisor', 'get_student_count') # 列表页显示的字段
    search_fields = ('name', 'academic_year', 'advisor__username') # 可搜索的字段
    list_filter = ('academic_year',) # 可筛选的字段
    autocomplete_fields = ['advisor'] # 为 'advisor' (班主任) 字段启用自动完成

    # 添加内联
    inlines = [StudentInClassInline]

    # def get_student_count(self, obj):
    #     # 假设 StudentProfile 中有 class_assigned 字段，并且 related_name='students'
    #     if hasattr(obj, 'students'): # 检查是否存在 'students' 反向关联
    #          return obj.students.count()
    #     return 0 # 如果没有，返回0
    # get_student_count.short_description = _('Number of Students') # 列的显示名称

    def get_student_count(self, obj):
        # 这个方法现在将正确地通过 related_name='students' 来计数关联的学生
        return obj.students.count()
    get_student_count.short_description = _('Number of Students')

@admin.register(Course) # 注册 Course 模型
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'department', 'instructor', 'credits', 'schedule_information', 'get_enrollment_count') # 列表页显示的字段
    search_fields = ('code', 'title', 'instructor__username', 'department__name') # 可搜索的字段
    list_filter = ('department', 'credits', 'instructor') # 可筛选的字段
    autocomplete_fields = ['department', 'instructor'] # 为 'department' 和 'instructor' 字段启用自动完成
    def get_enrollment_count(self, obj):
        # Enrollment 模型中 course 字段的 related_name 默认为 'enrollment_set' 或你自定义的 'enrollments'
        return obj.enrollments.count()
    get_enrollment_count.short_description = _('Enrolled Students') # 列的显示名称

@admin.register(Enrollment) # 注册 Enrollment 模型
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrollment_date') # 列表页显示的字段 (后续可以添加 'grade')
    search_fields = ('student__username', 'student__student_profile__student_id_number', 'course__title', 'course__code') # 可搜索的字段
    list_filter = ('enrollment_date', 'course__department') # 可筛选的字段
    autocomplete_fields = ['student', 'course'] # 为 'student' 和 'course' 字段启用自动完成
    date_hierarchy = 'enrollment_date' # 在列表页顶部添加日期层级导航