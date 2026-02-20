# Tech1 MMS API

**Tech1 MMS API** is a Django REST API for managing **job cards** and **job statuses** with role-based access for **technicians** and **admins**.  
It is designed to be easy to set up using a single `setup_project.sh` script so clients can get the project running quickly.

---

## **Features**

- Create, update, and retrieve **job cards**
- Log **job status changes** automatically
- Bulk import job card data via CSV
- Role-based access control for **technicians** and **admins**
- Ready to run with Python, Django REST Framework, and Redis

---

## **Requirements**

- Python 3.13+
- Django 5.x
- Django REST Framework
- Redis 8.x
- Git
- Linux-based system (Ubuntu/Debian recommended)

---

## **Setup Instructions**

1. **Clone the repository**
```bash
git clone https://github.com/Cjte/tech1-mms-api.git
cd tech1-mms-api


# Make setup script executable (Linux/Mac)
sudo chmod +x setup_project.sh

# Run setup script
./setup_project.sh

python manage.py runserver
