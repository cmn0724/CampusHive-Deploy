# CampusHive-System
## Project Description
CampusHive is a comprehensive, web-based management system designed to streamline and centralize key academic and administrative operations within an educational institution. Developed as a final project for the Master of Computing program, this application provides a unified platform for managing users, courses, and equipment, thereby enhancing efficiency and improving the user experience for students, faculty, and staff.

The system is built with a modern technology stack, featuring a Python/Django backend and a clean, responsive user interface. It is designed to be scalable and maintainable, making it a robust foundation for future development.

***\*Live Demo:\**** A live version of this project is deployed and accessible at [http://campushive-hkmu-prod.ap-east-1.elasticbeanstalk.com/](http://campushive-hkmu-prod.ap-east-1.elasticbeanstalk.com/).


## Key Features
**User Management:**

- Separate registration and login for different user roles (Student, Teacher, Staff/Admin).

- Role-based access control (RBAC) to ensure users can only access relevant information and functionalities.

**Course Management:**

- Teachers and administrators can create, update, and delete courses.

- Students can view available courses and enroll or drop from them.

- Teachers can manage course materials by uploading and organizing files.

**Grading System:**

- Teachers can grade student assignments and record final course grades.

- Students can view their grades and feedback.

**Equipment Management:**

- Centralized inventory for all campus equipment.

-  Streamlined process for users to borrow and return equipment.

- System for reporting and tracking equipment repairs.

## Tech Stack
*   **Backend:** Python 3.12, Django 5.0
*   **Database:** PostgreSQL (production), SQLite3 (development)
*   **Frontend:** HTML5, CSS3, Bootstrap 5
*   **Web Server**: Gunicorn
*   **Reverse Proxy**: Caddy
*   **Deployment**: AWS Elastic Beanstalk, S3 for media storage
*   **Version Control:** Git, GitHub
## Local Setup and Installation
### Prerequisites

*   Python 3.10 or higher
*   pip (Python package installer)
*   Git
### Installation Steps
1. **Clone the repository:**

   ```bash
   git clone https://github.com/cmn0724/CampusHive-system.git
   cd CampusHive-system
   ```

2. **Create and activate a virtual environment:**

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

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```
   *This command will install all the necessary Python libraries listed in the `requirements.txt` file.*

4. **Database Setup:**

   The project is configured to use SQLite for local development by default. Run the following commands to create the database and its tables:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser - optional but recommended for admin access:**

   A superuser account is required to access the Django admin interface and manage the system.

   ```bash
   python manage.py createsuperuser
   ```

   Follow the prompts to set a username, email, and password.

6. **Download PostgreSQL and install pgAdmin**:

   Open the server with password: hkmu2025

7. **Run the development server:**

   ```bash
   python manage.py runserver
   ```
   The application will now be running at`http://127.0.0.1:8000/`. 
### Generating `requirements.txt`
After installing or updating packages in your virtual environment, run this command to update `requirements.txt`:
```bash
pip freeze > requirements.txt
```

### Creating Users with Different Roles

Once you have created a superuser, you can create other users (Students, Teachers, Staff) through the Django Admin interface:

1. **Log in to the Admin Panel:**
   - Navigate to `http://127.0.0.1:8000/admin/`.
   - Log in using the superuser credentials you just created.
2. **Add a New User:**
   - In the admin dashboard, find the "Users" section and click on "Add".
   - Enter a **Username** and **Password** for the new user.
   - **Important:** In the "Role" field, select the desired role (`Student`, `Teacher`, or `Staff`).
   - Fill in any other optional details and click "Save".
3. **Create a User Profile (Required for Students and Staff):**
   - After creating a user, go to the "User Profiles" section in the admin panel.
   - Click "Add" next to **Student Profiles** or **Employee Profiles**, depending on the user's role.
   - Select the newly created user from the dropdown list.
   - Fill in the required profile information (e.g., Student ID, Department).
   - Click "Save".

Now you can log out of the admin account and log in with the new user's credentials to test their role-specific permissions and views.
