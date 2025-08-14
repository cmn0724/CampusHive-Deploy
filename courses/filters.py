# courses/filters.py
import django_filters
from django import forms # 用于自定义表单部件的 class
from .models import Course
from users.models import Department # 假设 Department 模型在 users 应用中
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class CourseFilter(django_filters.FilterSet):
    # 为 title 字段添加一个模糊搜索 (忽略大小写)
    # 使用 forms.TextInput 并添加 Bootstrap class
    title = django_filters.CharFilter(
        lookup_expr='icontains', 
        label='Course Title Contains',
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'})
    )
    # 为 code 字段添加一个模糊搜索
    code = django_filters.CharFilter(
        lookup_expr='icontains', 
        label='Course Code Contains',
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'})
    )
    # department 字段，使用 ModelChoiceFilter 生成下拉选择框
    # 并添加 Bootstrap class
    department = django_filters.ModelChoiceFilter(
        queryset=Department.objects.all(), # 确保 Department 模型已定义且可访问
        label='Department',
        empty_label='All Departments', # 添加一个“全部”选项
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'})
    )
    # instructor 字段，同样使用 ModelChoiceFilter
    # 限制 queryset 只选择教师角色的用户
    instructor = django_filters.ModelChoiceFilter(
        queryset=User.objects.filter(role='teacher'), # 假设你的 User 模型有 'role' 字段，并且 'teacher' 是一个有效值
        label='Instructor',
        empty_label='All Instructors',
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'})
        # 你可能想自定义下拉框中教师的显示方式，
        # 默认使用 User 模型的 __str__ 方法。如果 __str__ 是 username，
        # 你可能想显示全名。这可以通过自定义 ModelChoiceFilter 的 to_field_name 或 label_from_instance 实现，
        # 但对于初学者，默认行为通常足够。
    )
    # 假设你想根据学分进行筛选 (例如，大于等于某个值)
    # credits_min = django_filters.NumberFilter(field_name='credits', lookup_expr='gte', label='Min. Credits')
    # credits_max = django_filters.NumberFilter(field_name='credits', lookup_expr='lte', label='Max. Credits')
    class Meta:
        model = Course
        # fields 列表指定了哪些模型的字段可以直接用于筛选。
        # 如果你在上面已经明确定义了某个字段的筛选器 (如 title, department, instructor)，
        # 它们会覆盖这里的默认行为。
        # 你可以只列出那些你想让 django-filter 自动生成简单筛选器的字段，
        # 或者像下面这样，明确指定查找表达式。
        fields = {
            'title': ['icontains'], # 等同于上面定义的 title = CharFilter(...)
            'code': ['icontains'],
            'department': ['exact'],  # 'exact' 会使用上面定义的 ModelChoiceFilter
            'instructor': ['exact'],  # 'exact' 会使用上面定义的 ModelChoiceFilter
            'credits': ['exact', 'gte', 'lte'], # 允许精确匹配、大于等于、小于等于学分
        }
        # 为了避免与上面手动定义的筛选器冲突或重复，并且让手动定义的更优先，
        # 你也可以将 Meta.fields 设置为一个空字典或列表，如果你所有筛选器都在类属性中定义了。
        # fields = {} # 如果所有筛选器都在类属性中详细定义了
    # 你也可以在 __init__ 中统一为所有表单字段添加 class，如果不想在每个字段定义中都写 widget
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for name, field in self.form.fields.items():
    #         if hasattr(field.widget, 'attrs'):
    #             current_class = field.widget.attrs.get('class', '')
    #             if isinstance(field.widget, forms.Select):
    #                 field.widget.attrs['class'] = f'{current_class} form-select form-select-sm'.strip()
    #             else:
    #                 field.widget.attrs['class'] = f'{current_class} form-control form-control-sm'.strip()
