# 🚗 AutoFleetX

AutoFleetX is a **Django-based car rental web application** with a modern **HTML/CSS frontend** and a robust **PostgreSQL backend** connected via Django’s ORM.  
It offers **real-time car rental management**, **secure authentication (Google login via Django Allauth)**, and a **mobile-responsive user interface**.

---

## ✨ Features

### 🔐 Authentication & User Management
- Local account signup/login with **custom user model**.
- **Google Login integration** using `django-allauth`.
- Existing local users can **link their Google accounts** after login.
- Password management with **secure password reset & change flows**.

### 🚘 Car Rental System
- Browse, search, and filter cars by brand, type, rent/day, or seating capacity.
- **Availability tracking**: Only available cars can be rented.
- **One active rental per user** (backend-validated).
- **Wallet system**: Users can add balance and pay directly from their account.
- Automatic rental completion & early return handling.

### 📩 Email & Notifications
- REST API endpoint for **rental confirmation emails**.
- Success/warning/error messages with user-friendly feedback.
- Email linking required to ensure reliable confirmation emails.

### 👨‍💼 Admin Dashboard
- Add, edit, or remove cars.
- Generate **PDF reports** for:
  - Customer rentals & spending.
  - Currently reserved cars.
- View and manage contact messages from users.
- Overview dashboard: total cars, users, and active rentals.

### 💻 Frontend
- Beautiful, **fully responsive UI** built with HTML & CSS.
- Pagination for car listings (9 cars per page).
- Sidebar navigation for user profiles.
- Smooth and modern layout optimized for desktop & mobile.

### 🛡️ Robust Error Handling
- Graceful validation with detailed error messages.
- Edge case handling for rentals, forms, and authentication.
- Safe redirects and secure session management.

---

## 🏗️ Tech Stack

- **Backend:** [Django](https://www.djangoproject.com/) (Python)
- **Frontend:** HTML5, CSS3
- **Database:** PostgreSQL with Django ORM
- **Authentication:** Django Allauth (Google OAuth 2.0)
- **Email & APIs:** Django REST Framework
- **PDF Generation:** `xhtml2pdf`

---

## 📂 Project Structure






---

## 🚀 Getting Started

```bash
1. Clone the Repository
git clone https://github.com/your-username/AutoFleetX.git
cd AutoFleetX

2. Create a Virtual Environment
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

3. Install Dependencies
pip install -r requirements.txt

4. Database Setup
Update your PostgreSQL credentials in settings.py, then run:

python manage.py makemigrations
python manage.py migrate

5. Create a Superuser
python manage.py createsuperuser

6. Run the Server
python manage.py runserver


Visit http://127.0.0.1:8000/
 in your browser.
```  
🧑‍💻 Usage

Users: Sign up or log in with Google, browse cars, rent, and manage their rentals & wallet.

Admins: Manage cars, view reports, and oversee the entire rental system.

Email Confirmations: Automatic confirmation email sent upon rental success.

📸 Screenshots

Add screenshots of your frontend (homepage, car listings, profile, admin dashboard).
(You can later upload .png/.jpg in a screenshots/ folder and link them here.)

🔑 Key Highlights

✅ Mobile responsive UI.

✅ Secure Google OAuth integration.

✅ Real-time rental availability management.

✅ PDF-based reporting for admins.

✅ REST API powered confirmation emails.

🤝 Contributing

Contributions are welcome! Feel free to fork the repo and submit pull requests.

📜 License

This project is licensed under the MIT License.


