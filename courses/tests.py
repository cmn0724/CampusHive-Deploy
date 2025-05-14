from django.test import TestCase
# Create your tests here.
from django.contrib.auth import get_user_model
from django.utils import timezone
from users.models import Department, EmployeeProfile # 假设教师和部门来自 users 应用
from .models import Class, Course, Enrollment
User = get_user_model()
class ClassModelTests(TestCase):
    """
    测试 Class (班级) 模型
    """
    @classmethod
    def setUpTestData(cls):
        # 准备一个教师用户作为班主任
        cls.advisor_user = User.objects.create_user(
            username='classadvisor',
            password='password',
            role=User.ROLE_TEACHER # 确保 User 模型中有 ROLE_TEACHER
        )
        # 也可以选择性地创建 EmployeeProfile 如果 Class 模型的 advisor 字段直接关联 User
        # 如果 advisor 关联 EmployeeProfile, 则需要创建 EmployeeProfile 实例
        # EmployeeProfile.objects.create(user=cls.advisor_user, employee_id_number='T001')
        cls.class_instance = Class.objects.create(
            name='Grade 10 - Section A',
            academic_year='2023-2024',
            advisor=cls.advisor_user # 假设 advisor 直接关联 User 模型
        )
    def test_class_creation(self):
        # 测试班级的成功创建
        self.assertEqual(self.class_instance.name, 'Grade 10 - Section A')
        self.assertEqual(self.class_instance.academic_year, '2023-2024')
        self.assertEqual(self.class_instance.advisor, self.advisor_user)
        self.assertIsNotNone(self.class_instance.id)
    def test_class_str_representation(self):
        # 测试 Class 模型的 __str__ 方法
        # 假设 __str__ 返回 "班级名称 (学年)"
        expected_str = f"{self.class_instance.name} ({self.class_instance.academic_year})"
        self.assertEqual(str(self.class_instance), expected_str)

class CourseModelTests(TestCase):
    """
    测试 Course (课程) 模型
    """
    @classmethod
    def setUpTestData(cls):
        cls.department = Department.objects.create(name='Mathematics')
        cls.instructor_user = User.objects.create_user(
            username='courseinstructor',
            password='password',
            role=User.ROLE_TEACHER
        )
        # 假设 Course 模型的 instructor 字段直接关联 User
        # 如果关联 EmployeeProfile, 则需要创建 EmployeeProfile 实例
        cls.course = Course.objects.create(
            code='MATH101',
            title='Introduction to Algebra',
            description='Fundamental concepts of algebra.',
            department=cls.department,
            instructor=cls.instructor_user,
            credits=3
        )
    def test_course_creation(self):
        # 测试课程的成功创建
        self.assertEqual(self.course.code, 'MATH101')
        self.assertEqual(self.course.title, 'Introduction to Algebra')
        self.assertEqual(self.course.department, self.department)
        self.assertEqual(self.course.instructor, self.instructor_user)
        self.assertEqual(self.course.credits, 3)
    def test_course_str_representation(self):
        # 测试 Course 模型的 __str__ 方法
        # 假设 __str__ 返回 "课程代码 - 课程标题"
        expected_str = f"{self.course.code} - {self.course.title}"
        # expected_str = f"{self.class_instance.name}"
        self.assertEqual(str(self.course), expected_str)
    def test_course_default_credits(self):
        # 如果 credits 字段有默认值，可以测试它
        # 假设 credits 默认值为 0 (如果没有在模型中设置 default，此测试可能失败或行为不同)
        # course_no_credits = Course.objects.create(
        #     code='PHYS000',
        #     title='Conceptual Physics',
        #     department=self.department,
        #     instructor=self.instructor_user
        # )
        # self.assertEqual(course_no_credits.credits, 0) # 仅当模型中定义了 default=0
        pass # 如果没有明确的默认值，可以跳过或根据实际情况调整

class EnrollmentModelTests(TestCase):
    """
    测试 Enrollment (选课记录) 模型
    """
    @classmethod
    def setUpTestData(cls):
        cls.student_user = User.objects.create_user(
            username='enrollstudent',
            password='password',
            role=User.ROLE_STUDENT
        )
        # 假设 StudentProfile 不是选课的直接关联方，而是 User
        # 如果 Enrollment.student 指向 StudentProfile, 则需要创建 StudentProfile
        department = Department.objects.create(name='Computer Science Dept For Enrollment')
        instructor = User.objects.create_user(username='enrollinstructor', password='pwd', role=User.ROLE_TEACHER)
        cls.course = Course.objects.create(
            code='CS101',
            title='Intro to Programming',
            department=department,
            instructor=instructor,
            credits=4
        )
        cls.enrollment = Enrollment.objects.create(
            student=cls.student_user, # 假设 Enrollment.student 直接关联 User
            course=cls.course
            # enrollment_date 假设有 default=timezone.now 或 auto_now_add=True
            # grade 假设可以为 null 或有默认值
        )
    def test_enrollment_creation(self):
        # 测试选课记录的成功创建
        self.assertEqual(self.enrollment.student, self.student_user)
        self.assertEqual(self.enrollment.course, self.course)
        self.assertIsNotNone(self.enrollment.enrollment_date)
        # 检查 grade 的初始状态 (例如，如果允许 null=True, blank=True)
        self.assertIsNone(self.enrollment.grade) # 假设 grade 初始为 None
    def test_enrollment_str_representation(self):
        # 测试 Enrollment 模型的 __str__ 方法
        # 假设 __str__ 返回 "学生用户名 enrolled in 课程标题"
        expected_str = f"{self.student_user.username} enrolled in {self.course.title}"
        self.assertEqual(str(self.enrollment), expected_str)
    def test_enrollment_grade_update(self):
        # 测试成绩更新
        self.enrollment.grade = 'A'
        self.enrollment.save()
        updated_enrollment = Enrollment.objects.get(id=self.enrollment.id)
        self.assertEqual(updated_enrollment.grade, 'A')