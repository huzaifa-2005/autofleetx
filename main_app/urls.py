from django.urls import path
from . import views


urlpatterns = [
    # Authentication URLs
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'), 
    
    # Car listing URLs
    path('',views.home_view,name='home'),
    path('see-more-fleets/<str:vehicle_type>/', views.see_more_view, name='see_more'),
    path('all-cars/<int:scroll_to_section>/', views.all_cars_view, name='all-cars'),
    path('cars/page/<int:page>/<int:scroll_to_section>/', views.car_list_view, name='car_list'),
    path('cars/<int:car_id>/', views.car_detail_view, name='car_detail'),
    path('cars/<int:car_id>/rent/', views.rent_car, name='rent_car'),
    path('return/<int:rental_id>/', views.return_car, name='return_car'),


    
    # User account URLs 
    path('profile/', views.profile_view, name='profile'),
    path('rental-history/', views.rental_history_view, name='rental_history'),
    path('transactions/', views.transaction_history, name='transaction_history'),
    path('contact/', views.contact_us, name='contact_us'),
    path('services/', views.services_view, name='services'),
    # Admin URLs
    path('dashboard/admin-messages/', views.admin_contact_messages, name='admin_contact_messages'),
    path('dashboard/admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/admin/customer-report/', views.admin_customer_report, name='admin_customer_report'),
    path('dashboard/admin/reserved-cars/', views.admin_reserved_cars_report, name='admin_reserved_cars_report'),
    
     # PDF report URLs
    path('dashboard/admin/customer-report/pdf/', views.pdf_customer_report, name='pdf_customer_report'),
    path('dashboard/admin/reserved-cars/pdf/', views.pdf_reserved_cars_report, name='pdf_reserved_cars_report'),

    path('dashboard/admin/add-car/', views.admin_add_car, name='admin_add_car'),
    path('dashboard/admin/remove-cars/', views.admin_remove_cars, name='remove_cars'),
    path('car_images/<str:filename>/', views.car_image, name='car_image'),

   
]