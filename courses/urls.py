# courses/urls.py
from django.urls import path
from .views import CourseListView , CourseCreateViewActual
from .views import CourseDetailView
from .views import CourseUpdateView
from .views import CourseDeleteView
from .views import EnrollCourseView, DropCourseView
from .views import GradeEnrollmentsView
from .views import UploadMaterialView, DeleteMaterialView
from .views import CreateAssignmentViewActual, UpdateAssignmentView, DeleteAssignmentView
from .views import AssignmentDetailView
from .views import SubmitAssignmentView
from .views import GradeSubmissionView
from .views import TeacherCourseManagementView
# from . import views

app_name = 'courses'

urlpatterns = [
    # path('', CourseListView.as_view(), name='course_list'),
    # path('create/', CourseCreateView.as_view(), name='course_create'), 
    # path('<int:pk>/', CourseDetailView.as_view(), name='course_detail'),

    path('', CourseListView.as_view(), name='course_list'),
    path('create/', CourseCreateViewActual.as_view(), name='course_create'),
    path('<int:pk>/', CourseDetailView.as_view(), name='course_detail'),
    path('<int:pk>/update/', CourseUpdateView.as_view(), name='course_update'),
    path('<int:pk>/delete/', CourseDeleteView.as_view(), name='course_delete'),
    path('<int:course_id>/enroll/', EnrollCourseView.as_view(), name='enroll_course'),
    path('enrollment/<int:enrollment_id>/drop/', DropCourseView.as_view(), name='drop_course'),
    path('<int:course_id>/grades/', GradeEnrollmentsView.as_view(), name='grade_enrollments'),
    path('<int:course_id>/materials/upload/', UploadMaterialView.as_view(), name='upload_material'),
    path('materials/<int:pk>/delete/', DeleteMaterialView.as_view(), name='delete_material'), # pk here is material's pk
    path('<int:course_id>/assignments/create/', CreateAssignmentViewActual.as_view(), name='create_assignment'),
    path('assignments/<int:pk>/update/', UpdateAssignmentView.as_view(), name='update_assignment'), # pk is assignment's pk
    path('assignments/<int:pk>/delete/', DeleteAssignmentView.as_view(), name='delete_assignment'),
    path('assignments/<int:assignment_id>/', AssignmentDetailView.as_view(), name='assignment_detail'),
    path('assignments/<int:assignment_id>/submit/', SubmitAssignmentView.as_view(), name='submit_assignment'),
    path('submissions/<int:submission_id>/grade/', GradeSubmissionView.as_view(), name='grade_submission'),
    path('my-teaching/', TeacherCourseManagementView.as_view(), name='manage_teacher_courses'),
]
