from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied

class StudentRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        # return self.request.user.is_authenticated and self.request.user.is_student
        if not self.request.user.is_authenticated:
            return False
        # return hasattr(self.request.user, 'is_staff') and self.request.user.is_staff
        return self.request.user.is_student # 使用 User 模型中的 @property

    
    # Handle permission denied:
    # def handle_no_permission(self):
    #     if self.raise_exception:
    #         raise PermissionDenied("You do not have permission to view this page.")
    #     return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())

class TeacherRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        # return self.request.user.is_authenticated and self.request.user.is_teacher
        if not self.request.user.is_authenticated:
            return False
        return self.request.user.is_teacher # 使用 User 模型中的 @property
class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        # Django 默认 User 模型使用 is_staff
        # 如果你的自定义 User 模型有 is_staff_member 属性/方法，请相应调整
        if not self.request.user.is_authenticated:
            return False
        # return self.request.user.is_staff or self.request.user.is_superuser
        return self.request.user.is_staff_member_role # 使用 User 模型中的 @property
        # 或者，如果你的用户模型是 is_staff_member:
        # return hasattr(self.request.user, 'is_staff_member') and self.request.user.is_staff_member