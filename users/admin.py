# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin # 重命名以避免冲突
from django.utils.translation import gettext_lazy as _
from .models import User, Department, StudentProfile, EmployeeProfile

# 1. 定义 Inline 类 (必须在使用它们之前定义)
class StudentProfileInline(admin.StackedInline): # 或者 admin.TabularInline
    model = StudentProfile
    can_delete = False # 通常不希望通过 User 页面删除 Profile
    verbose_name_plural = _('Student Profile')
    fk_name = 'user' # 确保 StudentProfile 中指向 User 的外键名为 'user'
    # fields = ('student_id_number', 'enrollment_date', 'class_assigned') # 你想在inline中显示的字段
    # readonly_fields = (...)
    # extra = 1 # 默认显示几个空的inline表单
class EmployeeProfileInline(admin.StackedInline):
    model = EmployeeProfile
    can_delete = False
    verbose_name_plural = _('Employee Profile')
    fk_name = 'user' # 确保 EmployeeProfile 中指向 User 的外键名为 'user'
    # fields = ('employee_id_number', 'department', 'date_joined') # 你想在inline中显示的字段
    # readonly_fields = (...)
    # extra = 1

@admin.register(User) # 使用装饰器注册 User 模型
class UserAdmin(BaseUserAdmin):
    # 将 'role' 添加到 list_display, fieldsets 等
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'role') # 列表页显示的字段
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active') # 列表页右侧的过滤器
    search_fields = ('username', 'first_name', 'last_name', 'email') # 列表页顶部的搜索框可搜索的字段
    ordering = ('username',) # 默认排序字段
    fieldsets = BaseUserAdmin.fieldsets + (
        (_('Role Information'), {'fields': ('role',)}), # 角色信息
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (_('Role Information'), {'fields': ('role',)}), # 角色信息
    )

    # 将 Profile Inlines 添加到 UserAdmin
    inlines = [StudentProfileInline, EmployeeProfileInline]
    

@admin.register(Department) # 注册 Department 模型
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'head', 'get_employee_count') # 列表页显示的字段
    search_fields = ('name', 'head__username') # 可搜索的字段
    autocomplete_fields = ['head'] # 为 'head' 字段启用自动完成搜索框，方便选择用户
    def get_employee_count(self, obj):
        # 自定义方法，用于在列表页显示部门员工数量
        if hasattr(obj, 'employees'): # 更安全的检查
            return obj.employees.count()
        elif hasattr(obj, 'employeeprofile_set'):
            return obj.employeeprofile_set.count()
        return 0
    get_employee_count.short_description = _('Number of Employees') # 列的显示名称

@admin.register(StudentProfile) # 注册 StudentProfile 模型
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'student_id_number', 'enrollment_date', 'get_assigned_class_name') # 列表页显示的字段
    search_fields = ('user__username', 'student_id_number') # 可搜索的字段
    list_filter = ('enrollment_date',) # 可筛选的字段
    autocomplete_fields = ['user'] # 为 'user' 字段启用自动完成
    # 如果 StudentProfile 中有 class_assigned 字段:
    # autocomplete_fields = ['user', 'class_assigned']
    
    def get_assigned_class_name(self, obj):
        # 假设 StudentProfile 中有一个名为 class_assigned 的 ForeignKey 指向 courses.Class 模型
        if hasattr(obj, 'class_assigned') and obj.class_assigned:
            return obj.class_assigned.name
        return _("Not Assigned")
    get_assigned_class_name.short_description = _('Assigned Class') # 列的显示名称

@admin.register(EmployeeProfile) # 注册 EmployeeProfile 模型
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'employee_id_number', 'department', 'date_joined') # 列表页显示的字段
    search_fields = ('user__username', 'employee_id_number', 'department__name') # 可搜索的字段
    list_filter = ('department', 'date_joined') # 可筛选的字段
    autocomplete_fields = ['user', 'department'] # 为 'user' 和 'department' 字段启用自动完成