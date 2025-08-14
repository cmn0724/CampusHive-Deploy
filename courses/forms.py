# courses/forms.py
from django import forms
from .models import Course
from users.models import User #, Department # Assuming Department is in users app, adjust if different
from .models import Enrollment
from django.forms import inlineformset_factory
from .models import CourseMaterial
from .models import Assignment
from .models import Submission

class CourseCreationForm(forms.ModelForm):
    # Limit instructor choices to users with the 'teacher' role
    instructor = forms.ModelChoiceField(
        queryset=User.objects.filter(role=User.ROLE_TEACHER),
        required=False, # Or True, depending on your requirements
        label="Instructor"
    )
    # If Department is in a different app, ensure it's imported correctly.
    # department = forms.ModelChoiceField(queryset=Department.objects.all(), required=False)
    class Meta:
        model = Course
        fields = ['code', 
                  'title', 
                  'description', 
                  'credits', 
                  'department', 
                  'instructor',
                  'schedule_information',
                  ]
        # You can customize widgets here if needed, e.g., for description:
        # widgets = {
        #     'description': forms.Textarea(attrs={'rows': 3}),
        # }
    def __init__(self, *args, **kwargs):
        self.request_user = kwargs.pop('request_user', None) # Pass the request.user to the form
        super().__init__(*args, **kwargs)
        # If the form is for a teacher creating their own course,
        # you might want to default the instructor field.
        if self.request_user and self.request_user.is_teacher:
            # If instructor field should be current teacher and non-editable:
            # self.fields['instructor'].initial = self.request_user
            # self.fields['instructor'].disabled = True
            # Or, if they can assign other teachers, keep it as is.
            pass

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['code', 'title', 'description', 'credits', 'department'] # 列出你希望在表单中出现的字段
        # 'teacher' 字段会在 views.py 的 form_valid 中自动设置，所以通常不在这里包含

class EnrollmentGradeForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['student', 'grade']
        # Optional: Add widget if you want a dropdown for grades
        # widgets = {
        #     'grade': forms.Select(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('F', 'F'), ('P','Pass'), ('NP', 'Not Pass')])
        # }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 确保 'student' 字段存在 (inlineformset_factory 会添加它)
        if 'student' in self.fields:
            self.fields['student'].disabled = True # <--- 将 student 字段设为禁用
    
# For inline formset (batch grading)
EnrollmentGradeFormSet = inlineformset_factory(
    Course, # Parent model
    Enrollment, # Child model
    form=EnrollmentGradeForm,
    extra=0, # Don't show extra empty forms
    can_delete=False,
    fields=('student', 'grade'), # Fields to show in the formset
    # readonly_fields=('student',) # Make student field read-only in the form
)

# If Enrollment.student is a ForeignKey to User, not StudentProfile:
# We might need a custom formset or a different approach if 'student' is not directly editable.
# A simpler approach for now: iterate enrollments and create individual forms.


class CourseMaterialForm(forms.ModelForm):
    class Meta:
        model = CourseMaterial
        fields = ['title', 'file', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class AssignmentForm(forms.ModelForm):
    due_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        input_formats=['%Y-%m-%dT%H:%M']
    )
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'due_date', 'assignment_file']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }
    
    # 你可以添加一个 __init__ 方法来自定义表单，例如，如果需要基于 course 进行一些初始化
    # def __init__(self, *args, **kwargs):
    #     self.course = kwargs.pop('course', None) # 如果视图传递了 course
    #     super().__init__(*args, **kwargs)
    #     if self.course:
    #         # 基于 course 做一些事情，例如设置某些字段的初始值或 queryset
    #         pass

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['submitted_file']

class GradeSubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['grade', 'feedback']
        widgets = {
            'feedback': forms.Textarea(attrs={'rows': 4}),
        }