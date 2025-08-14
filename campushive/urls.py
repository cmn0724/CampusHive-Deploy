# campushive/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # Django's built-in authentication URLs (login, logout, password reset, etc.)
    # 通常 'accounts/' 前缀用于这些内置视图
    # path('accounts/', include('users.urls')), # 移除了 namespace，因为它会从 users.urls 的 app_name 获取
    path('accounts/', include('django.contrib.auth.urls')),
    
    # path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('users.urls')),
    # Your custom user-related URLs (like signup, dashboard)
    # 可以考虑使用不同的前缀，或者如果希望它们也在 'accounts/' 下，
    # 则需要确保 users.urls 中的路径不会与 django.contrib.auth.urls 中的路径冲突。
    # 如果 users.urls 中的路径是 'signup/', 'dashboard/student/'，
    # 那么 'accounts/signup/' 和 'accounts/dashboard/student/' 是可以的。
    
    # App URLs
    path('courses/', include('courses.urls')), # 移除了 namespace，因为它会从 courses.urls 的 app_name 获取
    path('equipment/', include('equipment.urls')),
    # Home page
    path('', TemplateView.as_view(template_name="home.html"), name='home'),
]

# Media files serving in development
if settings.DEBUG: # Important: only in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)