# equipment/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from .models import Equipment, BorrowingRecord, RepairRequest
from .forms import EquipmentForm, BorrowEquipmentForm, RepairRequestForm
from users.mixins import StaffRequiredMixin
from django.contrib import messages
from datetime import timedelta
from django import forms
from .filters import EquipmentFilter
from django.core.exceptions import PermissionDenied

class EquipmentListView(LoginRequiredMixin, ListView): # 任何登录用户都可以查看列表
    model = Equipment
    template_name = 'equipment/equipment_list.html' # 创建这个模板文件
    context_object_name = 'equipments' # 在模板中使用的变量名
    paginate_by = 10 # 可选：用于分页
    
    def get_queryset(self):
        queryset = super().get_queryset().order_by('name') # 获取基础 queryset
        self.filterset = EquipmentFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs # 返回筛选后的 queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterform'] = self.filterset.form # <--- 将 filterset 的表单传递给模板
        return context


class EquipmentDetailView(LoginRequiredMixin, DetailView):
    model = Equipment
    template_name = 'equipment/equipment_detail.html'
    context_object_name = 'equipment'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        equipment = self.get_object()
        # Get current and past borrowing records for this equipment
        context['borrowing_history'] = BorrowingRecord.objects.filter(equipment=equipment).order_by('-borrow_date').select_related('borrower')
        # Get repair requests for this equipment
        context['repair_requests'] = RepairRequest.objects.filter(equipment=equipment).order_by('-reported_at')
        return context
    
class EquipmentCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Equipment
    form_class = EquipmentForm
    template_name = 'equipment/equipment_form.html'
    success_url = reverse_lazy('equipment:equipment_list')

    def form_valid(self, form):
        messages.success(self.request, f"Equipment '{form.instance.name}' created successfully.")
        return super().form_valid(form)

class EquipmentUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Equipment
    form_class = EquipmentForm
    template_name = 'equipment/equipment_form.html'
    # success_url = reverse_lazy('equipment:equipment_list') # Or detail view

    def get_success_url(self):
        return reverse('equipment:equipment_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, f"Equipment '{form.instance.name}' updated successfully.")
        return super().form_valid(form)

class EquipmentDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Equipment
    template_name = 'equipment/equipment_confirm_delete.html'
    success_url = reverse_lazy('equipment:equipment_list')
    context_object_name = 'equipment' # To match template

    def post(self, request, *args, **kwargs):
        equipment_name = self.get_object().name
        messages.success(request, f"Equipment '{self.get_object().name}' has been deleted.")
        return super().post(request, *args, **kwargs)

class BorrowEquipmentView(LoginRequiredMixin, View): # Changed to View for more control, or use FormView/CreateView
    form_class = BorrowEquipmentForm
    template_name = 'equipment/borrow_equipment_form.html' # Create this template

    def get(self, request, equipment_id):
        equipment = get_object_or_404(Equipment, id=equipment_id)
        if not (equipment.status == Equipment.STATUS_AVAILABLE and equipment.quantity_available > 0):
            messages.error(request, f"'{equipment.name}' is not available for borrowing.")
            return redirect('equipment:equipment_detail', pk=equipment_id)
        
        # Pre-fill due_date with a default (e.g., 7 days from now)
        default_due_date = timezone.now() + timedelta(days=7)
        form = self.form_class(initial={'due_date': default_due_date.strftime('%Y-%m-%dT%H:%M')})
        return render(request, self.template_name, {'form': form, 'equipment': equipment})

    def post(self, request, equipment_id):
        equipment = get_object_or_404(Equipment, id=equipment_id)
        if not (equipment.status == Equipment.STATUS_AVAILABLE and equipment.quantity_available > 0):
            messages.error(request, f"'{equipment.name}' is not available for borrowing (state changed).")
            return redirect('equipment:equipment_detail', pk=equipment_id)

        form = self.form_class(request.POST)
        if form.is_valid():
            borrowing_record = form.save(commit=False)
            borrowing_record.equipment = equipment
            borrowing_record.borrower = request.user
            borrowing_record.is_returned = False # Explicitly set
            borrowing_record.save()

            # Update equipment status and quantity
            equipment.quantity_available -= 1
            if equipment.quantity_available == 0 and equipment.status != Equipment.STATUS_REPAIR:
                equipment.status = Equipment.STATUS_BORROWED  
            equipment.save()

            messages.success(request, f"You have successfully borrowed '{equipment.name}'. Due by {borrowing_record.due_date.strftime('%Y-%m-%d %H:%M')}.")
            return redirect('equipment:my_borrowings') # Redirect to user's borrowing list
        
        return render(request, self.template_name, {'form': form, 'equipment': equipment})

class ReturnEquipmentView(LoginRequiredMixin, View):
    def post(self, request, record_id):
        borrowing_record = get_object_or_404(BorrowingRecord, id=record_id)
        equipment = borrowing_record.equipment

        # 权限检查：
        # 1. 借阅者本人可以归还
        # 2. 具有 'is_staff_member_role' 的用户可以归还 (例如老师或管理员)
        # 3. 老师可以归还 (如果 is_teacher 和 is_staff_member_role 是独立的)
        
        can_return = False
        if request.user == borrowing_record.borrower:
            can_return = True
        elif hasattr(request.user, 'is_staff_member_role') and request.user.is_staff_member_role:
            can_return = True
        # 如果老师的归还权限不被 is_staff_member_role 覆盖，可以单独添加：
        # elif hasattr(request.user, 'is_teacher') and request.user.is_teacher:
        #     can_return = True
        if not can_return:
            # messages.error(request, "You do not have permission to return this item.")
            # return redirect('equipment:equipment_detail', pk=equipment.pk)
            raise PermissionDenied("You do not have permission to return this item.") # 这样会直接返回 403
        
        if borrowing_record.is_returned:
            messages.warning(request, "This item has already been marked as returned.")
        else:
            borrowing_record.is_returned = True
            borrowing_record.return_date = timezone.now()
            # borrowing_record.save()

            equipment.quantity_available = min(equipment.quantity_total, equipment.quantity_available + 1)
            # 更新设备状态
            # 检查是否还有其他未归还的相同设备的借用记录
            active_borrows_for_this_equipment_type = BorrowingRecord.objects.filter(
                equipment=equipment,
                is_returned=False
            ).exclude(pk=borrowing_record.pk).count() # 排除当前正在归还的这条记录
            
            if equipment.status == Equipment.STATUS_REPAIR:
                # 如果设备正在维修中，归还不应改变其维修状态，除非你有特定逻辑
                pass
            elif active_borrows_for_this_equipment_type == 0:
                # 如果这是该设备类型最后一条被归还的记录，则设备状态变回可用
                equipment.status = Equipment.STATUS_AVAILABLE
            # 如果你希望只要 quantity_available > 0 且不是维修中，就变为 AVAILABLE，可以添加以下逻辑：
            # elif equipment.quantity_available > 0 and equipment.status != Equipment.STATUS_REPAIR:
            #    equipment.status = Equipment.STATUS_AVAILABLE
            try:
                equipment.save()
                borrowing_record.save() # 在 equipment 保存成功后再保存
                messages.success(request, f"'{equipment.name}' (borrowed by {borrowing_record.borrower.username}) has been marked as returned.")
            except Exception as e:
                messages.error(request, f"An error occurred while trying to return the equipment: {e}")
        
        return redirect('equipment:equipment_detail', pk=equipment.pk)
    
    def get(self, request, record_id): # 处理直接通过GET访问此URL的情况
        # GET请求不应该改变状态，所以重定向
        borrowing_record = get_object_or_404(BorrowingRecord, id=record_id)
        # messages.info(request, "To return equipment, please use the 'Return' button.")
        messages.info(request, "To return equipment, please use the 'Return' button on the equipment detail page or borrowings list.")
        return redirect('equipment:equipment_detail', pk=borrowing_record.equipment.pk)

class MyBorrowingsView(LoginRequiredMixin, ListView):
    model = BorrowingRecord
    template_name = 'equipment/my_borrowings.html'
    context_object_name = 'borrowing_records'
    paginate_by = 10

    def get_queryset(self):
        return BorrowingRecord.objects.filter(borrower=self.request.user).order_by('-borrow_date').select_related('equipment')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['timezone_now'] = timezone.now() # Pass current time to template
        return context
        
class CreateRepairRequestView(LoginRequiredMixin, CreateView):
    model = RepairRequest
    form_class = RepairRequestForm
    template_name = 'equipment/repair_request_form.html' # Create this

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.equipment_item = get_object_or_404(Equipment, id=self.kwargs['equipment_id'])
        

    def form_valid(self, form):
        form.instance.equipment = self.equipment_item
        form.instance.reporter = self.request.user
        messages.success(self.request, f"Repair request for '{self.equipment_item.name}' submitted.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('equipment:equipment_detail', kwargs={'pk': self.equipment_item.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['equipment'] = self.equipment_item
        return context

class RepairRequestListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = RepairRequest
    template_name = 'equipment/repair_request_list.html' # Create this
    context_object_name = 'repair_requests'
    paginate_by = 10

    def get_queryset(self):
        # Optionally filter by status, e.g., show pending by default
        status_filter = self.request.GET.get('status')
        queryset = RepairRequest.objects.all().select_related('equipment', 'reporter').order_by('-reported_at')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = RepairRequest.STATUS_CHOICES
        return context

class RepairRequestDetailView(LoginRequiredMixin, StaffRequiredMixin, DetailView): # Or UpdateView to change status
    model = RepairRequest
    template_name = 'equipment/repair_request_detail.html' # Create this
    context_object_name = 'repair_request'

class UpdateRepairRequestStatusView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = RepairRequest
    fields = ['status', 'resolution_notes', 'resolved_at']
    template_name = 'equipment/repair_request_update_form.html' # Create this
    context_object_name = 'repair_request'

    def get_form(self, form_class=None): # Add date widget for resolved_at
        form = super().get_form(form_class)
        form.fields['resolved_at'].widget = forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M')
        form.fields['resolved_at'].input_formats=['%Y-%m-%dT%H:%M']
        form.fields['resolved_at'].required = False # Make it optional
        if 'resolution_notes' in form.fields: # 检查一下，因为 fields 中可能没有它
             form.fields['resolution_notes'].widget = forms.Textarea(attrs={'rows': 4, 'class':'form-control'})
        return form

    def form_valid(self, form):
        repair_request = form.instance # 获取当前操作的报修对象
        equipment = repair_request.equipment # 获取对应的设备

        # 如果状态被设置为“已解决” (STATUS_RESOLVED)
        if repair_request.status == RepairRequest.STATUS_RESOLVED:
            if not repair_request.resolved_at: # 如果解决日期未手动设置
                repair_request.resolved_at = timezone.now() # 自动设置为当前时间
            
            # 检查设备是否因为此报修而处于“维修中”状态
            # 并且没有其他“未解决”的报修请求针对此设备
            other_pending_repairs = RepairRequest.objects.filter(
                equipment=equipment,
                status__in=[RepairRequest.STATUS_PENDING, RepairRequest.STATUS_IN_PROGRESS]
            ).exclude(pk=repair_request.pk).exists()
            if equipment.status == Equipment.STATUS_REPAIR and not other_pending_repairs:
                equipment.status = Equipment.STATUS_AVAILABLE # 将设备状态改回“可用”
                equipment.save()
        
        # 如果状态被设置为“已关闭” (STATUS_CLOSED)，也认为问题已解决
        elif repair_request.status == RepairRequest.STATUS_CLOSED:
            if not repair_request.resolved_at: # 如果解决日期未手动设置 (例如直接从未解决跳到关闭)
                repair_request.resolved_at = timezone.now()
            # 同样检查设备状态
            other_pending_repairs = RepairRequest.objects.filter(
                equipment=equipment,
                status__in=[RepairRequest.STATUS_PENDING, RepairRequest.STATUS_IN_PROGRESS]
            ).exclude(pk=repair_request.pk).exists()
            if equipment.status == Equipment.STATUS_REPAIR and not other_pending_repairs:
                equipment.status = Equipment.STATUS_AVAILABLE
                equipment.save()
        
        # 如果状态从“已解决”或“已关闭”改回“处理中”或“待处理”
        elif repair_request.status in [RepairRequest.STATUS_PENDING, RepairRequest.STATUS_IN_PROGRESS]:
            repair_request.resolved_at = None # 清除解决日期
            # 如果设备之前是“可用”的，现在因为这个问题重新打开，应该将其标记为“维修中”
            if equipment.status == Equipment.STATUS_AVAILABLE:
                equipment.status = Equipment.STATUS_REPAIR
                equipment.save()
        
        messages.success(self.request, f"Status for repair request of '{equipment.name}' updated.")
        return super().form_valid(form) # 保存 repair_request 的更改

    def get_success_url(self):
        return reverse('equipment:repair_request_detail', kwargs={'pk': self.object.pk})