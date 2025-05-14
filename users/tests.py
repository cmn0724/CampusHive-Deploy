# users/tests.py
from django.test import TestCase
# Create your tests here.
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Department, StudentProfile, EmployeeProfile


User = get_user_model() # 获取当前项目使用的 User 模型

class UserModelTests(TestCase):
    """
    测试 User 模型
    """
    def test_create_user(self):
        # 测试普通用户的创建
        user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123',
            first_name='Test',
            last_name='User',
            role=User.ROLE_STUDENT # 假设 User 模型中有 ROLE_STUDENT 常量
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertTrue(user.check_password('password123'))
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')
        self.assertEqual(user.role, User.ROLE_STUDENT)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active) # create_user 默认 is_active=True
    
    def test_create_superuser(self):
        # 测试超级用户的创建
        admin_user = User.objects.create_superuser(
            username='adminuser',
            email='admin@example.com',
            password='adminpassword123',
            role=User.ROLE_ADMIN # 超级用户通常也是员工
        )
        self.assertEqual(admin_user.username, 'adminuser')
        self.assertEqual(admin_user.email, 'admin@example.com')
        self.assertTrue(admin_user.check_password('adminpassword123'))
        self.assertEqual(admin_user.role, User.ROLE_ADMIN)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_active)
    
    def test_user_str_representation(self):
        # 测试 User 模型的 __str__ 方法
        user = User.objects.create_user(username='struser', password='password')
        self.assertEqual(str(user), 'struser')

class DepartmentModelTests(TestCase):
    """
    测试 Department 模型
    """
    @classmethod
    def setUpTestData(cls):
        # setUpTestData 用于设置只需执行一次的、跨多个测试方法共享的数据
        cls.head_user = User.objects.create_user(username='depthead', password='password')
        cls.department = Department.objects.create(name='Computer Science', head=cls.head_user)
    
    def test_department_creation(self):
        # 测试部门的成功创建
        self.assertEqual(self.department.name, 'Computer Science')
        self.assertEqual(self.department.head, self.head_user)
        self.assertIsNotNone(self.department.id) # 确保已保存并获得 ID
    
    def test_department_str_representation(self):
        # 测试 Department 模型的 __str__ 方法
        self.assertEqual(str(self.department), 'Computer Science')

class StudentProfileModelTests(TestCase):
    """
    测试 StudentProfile 模型
    """
    @classmethod
    def setUpTestData(cls):
        cls.student_user = User.objects.create_user(
            username='student1',
            password='password',
            role=User.ROLE_STUDENT
        )
        cls.profile = StudentProfile.objects.create(
            user=cls.student_user,
            student_id_number='S12345',
            enrollment_date=timezone.now().date()
        )
    
    def test_student_profile_creation(self):
        # 测试学生档案的创建
        self.assertEqual(self.profile.user, self.student_user)
        self.assertEqual(self.profile.student_id_number, 'S12345')
        self.assertIsNotNone(self.profile.enrollment_date) # 假设有默认值或 auto_now_add
    
    def test_student_profile_str_representation(self):
        # 测试 StudentProfile 模型的 __str__ 方法
        # 假设 __str__ 返回 "用户名 - Student Profile"
        expected_str = f"{self.student_user.username} - Student Profile"
        self.assertEqual(str(self.profile), expected_str)

class EmployeeProfileModelTests(TestCase):
    """
    测试 EmployeeProfile 模型
    """
    @classmethod
    def setUpTestData(cls):
        cls.teacher_user = User.objects.create_user(
            username='teacher1',
            password='password',
            role=User.ROLE_TEACHER # 确保 User 模型中有 ROLE_TEACHER
        )
        cls.department = Department.objects.create(name='Physics')
        cls.profile = EmployeeProfile.objects.create(
            user=cls.teacher_user,
            employee_id_number='E98765',
            department=cls.department,
            date_joined=timezone.now().date() 
        )
    
    def test_employee_profile_creation(self):
        # 测试员工档案的创建
        self.assertEqual(self.profile.user, self.teacher_user)
        self.assertEqual(self.profile.employee_id_number, 'E98765')
        self.assertEqual(self.profile.department, self.department)
        self.assertIsNotNone(self.profile.date_joined)
    
    def test_employee_profile_str_representation(self):
        # 测试 EmployeeProfile 模型的 __str__ 方法
        # 假设 __str__ 返回 "用户名 - Employee Profile"
        expected_str = f"{self.teacher_user.username} - Employee Profile"
        self.assertEqual(str(self.profile), expected_str)
    
    def test_employee_profile_default_department(self):
        # 如果 department 字段允许 null=True, blank=True，可以测试不指定部门的情况
        staff_user = User.objects.create_user(username='staff1', password='password', role=User.ROLE_STAFF_MEMBER)
        profile_no_dept = EmployeeProfile.objects.create(
            user=staff_user,
            employee_id_number='E00001'
        )
        self.assertIsNone(profile_no_dept.department) # 假设 department 可以为 None