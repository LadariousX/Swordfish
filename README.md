# Team swordfish
### CivicLens 

demo at [This link](https://estrella-felicitous-ian.ngrok-free.dev)

My team and I were not impressed with the upkeep of Corpus Christi's infrastructure from piling up trash or repeatedly patched roads. 

Our project Civic lens is a smart reporting app that allows normal residents to directly notify city services of issues
they come across. We built this project using the Django web framework, provides a well-rounded baseline and easy-to-use
Object-relational-mapper. We chose to add GPT models to our project since they are incredibly reliable easy to use and train.
getting good results at first as image recognition models cannot be trained. We overcame this by running the project
through two models: one had structured output while another  was fine-tuned with a listJson of examples. We all learned a lot from 
this project and the experience we gained collaborating with each other is priceless.

credentials for example accounts: 

Admin: 12345678a


# 🎟️ TicketPortal

> **A Django-based web application** that allows public users to submit tickets (image, location, comments, phone number) **without login**, while admins can view, categorize, and manage submissions directly from the **Django Admin Panel**.

TicketPortal is a lightweight ticket submission system built with **Django**.  
It enables **anonymous ticket reporting** and **admin-side management**, making it ideal for municipal issue reporting, feedback systems, or public service portals.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+  
- pip (Python package manager)  
- Git installed  

---

### Setup

#### 1 Clone the Repository
```bash
git clone https://github.com/<your-username>/TicketPortal.git
cd TicketPortal
```

#### 2 Create and Activate Virtual Environment
**Linux/Mac**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows**
```bash
python -m venv venv
venv\Scripts\activate
```

#### 3 Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4 Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

#### 5 Create Admin (Superuser)
```bash
python manage.py createsuperuser
```
Follow prompts to set:
- Username  
- Email  
- Password  

#### 6 Run the Server
```bash
python manage.py runserver
```

---

### Access the App

- **User Form →** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)  
  (Submit tickets — no login required)

- **Admin Panel →** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)  
  (Login with superuser credentials)

---