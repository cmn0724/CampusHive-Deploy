# users/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _ # Django的翻译函数
from courses.models import Class

class UserManager(BaseUserManager):
    """自定义用户管理器"""
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        # 确保 username 字段有值，因为 AbstractUser 需要它
        # 如果你没有传入 username，可以从 email 生成一个
        if 'username' not in extra_fields:
            extra_fields['username'] = email.split('@')[0]
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
 
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', User.ROLE_ADMIN)
 
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        
        # 确保 username 字段被设置
        if 'username' not in extra_fields:
            extra_fields['username'] = email.split('@')[0]
            
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    # 定义角色常量
    ROLE_STUDENT = 'student'
    ROLE_TEACHER = 'teacher'
    ROLE_STAFF_MEMBER = 'staff' 
    ROLE_ADMIN = 'admin'
    
    ROLE_CHOICES = [
        (ROLE_STUDENT, _('Student')), # 学生
        (ROLE_TEACHER, _('Teacher')), # 教师
        (ROLE_STAFF_MEMBER, _('Staff')),   # 职员
        (ROLE_ADMIN, _('Admin'))
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

    objects = UserManager()

    def save(self, *args, **kwargs):
        # 根据 role 设置 AbstractUser 的 is_staff 字段
        # if self.role in [User.ROLE_ADMIN, User.ROLE_STAFF_MEMBER, User.ROLE_TEACHER]: # 假设 Admin, Staff, Teacher 可以访问 admin
        #     self.is_staff = True
        # else: # 例如 Student
        #     self.is_staff = False

        if self.role == self.ROLE_ADMIN:
            self.is_staff = True
            self.is_superuser = True
        elif self.role in [self.ROLE_STAFF_MEMBER, self.ROLE_TEACHER]:
            self.is_staff = True
            self.is_superuser = False # 确保非Admin的员工不是超级用户
        else: # Student
            self.is_staff = False
            self.is_superuser = False
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.username

    # 添加辅助方法
    @property
    def is_student(self):
        return self.role == self.ROLE_STUDENT
    
    @property
    def is_teacher(self):
        return self.role == self.ROLE_TEACHER
    
    @property
    def is_staff_member_role(self): 
        return self.role == self.ROLE_STAFF_MEMBER
    
    @property
    def is_admin(self): # 可以添加一个明确的 is_admin 属性
        return self.role == self.ROLE_ADMIN

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
    
    assigned_class = models.ForeignKey(
        Class, # 指向 courses.Class 模型
        on_delete=models.SET_NULL, # 当班级被删除时，学生的班级字段设为 NULL，而不是删除学生
        null=True, # 允许为空，表示学生可能暂未被分配班级
        blank=True, # 在表单中允许为空
        related_name='students' # 定义反向关系名称，以便从 Class 实例访问其所有学生 (e.g., class_instance.students.all())
    )
    
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