# equipment/urls.py
from django.urls import path
from .views import EquipmentListView, EquipmentDetailView
from .views import EquipmentCreateView, EquipmentUpdateView, EquipmentDeleteView
from .views import BorrowEquipmentView
from .views import ReturnEquipmentView
from .views import MyBorrowingsView
from .views import CreateRepairRequestView
from .views import RepairRequestListView, RepairRequestDetailView, UpdateRepairRequestStatusView


app_name = 'equipment'

urlpatterns = [
    path('', EquipmentListView.as_view(), name='equipment_list'),
    path('<int:pk>/', EquipmentDetailView.as_view(), name='equipment_detail'),
    path('create/', EquipmentCreateView.as_view(), name='equipment_create'),
    path('<int:pk>/update/', EquipmentUpdateView.as_view(), name='equipment_update'),
    path('<int:pk>/delete/', EquipmentDeleteView.as_view(), name='equipment_delete'),
    path('<int:equipment_id>/borrow/', BorrowEquipmentView.as_view(), name='borrow_equipment'),
    # path('borrowing/<int:borrowing_record_id>/return/', ReturnEquipmentView.as_view(), name='return_equipment'),
    path('borrowing/<int:record_id>/return/', ReturnEquipmentView.as_view(), name='return_equipment_record'),
    path('my-borrowings/', MyBorrowingsView.as_view(), name='my_borrowings'),
    path('<int:equipment_id>/report-issue/', CreateRepairRequestView.as_view(), name='create_repair_request'),
    path('repair-requests/', RepairRequestListView.as_view(), name='repair_request_list'),
    path('repair-requests/<int:pk>/', RepairRequestDetailView.as_view(), name='repair_request_detail'),
    path('repair-requests/<int:pk>/update/', UpdateRepairRequestStatusView.as_view(), name='update_repair_request_status'),
]