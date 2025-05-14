from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied # Or redirect to a 'permission_denied' page

def student_required(view_func):
    """Decorator for views that checks that the user is a student."""
    decorated_view_func = user_passes_test(
        lambda u: u.is_authenticated and u.is_student,
        login_url='login', # Or your custom login URL
        # redirect_field_name=None # Or a custom permission denied page
    )(view_func)
    return decorated_view_func

def teacher_required(view_func):
    """Decorator for views that checks that the user is a teacher."""
    decorated_view_func = user_passes_test(
        lambda u: u.is_authenticated and u.is_teacher,
        login_url='login',
    )(view_func)
    return decorated_view_func

def staff_required(view_func): # For admin/staff roles
    """Decorator for views that checks that the user is a staff member."""
    decorated_view_func = user_passes_test(
        lambda u: u.is_authenticated and u.is_staff_member, # Check your User model property name
        login_url='login',
    )(view_func)
    return decorated_view_func