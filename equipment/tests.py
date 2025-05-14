from django.test import TestCase
# Create your tests here.
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import EquipmentCategory, Equipment, BorrowingRecord
User = get_user_model()

class EquipmentCategoryModelTests(TestCase):
    """
    测试 EquipmentCategory (设备分类) 模型
    """
    @classmethod
    def setUpTestData(cls):
        cls.category = EquipmentCategory.objects.create(
            name='Electronics',
            description='Electronic devices and components.'
        )
    def test_category_creation(self):
        # 测试设备分类的成功创建
        self.assertEqual(self.category.name, 'Electronics')
        self.assertEqual(self.category.description, 'Electronic devices and components.')
    def test_category_str_representation(self):
        # 测试 EquipmentCategory 模型的 __str__ 方法
        # 假设 __str__ 返回分类名称
        self.assertEqual(str(self.category), 'Electronics')

class EquipmentModelTests(TestCase):
    """
    测试 Equipment (设备) 模型
    """
    @classmethod
    def setUpTestData(cls):
        cls.category = EquipmentCategory.objects.create(name='Lab Equipment')
        cls.equipment = Equipment.objects.create(
            name='Microscope Model X',
            identifier='MICRO-001',
            category=cls.category,
            status=Equipment.STATUS_AVAILABLE, # 假设模型中有 STATUS_AVAILABLE 常量
            quantity_total=5,
            quantity_available=5, #可能会根据逻辑自动计算，或手动设置
            # purchase_date 可以是 auto_now_add 或手动设置
            purchase_date=timezone.now().date(),
            description='High power optical microscope.'
        )
        # 如果 quantity_available 不是通过 save 方法自动计算的，需要在这里设置
        # 例如，如果在模型中定义了 pre_save 信号或重写了 save 方法来更新它
        # 或者，如果它只是一个简单字段，则在创建时赋值
        if not hasattr(cls.equipment, 'quantity_available') or cls.equipment.quantity_available is None:
             cls.equipment.quantity_available = cls.equipment.quantity_total # 简单的初始假设
             cls.equipment.save()
    def test_equipment_creation(self):
        # 测试设备的成功创建
        self.assertEqual(self.equipment.name, 'Microscope Model X')
        self.assertEqual(self.equipment.identifier, 'MICRO-001')
        self.assertEqual(self.equipment.category, self.category)
        self.assertEqual(self.equipment.status, Equipment.STATUS_AVAILABLE)
        self.assertEqual(self.equipment.quantity_total, 5)
        # 根据 quantity_available 的实现来测试
        self.assertEqual(self.equipment.quantity_available, 5) # 假设初始时等于 total
        self.assertIsNotNone(self.equipment.purchase_date)
    def test_equipment_str_representation(self):
        # 测试 Equipment 模型的 __str__ 方法
        # 假设 __str__ 返回 "设备名称 (设备ID)"
        expected_str = f"{self.equipment.name} ({self.equipment.identifier})"
        self.assertEqual(str(self.equipment), expected_str)
    def test_equipment_status_choices(self):
        # 测试设备状态是否在预期的选项内
        # 这更多是模型定义层面的，但可以简单验证
        self.assertIn(self.equipment.status, [choice[0] for choice in Equipment.STATUS_CHOICES]) # 假设有 STATUS_CHOICES

class BorrowingRecordModelTests(TestCase):
    """
    测试 BorrowingRecord (借用记录) 模型
    """
    @classmethod
    def setUpTestData(cls):
        cls.borrower_user = User.objects.create_user(
            username='borrower1',
            password='password',
            role=User.ROLE_STUDENT # 或其他允许借用的角色
        )
        category = EquipmentCategory.objects.create(name='Audio Visual')
        cls.equipment_item = Equipment.objects.create(
            name='Projector P100',
            identifier='PROJ-001',
            category=category,
            quantity_total=1,
            quantity_available=1, # 初始可用
            status=Equipment.STATUS_AVAILABLE
        )
        cls.record = BorrowingRecord.objects.create(
            equipment=cls.equipment_item,
            borrower=cls.borrower_user,
            borrow_date=timezone.now(),
            due_date=timezone.now() + timezone.timedelta(days=7)
            # is_returned 默认为 False, return_date 默认为 None
        )
    def test_borrowing_record_creation(self):
        # 测试借用记录的成功创建
        self.assertEqual(self.record.equipment, self.equipment_item)
        self.assertEqual(self.record.borrower, self.borrower_user)
        self.assertIsNotNone(self.record.borrow_date)
        self.assertIsNotNone(self.record.due_date)
        self.assertFalse(self.record.is_returned)
        self.assertIsNone(self.record.return_date)
    def test_borrowing_record_str_representation(self):
        # 测试 BorrowingRecord 模型的 __str__ 方法
        # 假设 __str__ 返回 "设备名称 borrowed by 用户名 on 借用日期"
        expected_str = f"{self.equipment_item.name} borrowed by {self.borrower_user.username}"
        # borrow_date_str = self.record.borrow_date.strftime('%Y-%m-%d') # 格式化日期
        # expected_str = f"{self.equipment_item.name} borrowed by {self.borrower_user.username} on {borrow_date_str}"
        self.assertEqual(str(self.record), expected_str)
    def test_mark_as_returned(self):
        # 测试标记为已归还的逻辑 (如果模型中有此方法或通过保存实现)
        self.record.is_returned = True
        self.record.return_date = timezone.now()
        self.record.save()
        updated_record = BorrowingRecord.objects.get(id=self.record.id)
        self.assertTrue(updated_record.is_returned)
        self.assertIsNotNone(updated_record.return_date)
        # 如果归还会影响 Equipment.quantity_available，也应该在这里测试
        # self.equipment_item.refresh_from_db()
        # self.assertEqual(self.equipment_item.quantity_available, 1) # 假设归还后数量加回