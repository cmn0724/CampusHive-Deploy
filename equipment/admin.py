# equipment/admin.py
from django.contrib import admin
# Register your models here.
from django.utils.translation import gettext_lazy as _ # 导入翻译函数
from .models import EquipmentCategory, Equipment, BorrowingRecord # 导入所有需要管理的模型
@admin.register(EquipmentCategory) # 注册 EquipmentCategory 模型
class EquipmentCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'get_equipment_count') # 列表页显示的字段
    search_fields = ('name',) # 可搜索的字段
    def get_equipment_count(self, obj):
        # Equipment 模型中 category 字段的 related_name 默认为 'equipment_set' 或你自定义的 'equipment_items'
        return obj.equipment_items.count()
    get_equipment_count.short_description = _('Number of Equipment Items') # 列的显示名称
@admin.register(Equipment) # 注册 Equipment 模型
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'identifier', 'category', 'status', 'quantity_total', 'quantity_available', 'purchase_date') # 列表页显示的字段
    search_fields = ('name', 'identifier', 'category__name') # 可搜索的字段
    list_filter = ('status', 'category', 'purchase_date') # 可筛选的字段
    autocomplete_fields = ['category'] # 为 'category' 字段启用自动完成
    ordering = ('name',) # 默认排序
    # 如果 quantity_available 是通过借还逻辑自动更新的，可以考虑设为只读
    # readonly_fields = ('quantity_available',)
@admin.register(BorrowingRecord) # 注册 BorrowingRecord 模型
class BorrowingRecordAdmin(admin.ModelAdmin):
    list_display = ('equipment', 'borrower', 'borrow_date', 'due_date', 'return_date', 'is_returned') # 列表页显示的字段
    search_fields = ('equipment__name', 'equipment__identifier', 'borrower__username') # 可搜索的字段
    list_filter = ('is_returned', 'borrow_date', 'due_date', 'return_date', 'borrower__role') # 可筛选的字段
    autocomplete_fields = ['equipment', 'borrower'] # 为 'equipment' 和 'borrower' 字段启用自动完成
    date_hierarchy = 'borrow_date' # 在列表页顶部添加日期层级导航
    actions = ['mark_as_returned', 'mark_as_not_returned'] # 添加自定义action
    def mark_as_returned(self, request, queryset):
        # 自定义 action，将选中的记录标记为已归还
        queryset.update(is_returned=True, return_date=admin.utils.timezone.now()) # 假设需要记录归还时间
    mark_as_returned.short_description = _("Mark selected records as returned") # Action的显示名称
    def mark_as_not_returned(self, request, queryset):
        # 自定义 action，将选中的记录标记为未归还
        queryset.update(is_returned=False, return_date=None)
    mark_as_not_returned.short_description = _("Mark selected records as NOT returned")