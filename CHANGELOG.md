# 更新日志

## [未发布] - 2025-05-14  

### 新增 (Added)
- **用户模块**:
    - 用户模型增加角色字段 (`student`, `teacher`, `staff`, `admin`)。
    - 用户模型增加电话号码和出生日期字段。
    - 创建 `StudentProfile` 模型，包含学号、入学日期等。
    - 创建 `EmployeeProfile` 模型，包含工号、所属部门、入职日期等。
    - Django Admin 中 `User` 编辑页面集成 `StudentProfile` 和 `EmployeeProfile`的 Inline 编辑。
    - 为用户相关模型 (User, Department, StudentProfile, EmployeeProfile) 编写单元测试。
- **课程模块**:
    - 创建 `Class` (班级) 模型，包含班级名称、学年、班主任。
    - 创建 `Course` (课程) 模型，包含课程代码、标题、描述、所属部门、授课教师、学分。
    - 创建 `Enrollment` (选课记录) 模型，关联学生和课程，记录选课日期和成绩。
    - 实现课程列表视图 (`CourseListView`) 和课程创建视图 (`CourseCreateView`) 的基本功能。
    - 为课程相关模型 (Class, Course, Enrollment) 编写单元测试。
    - 为 `CourseListView` 和 `CourseCreateView` 编写了初步的视图单元测试。
- **设备模块**:
    - 创建 `EquipmentCategory` (设备分类) 模型。
    - 创建 `Equipment` (设备) 模型，包含设备名称、ID、分类、状态、总数量、可用数量、采购日期等。
    - 创建 `BorrowingRecord` (借用记录) 模型，关联设备和借用人，记录借用和归还信息。
    - 为设备相关模型 (EquipmentCategory, Equipment, BorrowingRecord) 编写单元测试。

### 修复 (Fixed)
- 修复了 `UserAdmin` 中 `list_filter` 因 `is_staff` 属性与字段冲突导致的 `admin.E116` 错误。
- 修复了 `CourseListView` 中因课程代码字段名不匹配 (`course_code` vs `code`) 导致的 `FieldError`。
- 解决了 `courses/tests.py` 和 `users/tests.py` 中的导入错误和属性引用错误。

### 变更 (Changed)
- `User` 模型的 `is_staff` 字段现在通过 `save()` 方法根据 `role` 字段自动同步。
- `Course` 模型的课程代码字段统一为 `code`。

---


### 新增
- 项目初始化。
- ...
