from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name') # Role will be set in the view

    def __init__(self, *args, **kwargs): # 添加 __init__ 来修改 widgets
        super().__init__(*args, **kwargs)
        # 为注册表单的字段添加 Bootstrap class
        for field_name, field in self.fields.items():
            # 确保字段存在 widget 属性
            if hasattr(field.widget, 'attrs'):
                # 根据字段类型选择不同的 class，或统一添加
                field.widget.attrs.update({'class': 'form-control mb-2', 'placeholder': field.label})
                if field_name == 'email': # 给 email 字段特定的 placeholder
                    field.widget.attrs['placeholder'] = 'Enter your email'
                # ... 可以为其他字段添加特定 placeholder

    def save(self, commit=True):
        user = super().save(commit=False)
        if hasattr(User, 'ROLE_STUDENT'):
            user.role = User.ROLE_STUDENT # Default role for new sign-ups
        else:
            # 如果没有 ROLE_STUDENT，你可能需要设置一个默认值或在视图中处理
            # 或者确保你的 User 模型中有 'role' 字段并正确配置了 choices
            print("Warning: User.ROLE_STUDENT not found, default role not set for new user.")
        
        # You might want to add email uniqueness check here if not handled by model's unique=True
        if commit:
            user.save()
        return user
    
class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 为登录表单的 username 字段添加 Bootstrap class 和 placeholder
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control mb-2', 'placeholder': 'Username or Email'} # 假设用户名或邮箱都可以登录
        )
        # 为登录表单的 password 字段添加 Bootstrap class 和 placeholder
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Password'} # mb-3 给密码框下面多一点空间
        )