from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _ # Django的翻译函数

class User(AbstractUser):
    # 定义角色常量
    ROLE_STUDENT = 'student'
    ROLE_TEACHER = 'teacher'
    ROLE_STAFF = 'staff' # 或者你喜欢用 'admin'
    ROLE_CHOICES = [
        (ROLE_STUDENT, _('Student')), # 学生
        (ROLE_TEACHER, _('Teacher')), # 教师
        (ROLE_STAFF, _('Staff')),   # 职员
    ]
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=ROLE_STUDENT, # 或者一个更合适的默认值
        verbose_name=_('Role') # 角色
    )

    # 添加你确定的其他通用字段，例如：
    phone_number = models.CharField(_('Phone Number'), max_length=20, blank=True, null=True) # 电话号码
    # profile_picture = models.ImageField(_('Profile Picture'), upload_to='profile_pics/', blank=True, null=True) # 头像
    date_of_birth = models.DateField(_('Date of Birth'), blank=True, null=True) # 出生日期，可能放在StudentProfile中更好

    def __str__(self):
        return self.username

    # 你之后可能会在这里添加辅助方法，例如：
    # @property
    # def is_student(self):
    #     return self.role == self.ROLE_STUDENT
    #
    # @property
    # def is_teacher(self):
    #     return self.role == self.ROLE_TEACHER
    #
    # @property
    # def is_staff(self):
    #     return self.role == self.ROLE_STAFF

class Department(models.Model):
    name = models.CharField(_('Department Name'), max_length=100, unique=True) # 部门名称
    description = models.TextField(_('Description'), blank=True, null=True) # 描述
    head = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': User.ROLE_TEACHER}, # 或者 staff (职员)
        related_name='headed_department',
        verbose_name=_('Department Head') # 部门主管
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Department') # 部门
        verbose_name_plural = _('Departments') # 部门 (复数)

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='student_profile') # 关联用户
    student_id_number = models.CharField(_('Student ID'), max_length=20, unique=True) # 学号
    # class_assigned = models.ForeignKey('courses.Class', ...) # 我们将在 courses 应用中定义 Class
    enrollment_date = models.DateField(_('Enrollment Date')) # 入学日期
    # 添加 ERD 中其他学生特有的字段

    def __str__(self):
        # return f"{self.user.username} - Student" #某某 - 学生
        return f"{self.user.username} - Student Profile"

    class Meta:
        verbose_name = _('Student Profile') # 学生资料
        verbose_name_plural = _('Student Profiles') # 学生资料 (复数)

class EmployeeProfile(models.Model): # 适用于教师和其他职员
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='employee_profile') # 关联用户
    employee_id_number = models.CharField(_('Employee ID'), max_length=20, unique=True) # 工号
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='employees') # 所属部门
    #date_joined = models.DateField(_('Date Joined')) # 入职日期
    date_joined = models.DateField(default=timezone.now)
    # 添加其他员工特有的字段

    def __str__(self):
        # return f"{self.user.username} - Employee" # 某某 - 员工
        return f"{self.user.username} - Employee Profile"

    class Meta:
        verbose_name = _('Employee Profile') # 员工资料
        verbose_name_plural = _('Employee Profiles') # 员工资料 (复数)