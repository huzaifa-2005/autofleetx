#  AutoFleetX

## LIVE DEMO : https://autofleetx-production-c144.up.railway.app/
> This live demo is hosted on a trial deployment and will expire **30 days after the initial deployment date**.
AutoFleetX is a **Django-based car rental web application** with a modern **HTML/CSS frontend** and a robust **PostgreSQL backend** connected via Django’s ORM.
It offers **real-time car rental management**, **secure authentication (Google login via Django Allauth)**, and a **mobile-responsive user interface**.

---

##  Features

###  Authentication & User Management

* Local account signup/login with **custom user model**.
* **Google Login integration** using `django-allauth`.
* Existing local users can **link their Google accounts** after login.
* Password management with **secure password reset & change flows**.

###  Car Rental System

* Browse, search, and filter cars by brand, type, rent/day, or seating capacity.
* **Availability tracking**: Only available cars can be rented.
* **One active rental per user** (backend-validated).
* **Wallet system**: Users can add balance and pay directly from their account.
* Automatic rental completion & early return handling.

###  Email & Notifications

* REST API endpoint for **rental confirmation emails**.
* Success/warning/error messages with user-friendly feedback.
* Email linking required to ensure reliable confirmation emails.

###  Admin Dashboard

* Add, edit, or remove cars.
* Generate **PDF reports** for:

  * Customer rentals & spending.
  * Currently reserved cars.
* View and manage contact messages from users.
* Overview dashboard: total cars, users, and active rentals.

###  Frontend

* Beautiful, **fully responsive UI** built with HTML & CSS.
* Pagination for car listings (9 cars per page).
* Sidebar navigation for user profiles.
* Smooth and modern layout optimized for desktop & mobile.

###  Robust Error Handling

* Graceful validation with detailed error messages.
* Edge case handling for rentals, forms, and authentication.
* Safe redirects and secure session management.

---

##  Tech Stack

* **Backend:** [Django](https://www.djangoproject.com/) (Python)
* **Frontend:** HTML5, CSS3, Vanilla JavaScript
* **Database:** PostgreSQL with Django ORM
* **Authentication:** Django Allauth (Google OAuth 2.0)
* **Email & APIs:** Django REST Framework
* **PDF Generation:** `xhtml2pdf`

---

## 📂 Project Structure

```bash
AutoFleetX/
├── api/                # API app (REST endpoints)
├── Car_Rental_System/    # Django project config
├── main_app/           # Main business logic app
├── media/              # User-uploaded files
├── static/             # Static assets (CSS, JS, images)
├── templates/          # Shared HTML templates
├── venv/               # Virtual environment
├── .env                # Environment variables
├── .gitignore
├── build.sh
├── manage.py
├── Procfile
├── railway.json
├── README.md
└── requirements.txt
```

---

##  Key Highlights: REST API & Google OAuth

* **RESTful Email Notifications**:
  The system uses **Django REST Framework** to expose API endpoints for sending **confirmation emails** after successful car rentals.
  This ensures clean separation between frontend and backend, making email communication **scalable and maintainable**.

* **Advanced Google OAuth Integration**:
  Integrated using **`django-allauth`**, AutoFleetX supports:

  * **Sign in with Google** directly.
  * **Linking local accounts** with verified Google accounts post-authentication.
  * Smooth fallback between local login and Google OAuth.

This combination provides **flexibility, enhanced security, and a professional-grade authentication system**.

---

## 🚀 Getting Started

**1. Clone the Repository**

```bash
git clone https://github.com/huzaifa-2005/AutoFleetX.git
cd AutoFleetX
```

**2. Create and Activate Virtual Environment**

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

**3. Install Dependencies**

```bash
pip install -r requirements.txt
```

**4. Database Setup**
Update your PostgreSQL credentials in `settings.py`, then run:

```bash
python manage.py makemigrations
python manage.py migrate
```

**5. Create a Superuser**

```bash
python manage.py createsuperuser
```

**6. Run the Server**

```bash
python manage.py runserver
```



---

##  Usage

* **Users**: Sign up or log in with Google, browse cars, rent, and manage their rentals & wallet.
* **Admins**: Manage cars, view reports, track customers and rental records, and oversee the entire rental system.
* **Email Confirmations**: Automatic confirmation email sent upon rental success.

---

##  Screenshots

### App Preview :

<table width="100%"> 
<tr>
<td width="50%">      
&nbsp; 
<br>
<p align="center">
   🔹Landing Page For Users  
</p>
<img src="static\screenshots\landing.png" height=690px width=550px >
</td> 
<td width="50%">
<br>
<p align="center">
 🔹Browse Cars
</p>
<img src="static\screenshots\browse-cars.png" height=690px width=550px >  
</td>
</table>

<table width="100%"> 
<tr>
<td width="50%">      
&nbsp; 
<br>
<p align="center">
   🔹User Rental History  
</p>
<img src="static\screenshots\rental-history.png" height=2650px width=550px >
</td> 
<td width="50%">
<br>
<p align="center">
 🔹Admin Interface
</p>
<img src="static\screenshots\adm-interface.png" height=690px width=550px >  
</td>
</table>

<table width="100%"> 
<tr>
<td width="50%">      
&nbsp; 
<br>
<p align="center">
   🔹Admin Dashboard  
</p>
<img src="static\screenshots\admin-dash.png" height=1300px width=550px >
</td> 
<td width="50%">
<br>
<p align="center">
 🔹Confirmation Email
</p>
<img src="static\screenshots\email.png" height=350px width=670px >  
</td>
</table>

---

##  Summary

- ✅ Mobile responsive UI
- ✅ Secure Google OAuth integration
- ✅ A complex django powered backend with robust error handling 
- ✅ Real-time rental availability management
- ✅ PDF-based reporting for admins
- ✅ REST API powered confirmation emails
 
---

##  Contributing

Contributions are welcome! Feel free to fork the repo and submit pull requests.

---

##  License

This project is licensed under the MIT License.

---


