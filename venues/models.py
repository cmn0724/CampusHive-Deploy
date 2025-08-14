# venues/models.py
from django.db import models
from django.conf import settings # 用于关联 User 模型
from django.core.exceptions import ValidationError

class Venue(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Venue name")
    # 可以根据需要添加其他字段，如：
    # location_details = models.CharField(max_length=255, blank=True, null=True, verbose_name="位置详情")
    # capacity = models.PositiveIntegerField(blank=True, null=True, verbose_name="容量")
    # description = models.TextField(blank=True, null=True, verbose_name="描述")
    class Meta:
        verbose_name = "Venue"
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return self.name

class VenueBooking(models.Model):
    """
    场所预订记录模型
    """
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, verbose_name="Booking venue")
    # 预订时间段，这里简化为手动记录的文本字段，管理员自行规范格式
    # 例如："2024-07-30 14:00-16:00" 或 "每周三下午"
    # 如果未来需要基于时间段的查询或冲突检测，这里需要改成 DateTimeField for start and end
    # booking_period = models.CharField(max_length=255, verbose_name="Booking time")
    start_time = models.DateTimeField(verbose_name="Start time")
    end_time = models.DateTimeField(verbose_name="End time")
    booked_by_name = models.CharField(max_length=100, verbose_name="Booking user name")
    notes = models.TextField(blank=True, null=True, verbose_name="Comment")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creation time")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updating time")

    # @property
    def booking_period_display(self): # 用于在 list_display 中显示
        if self.start_time and self.end_time:
            start_formatted = self.start_time.strftime('%Y-%m-%d %H:%M')
            end_formatted = self.end_time.strftime('%Y-%m-%d %H:%M')
            return f"{start_formatted} - {end_formatted}"
        return "N/A"
    # booking_period_display.short_description = "预订时间段"
    booking_period_display.short_description = "Booking Period"

    def clean(self): # 添加简单的验证
        if self.start_time and self.end_time and self.start_time >= self.end_time:
            raise ValidationError("End time must be later than start time.")
        super().clean()
    
    # 预订人，可以直接记录姓名，或者关联到系统用户
    # 方案一：直接记录预订人姓名 (简单)
    # booked_by_name = models.CharField(max_length=100, verbose_name="Booking user name")
    # 方案二：关联到系统用户 (如果预订人是系统内的用户，更规范)
    # booked_by_user = models.ForeignKey(
    #     settings.AUTH_USER_MODEL,
    #     on_delete=models.SET_NULL, # 或者 models.PROTECT，取决于业务逻辑
    #     null=True,
    #     blank=True, # 允许管理员只填写姓名而不关联用户
    #     verbose_name="预订用户 (系统内)"
    # )
    
    # 可以添加一个备注字段
    # notes = models.TextField(blank=True, null=True, verbose_name="Comment")
    # created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creation time")
    # updated_at = models.DateTimeField(auto_now=True, verbose_name="Updating time")
    class Meta:
        verbose_name = "Venue booking record"
        verbose_name_plural = verbose_name
        ordering = ['-created_at', 'venue'] # 通常按创建时间倒序
    def __str__(self):
        # return f"{self.venue.name} - {self.booking_period} - by {self.booked_by_name}"
        return f"{self.venue.name} - {self.booking_period_display()} - by {self.booked_by_name}"
