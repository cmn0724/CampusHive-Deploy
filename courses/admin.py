from django.contrib import admin
# Register your models here.
from django.utils.translation import gettext_lazy as _ # 导入翻译函数
from .models import Class, Course, Enrollment # 导入所有需要管理的模型
@admin.register(Class) # 注册 Class 模型
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'academic_year', 'advisor', 'get_student_count') # 列表页显示的字段
    search_fields = ('name', 'academic_year', 'advisor__username') # 可搜索的字段
    list_filter = ('academic_year',) # 可筛选的字段
    autocomplete_fields = ['advisor'] # 为 'advisor' (班主任) 字段启用自动完成
    def get_student_count(self, obj):
        # 假设 StudentProfile 中有 class_assigned 字段，并且 related_name='students'
        if hasattr(obj, 'students'): # 检查是否存在 'students' 反向关联
             return obj.students.count()
        return 0 # 如果没有，返回0
    get_student_count.short_description = _('Number of Students') # 列的显示名称
@admin.register(Course) # 注册 Course 模型
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'department', 'instructor', 'credits', 'get_enrollment_count') # 列表页显示的字段
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