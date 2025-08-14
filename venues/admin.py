# venues/admin.py
from django.contrib import admin
from .models import Venue, VenueBooking

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name',) # 场所列表页显示名称
    search_fields = ('name',) # 允许按名称搜索
    # list_display = ('venue', 'booking_period_display', 'booked_by_name', 'created_at') # 使用新属性
    # # ...
    # fieldsets = (
    #     (None, {
    #         'fields': ('venue', ('start_time', 'end_time'), 'booked_by_name') # 将 start_time 和 end_time 放在一行
    #     }),
    # )
    # # Django Admin 会为 DateTimeField 自动添加一个简单的 JS 日期和时间选择器
@admin.register(VenueBooking)
class VenueBookingAdmin(admin.ModelAdmin):
    # list_display = ('venue', 'booking_period', 'booked_by_name', 'created_at') # 预订记录列表页显示字段
    list_display = ('venue', 'booking_period_display', 'booked_by_name', 'created_at', 'updated_at')
    list_filter = ('venue', 'created_at', 'start_time') # 允许按场所和创建时间筛选
    search_fields = ('venue__name', 'booked_by_name', 'notes') # 允许搜索的字段
    
    # 定义表单中字段的顺序和分组 (可选, 但能改善编辑体验)
    fieldsets = (
        (None, {
            # 'fields': ('venue', 'booking_period', 'booked_by_name')
            'fields': ('venue', ('start_time', 'end_time'), 'booked_by_name')
        }),
        ('Additional Information', {
            'fields': ('notes',),
            'classes': ('collapse',) # 默认折叠此部分
        }),
    )
    
    # 如果希望在添加/编辑 VenueBooking 时，venue 字段使用下拉选择而不是输入框ID
    # raw_id_fields = () # 如果 Venue 数量很多，可以使用 ('venue',) 来获得一个搜索弹出框
    autocomplete_fields = ['venue'] # Django 2.0+ 推荐使用这个，需要在 VenueAdmin 中设置 search_fields
    # 确保 VenueAdmin 中有 search_fields = ('name',) 才能使 autocomplete_fields 生效
    # 在本例中，VenueAdmin 已有 search_fields
