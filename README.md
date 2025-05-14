# CampusHive-System 
## Project Description
This is a comprehensive campus management system designed for the HKMU Computer Science final year project. It aims to provide an integrated platform for managing core campus affairs such as students, courses, equipment borrowing, club activities, etc., to improve operational efficiency and user experience.
## 主要功能 (Key Features)
*   用户管理 (User Management): 学生、教职工、管理员角色及权限。
*   课程管理 (Course Management): 课程信息、选课、成绩录入。
*   设备管理 (Equipment Management): 设备信息、借阅、归还跟踪。
*   部门与班级管理 (Department and Class Management): 组织架构管理。
*   (未来可能加入：社团活动、通知公告等)
*   (Features may include: Club activities, announcements in the future)
## 技术栈 (Tech Stack)
*   **后端 (Backend):** Python 3.12, Django 5.x
*   **数据库 (Database):** SQLite (开发阶段), PostgreSQL (生产环境考虑)
*   **前端 (Frontend):** HTML, CSS, JavaScript (暂定，可能引入框架如 Bootstrap 或 Vue.js/React)
*   **版本控制 (Version Control):** Git, GitHub (或其他)
## 安装与运行 (Setup and Run)
### 先决条件 (Prerequisites)
*   Python 3.10+ (推荐 3.12)
*   Pip (Python 包安装器)
*   Git
### 安装步骤 (Installation Steps)
1.  **克隆仓库 (Clone the repository):**
    ```bash
    git clone https://github.com/your-username/CampusHive-system.git
    cd CampusHive-system
    ```
2.  **创建并激活虚拟环境 (Create and activate a virtual environment):**
    *   Windows:
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```
    *   macOS/Linux:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
3.  **安装依赖 (Install dependencies):**
    ```bash
    pip install -r requirements.txt
    ```
    *(注意: 你需要先生成 `requirements.txt` 文件，见下方说明)*
4.  **数据库迁移 (Apply database migrations):**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
5.  **创建超级用户 (Create a superuser - optional but recommended for admin access):**
    ```bash
    python manage.py createsuperuser
    ```
    (按照提示输入用户名、邮箱和密码)
6.  **运行开发服务器 (Run the development server):**
    ```bash
    python manage.py runserver
    ```
    系统将在 `http://127.0.0.1:8000/` 上运行。
### 生成 `requirements.txt` (Generating `requirements.txt`)
在你的虚拟环境中，当安装了新的包或更新了包之后，运行以下命令来更新 `requirements.txt`：
(After installing or updating packages in your virtual environment, run this command to update `requirements.txt`:)
```bash
pip freeze > requirements.txt