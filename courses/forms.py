# courses/forms.py
from django import forms
from .models import Course
from users.models import User #, Department # Assuming Department is in users app, adjust if different

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
        fields = ['code', 'title', 'description', 'credits', 'department', 'instructor']
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