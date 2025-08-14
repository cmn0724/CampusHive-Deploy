from django.db import models
# Create your models here.
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class EquipmentCategory(models.Model):
    name = models.CharField(_('Category Name'), max_length=100, unique=True) # 分类名称
    description = models.TextField(_('Description'), blank=True, null=True) # 描述

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Equipment Category') # 设备分类
        verbose_name_plural = _('Equipment Categories') # 设备分类 (复数)

class Equipment(models.Model):
    name = models.CharField(_('Equipment Name'), max_length=200) # 设备名称
    category = models.ForeignKey(EquipmentCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='equipment_items') # 所属分类
    identifier = models.CharField(_('Identifier/Serial Number'), max_length=100, unique=True) # 标识符/序列号
    description = models.TextField(_('Description'), blank=True) # 描述
    quantity_total = models.PositiveIntegerField(_('Total Quantity'), default=1) # 总数量 (用于消耗品或批量物品)
    quantity_available = models.PositiveIntegerField(_('Available Quantity'), default=1) # 可用数量 (用于跟踪可用性)
    # status (例如: available (可用), borrowed (已借出), under_repair (维修中))
    STATUS_AVAILABLE = 'available'
    STATUS_BORROWED = 'borrowed'
    STATUS_REPAIR = 'under_repair'
    STATUS_CHOICES = [
        (STATUS_AVAILABLE, _('Available')), # 可用
        (STATUS_BORROWED, _('Borrowed')), # 已借出
        (STATUS_REPAIR, _('Under Repair')), # 维修中
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_AVAILABLE) # 状态
    purchase_date = models.DateField(_('Purchase Date'), null=True, blank=True) # 购买日期
    # location (位置), condition (状况) 等

    def __str__(self):
        return f"{self.name} ({self.identifier})"

    def save(self, *args, **kwargs):
        # 基本逻辑确保可用数量不会被错误管理
        if self.quantity_available > self.quantity_total:
            self.quantity_available = self.quantity_total
        super().save(*args, **kwargs)

class BorrowingRecord(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='borrowings') # 所借设备
    borrower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='borrowed_items'
        # limit_choices_to={'role__in': ['student', 'teacher']} # 如果只有学生/教师可以借用
    ) # 借用人
    borrow_date = models.DateTimeField(auto_now_add=True) # 借用日期
    due_date = models.DateTimeField() # 应还日期
    return_date = models.DateTimeField(null=True, blank=True) # 归还日期
    is_returned = models.BooleanField(default=False) # 是否已归还
    # notes (备注)

    def __str__(self):
        return f"{self.equipment.name} borrowed by {self.borrower.username}" # 某设备被某用户借用
    
    @property
    def is_overdue(self): 
        if self.is_returned:
            return False
        return self.due_date < timezone.now()

# 其他模型: RepairRequest (报修请求) (根据你的 ERD)
class RepairRequest(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='repair_requests')
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reported_repairs')
    reported_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(_('Problem Description'))
    # 定义状态常量
    STATUS_PENDING = 'pending'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_RESOLVED = 'resolved'
    STATUS_CLOSED = 'closed' # 可选：已解决且关闭
    # 定义状态选项
    STATUS_CHOICES = [
        (STATUS_PENDING, _('Pending Review')),
        (STATUS_IN_PROGRESS, _('In Progress')),
        (STATUS_RESOLVED, _('Resolved')),
        (STATUS_CLOSED, _('Closed')),
    ]
    status = models.CharField(
        _('Status'),
        max_length=20,
        choices=STATUS_CHOICES, # 现在 STATUS_CHOICES 已经被定义了
        default=STATUS_PENDING   # STATUS_PENDING 也被定义了
    )
    resolved_at = models.DateTimeField(_('Resolved At'), null=True, blank=True)
    resolution_notes = models.TextField(_('Resolution Notes'), blank=True)
    # technician = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='handled_repairs', limit_choices_to={'is_staff': True}) # 可选：负责的技术员
    def __str__(self):
        return f"Repair for {self.equipment.name} ({self.get_status_display()})"
    class Meta:
        verbose_name = _('Repair Request')
        verbose_name_plural = _('Repair Requests')
        ordering = ['-reported_at']
    def save(self, *args, **kwargs):
        if self.status == self.STATUS_RESOLVED and not self.resolved_at:
            self.resolved_at = timezone.now()
        # 如果从 resolved/closed 变回 pending/in_progress，清除 resolved_at
        elif self.status in [self.STATUS_PENDING, self.STATUS_IN_PROGRESS] and self.resolved_at:
            self.resolved_at = None
        super().save(*args, **kwargs)