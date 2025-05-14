from django.db import models
# Create your models here.
from django.conf import settings # 用于导入 AUTH_USER_MODEL
from django.utils.translation import gettext_lazy as _

class Class(models.Model): # 代表一个学生群体，例如“高一(1)班”
    name = models.CharField(_('Class Name'), max_length=100, unique=True) # 班级名称
    # 考虑链接到一个 'GradeLevel' (年级) 模型，或者只是一个 CharField
    academic_year = models.CharField(_('Academic Year'), max_length=9, help_text=_('e.g., 2024/2025')) # 学年，例如 2024/2025
    advisor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'teacher'}, # 假设 User 模型有 'role' 字段
        related_name='advised_classes',
        verbose_name=_('Class Advisor') # 班主任
    )
    # 将 StudentProfile 链接到 Class
    # students = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='classes_enrolled_in', limit_choices_to={'role':'student'}, blank=True)
    # 如果一个学生只属于一个班级，那么在 StudentProfile 中使用 ForeignKey 会更好

    def __str__(self):
        # return self.name
        return f"{self.name} ({self.academic_year})"

    class Meta:
        verbose_name = _('Class') # 班级
        verbose_name_plural = _('Classes') # 班级 (复数)

# 在 users/models.py 的 StudentProfile 中添加:
# class_assigned = models.ForeignKey('courses.Class', on_delete=models.SET_NULL, null=True, blank=True, related_name='students', verbose_name=_('Assigned Class')) # 所属班级

class Course(models.Model):
    code = models.CharField(_('Course Code'), max_length=20, unique=True) # 课程代码
    title = models.CharField(_('Course Title'), max_length=200) # 课程标题
    description = models.TextField(_('Description'), blank=True) # 描述
    credits = models.PositiveSmallIntegerField(_('Credits'), default=0) # 学分
    department = models.ForeignKey('users.Department', on_delete=models.SET_NULL, null=True, blank=True, related_name='courses') # 开课院系
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'teacher'},
        related_name='taught_courses',
        verbose_name=_('Instructor') #授课教师
    )

    def __str__(self):
        return f"{self.code} - {self.title}"

class Enrollment(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, # 或者 StudentProfile 如果你更喜欢直接链接
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'student'},
        related_name='enrollments'
    ) # 学生
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments') # 课程
    enrollment_date = models.DateField(auto_now_add=True) # 选课日期
    grade = models.CharField(max_length=5, blank=True, null=True) # 简单的成绩字段，或者 ForeignKey 到一个 Grade 模型

    class Meta:
        unique_together = ('student', 'course') # 一个学生只能选同一门课一次
        verbose_name = _('Enrollment') # 选课记录
        verbose_name_plural = _('Enrollments') # 选课记录 (复数)

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.title}" # 某某学生选了某某课程

# 其他模型: Grade (成绩), CourseMaterial (课程资料), Assignment (作业), Submission (提交记录) (根据你的 ERD)
# 目前，专注于主要的结构性模型。