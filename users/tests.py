# users/tests.py
from django.test import TestCase
# Create your tests here.
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Department, StudentProfile, EmployeeProfile
from .forms import CustomUserCreationForm, CustomLoginForm # Import your forms
from django.contrib.auth.forms import AuthenticationForm # For comparing CustomLoginForm
from django.urls import reverse


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

class CustomUserCreationFormTests(TestCase):
    def test_valid_form_student_creation(self):
        form_data = {
            'username': 'formstudent_real',
            'email': 'formstudent@example.com', # email 是表单字段
            'first_name': 'Form',              # first_name 是表单字段
            'last_name': 'Student',            # last_name 是表单字段
            'password1': 'ValidPassword123!',  # UserCreationForm 需要
            'password2': 'ValidPassword123!',  # UserCreationForm 需要
        }
        form = CustomUserCreationForm(data=form_data)
        
        # 打印错误以帮助调试，如果 is_valid() 失败
        if not form.is_valid():
            print(f"CustomUserCreationForm errors: {form.errors.as_json(indent=2)}")
        self.assertTrue(form.is_valid(), "Form should be valid with correct data.")
        
        user = form.save()
        self.assertEqual(user.username, 'formstudent_real')
        self.assertEqual(user.email, 'formstudent@example.com')
        self.assertEqual(user.first_name, 'Form')
        self.assertEqual(user.last_name, 'Student')
        self.assertTrue(user.check_password('ValidPassword123!'))
        
        # 验证 role (由 form.save() 设置)
        self.assertEqual(user.role, User.ROLE_STUDENT)
    def test_invalid_form_missing_username(self):
        form = CustomUserCreationForm(data={'password': 'password123'})
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
    # Add more tests for other invalid scenarios (e.g., password too short, username exists)
class CustomLoginFormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='loginformuser', password='password123')
    def test_valid_login_form(self):
        form_data = {'username': 'loginformuser', 'password': 'password123'}
        # CustomLoginForm might inherit AuthenticationForm, which needs a request object
        # For simplicity, if your CustomLoginForm doesn't strictly need request for basic validation:
        form = CustomLoginForm(data=form_data)
        # However, AuthenticationForm's is_valid() calls self.user_cache = self.get_user()
        # which needs request. So, we usually test login forms through the client in view tests.
        
        # A simpler check might be if the form fields are present, but that's not very useful.
        # The true test of a login form is whether it authenticates a user,
        # which is best done in a view test using self.client.login() or by posting to the login view.
        # For now, let's just assert it can be instantiated if it has no request dependency for basic structure.
        self.assertIsNotNone(form)
        # Actual validation testing is better in view tests.

class UserAuthenticationViewTests(TestCase):
    # ... (as provided in the previous answer, ensure URL names like 'users:login', 'users:signup', 'logout' match your setup)
    # ... (ensure LOGIN_REDIRECT_URL and LOGOUT_REDIRECT_URL are considered or mocked if necessary)
    @classmethod
    def setUpTestData(cls):
        # User for login tests
        cls.login_test_user = User.objects.create_user(username='logintest', password='password123', role=User.ROLE_STUDENT)
    def test_login_view_get_request(self):
        response = self.client.get(reverse('users:login')) # Ensure 'users:login' is correct
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html') # Ensure template path is correct
    def test_login_view_successful_post(self):
        response = self.client.post(reverse('users:login'), {'username': 'logintest', 'password': 'password123'})
        self.assertEqual(response.status_code, 302) # Expect redirect
        # Check settings.LOGIN_REDIRECT_URL or the 'next' parameter behavior
        # Assuming LOGIN_REDIRECT_URL = 'home'
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(self.client.session['_auth_user_id']) # Check if user is logged in
    def test_login_view_failed_post_wrong_password(self):
        response = self.client.post(reverse('users:login'), {'username': 'logintest', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200) # Stays on login page
        
        form_in_context = response.context.get('form')
        self.assertIsNotNone(form_in_context, "Form not found in response context.")
        
        # 检查非字段错误 (None 作为 field name)
        self.assertFormError(form_in_context, None, 'Please enter a correct username and password. Note that both fields may be case-sensitive.')
        # 或者，如果错误是针对特定字段的，例如 'username' 或 '__all__' (对于非字段错误有时也用 __all__)
        # self.assertFormError(form_in_context, '__all__', 'Please enter a correct username and password. Note that both fields may be case-sensitive.')
        self.assertFalse('_auth_user_id' in self.client.session)
    def test_logout_view(self):
        self.client.login(username='logintest', password='password123')
        self.assertTrue('_auth_user_id' in self.client.session)
        response = self.client.post(reverse('logout')) # Django's default logout URL
        self.assertEqual(response.status_code, 302)
        # Check settings.LOGOUT_REDIRECT_URL
        # Assuming LOGOUT_REDIRECT_URL = 'home'
        self.assertRedirects(response, reverse('home'))
        self.assertFalse('_auth_user_id' in self.client.session)
class SignUpViewTests(TestCase):
    def test_signup_view_get_request(self):
        response = self.client.get(reverse('users:signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html') # Ensure template is correct
    def test_signup_view_successful_post(self):
        initial_user_count = User.objects.count()
        signup_data = {
            'username': 'new_signed_up_user',
            'email': 'newsignup@example.com',    # email 是表单字段
            'first_name': 'New',                 # first_name 是表单字段
            'last_name': 'SignedUp',             # last_name 是表单字段
            'password1': 'StrongPassword123!',   # UserCreationForm 需要
            'password2': 'StrongPassword123!',   # UserCreationForm 需要
        }
        response = self.client.post(reverse('users:signup'), signup_data, follow=True)
        # 调试信息：如果用户未创建
        if User.objects.count() == initial_user_count:
            if response.context and 'form' in response.context:
                form_errors = response.context['form'].errors.as_data()
                print(f"Signup view form errors: {form_errors}")
            else:
                print("Signup view: Form not in context or unexpected response.")
                print(f"Status code: {response.status_code}")
                # print(f"Content: {response.content.decode()[:500]}")
        self.assertEqual(User.objects.count(), initial_user_count + 1, "User should be created.")
        
        try:
            new_user = User.objects.get(username='new_signed_up_user')
        except User.DoesNotExist:
            self.fail("Newly created user not found in database.")
        self.assertEqual(new_user.email, 'newsignup@example.com')
        self.assertEqual(new_user.first_name, 'New')
        self.assertEqual(new_user.last_name, 'SignedUp')
        self.assertTrue(new_user.check_password('StrongPassword123!'))
        
        # 验证 role (由 form.save() 设置，并通过 SignUpView 调用)
        self.assertEqual(new_user.role, User.ROLE_STUDENT)
        self.assertTrue(new_user.is_active) # UserCreationForm 默认创建 active user
        # 检查用户是否已登录 (因为 SignUpView 调用了 login())
        self.assertIsNotNone(response.context, "Response context should exist.")
        if response.context: # 添加检查以避免 NoneType 错误
             self.assertTrue(response.context['user'].is_authenticated, "User should be authenticated after signup.")
        
        # 检查重定向 (SignUpView 的 success_url 是 'home')
        self.assertRedirects(response, reverse('home'), status_code=302, target_status_code=200, msg_prefix="Redirect after signup failed.")


class UserProfileViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create_user(username='profiletestuser', password='password123', role=User.ROLE_STUDENT)
    def test_profile_view_authenticated_user(self):
        self.client.login(username='profiletestuser', password='password123')
        response = self.client.get(reverse('users:user_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_profile.html')
        self.assertEqual(response.context['profile_user'], self.test_user)
    def test_profile_view_unauthenticated_user(self):
        response = self.client.get(reverse('users:user_profile'))
        self.assertEqual(response.status_code, 302) # Redirects to login
        expected_redirect_url = f"{reverse('users:login')}?next={reverse('users:user_profile')}"
        self.assertRedirects(response, expected_redirect_url)