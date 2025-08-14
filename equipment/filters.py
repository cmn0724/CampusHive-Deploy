# equipment/filters.py
import django_filters
from .models import Equipment, EquipmentCategory

class EquipmentFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Search by Name') # 按名称搜索 (不区分大小写包含)
    category = django_filters.ModelChoiceFilter(queryset=EquipmentCategory.objects.all(), label='Category') # 按分类筛选
    status = django_filters.ChoiceFilter(choices=Equipment.STATUS_CHOICES, label='Status') # 按状态筛选

    class Meta:
        model = Equipment
        fields = ['name', 'category', 'status']