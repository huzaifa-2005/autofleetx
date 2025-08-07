from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone
from django.utils.timezone import is_naive, make_aware
from django.http import HttpResponse
from django.template.loader import render_to_string
import datetime
import io
from xhtml2pdf import pisa
from django.urls import reverse
from .models import CustomUser, Car, Rental, Transaction, ContactMessage
from .forms import CustomUserCreationForm, CustomUserLoginForm, AddBalanceForm, AdminCarForm, ProfileForm
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q
from django.utils.http import url_has_allowed_host_and_scheme


def is_admin(user):
    """Check if the user is an admin"""
    return user.is_superuser



# Authentication Views
def signup_view(request):
    """Handle user registration"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            messages.success(request, f'Account created successfully. Welcome, {user.first_name}!',extra_tags='account-created')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'main_app/signup.html', {'form': form})

from django.utils.http import url_has_allowed_host_and_scheme

def login_view(request):
    next_url = request.GET.get('next', '')
    form = CustomUserLoginForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                
                # Safely redirect to next_url if present
                if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                    return redirect(next_url)
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password', extra_tags='invalid-credentials')
    
    return render(request, 'main_app/login.html', {'form': form})

@login_required
def logout_view(request):
    """Handle user logout via POST"""
    if request.method == 'POST':
        logout(request)
        messages.info(request, 'You have been logged out.', extra_tags="auth")
    return redirect('login')

def all_cars_view(request, scroll_to_section=0):

    Rental.check_returns()

    if request.method == "POST" and request.user.is_superuser:
        name = request.POST.get("name", "").strip()
        brand = request.POST.get("brand", "").strip()
        seating_capacity = request.POST.get("seating_capacity", "").strip()
        rent_per_day = request.POST.get("rent_per_day", "").strip()
        vehicle_type = request.POST.get("vehicle_type", "").strip()
        
        filters = Q()
        # if name is not an empty string then we will add the filter
        if name:
            filters |= Q(name__icontains=name)
        if brand:
            filters |= Q(brand__icontains=brand)
        if seating_capacity:
            try:  
                filters |= Q(seating_capacity=int(seating_capacity))   
            except ValueError:
                messages.error(request, "Seating capacity must be a positive number.",extra_tags="seating-capacity-error")
        if rent_per_day:
            try:
                filters |= Q(rent_per_day=int(rent_per_day))
            except ValueError:
                messages.error(request, "Rent per day must be a positive number.",extra_tags="rent-per-day-error")
        if vehicle_type:
            filters |= Q(vehicle_type__icontains=vehicle_type)

        if filters:  # Only search if at least one field was filled
            try:
                cars = Car.objects.filter(filters)
                if not cars.exists():
                    messages.info(request, "No cars found matching your search criteria.",extra_tags="no-cars-found")
                    cars = Car.objects.all()  # Fallback to all cars if no results
            except Exception as e:
                messages.error(request, f"Error while searching: {e}",extra_tags="search-error")
                cars = Car.objects.all()
        else:
            messages.info(request, "No search criteria provided.",extra_tags="no-search-criteria")
            cars = Car.objects.all()

        paginator = Paginator(cars, 9)
        page_obj = paginator.get_page(1)

        context = {
            'page_obj': page_obj,
            'total_pages': paginator.num_pages,
            'scroll_to_section': True,
            'current_page': 1
        }
        return render(request, "main_app/all-cars.html", context)
    if request.method == "POST" and not request.user.is_superuser:
        brand = request.POST.get("brand", "").strip()
        seating_capacity = request.POST.get("seating_capacity", "").strip()
        max_rent = request.POST.get("max_rent", "").strip()
        min_rent = request.POST.get("min_rent", "").strip()        
        vehicle_type = request.POST.get("vehicle_type", "").strip()
        
        cars= Car.objects.filter(available=True)
        if min_rent:
            try:
                cars = cars.filter(rent_per_day__gte=int(min_rent))
            except ValueError:
                messages.error(request, "Rent per day must be a positive number.",extra_tags="rent-per-day-error")   
        if max_rent:
            try:
                cars = cars.filter(rent_per_day__lte=int(max_rent))
            except ValueError:
                messages.error(request, "Rent per day must be a positive number.",extra_tags="rent-per-day-error") 
                   
        if brand:
            cars = cars.filter(brand__icontains=brand)
        if seating_capacity:
            try:  
                cars = cars.filter(seating_capacity=int(seating_capacity))   
            except ValueError:
                messages.error(request, "Seating capacity must be a positive number.",extra_tags="seating-capacity-error")
        if vehicle_type:
            cars=cars.filter(vehicle_type__icontains=vehicle_type)
         
        try:
            if not any([brand, seating_capacity, min_rent, max_rent, vehicle_type]):
                messages.info(request, "No search criteria provided.", extra_tags="no-search-criteria")
                cars=Car.objects.all()
            elif not cars.exists():
                messages.info(request, "No cars found matching your search criteria.", extra_tags="no-cars-found") 
                cars=Car.objects.all()

        
        except Exception as e:
            messages.error(request, f"Error while searching: {e}",extra_tags="search-error")
            cars = Car.objects.all()
        

        paginator = Paginator(cars, 9)
        page_obj = paginator.get_page(1)

        context = {
            'page_obj': page_obj,
            'total_pages': paginator.num_pages,
            'scroll_to_section': True,
            'current_page': 1
        }
        return render(request, "main_app/all-cars.html", context)
    
    
    cars = Car.objects.all()
    paginator = Paginator(cars, 9)
    page_obj = paginator.get_page(1)
    if bool(scroll_to_section) == False:
        context = {
            'page_obj': page_obj,
            'total_pages': paginator.num_pages,
            'scroll_to_section': False,
            'current_page': 1
        }
    else:
        context = {
            'page_obj': page_obj,
            'total_pages': paginator.num_pages,
            'scroll_to_section': True,
            'current_page': 1
        }    
    return render(request, 'main_app/all-cars.html', context)

def car_list_view(request, page=1, scroll_to_section=False):
    """View for paginated car listings"""
    cars = Car.objects.all()
    paginator = Paginator(cars, 9)  # 9 cars per page (except last page might have 8)
    page_obj = paginator.get_page(page)
    
    context = {
        'page_obj': page_obj,
        'total_pages': paginator.num_pages,
        'current_page': page,
        'scroll_to_section': bool(scroll_to_section)
    }
    return render(request, 'main_app/all-cars.html', context)



def home_view(request):
    Rental.check_returns()
    return render(request, 'main_app/home.html')
    

@login_required

def profile_view(request):
    """User profile page"""
    user = request.user
    form = AddBalanceForm()
    profile_form = ProfileForm(instance=user)
    if request.method == 'POST':
        # Handling Add Balance Form
        if 'balance_submit' in request.POST:
            form = AddBalanceForm(request.POST)
            profile_form = ProfileForm(instance=user)  
            if form.is_valid():
                amount = form.cleaned_data['amount']
                try:
                    user.add_balance(amount)
                    Transaction.objects.create(
                        user=user,
                        amount=amount,
                        transaction_type='ADD',
                        description='Added to wallet'
                    )
                    messages.success(request, f'Rs {amount} added to your balance.', extra_tags="amount-added-to-wallet")
                    return redirect('/profile/#profile-section')
                except ValueError as e:
                    messages.error(request, str(e))

        # Handling Address Update Form
        elif 'address_submit' in request.POST:
            form = AddBalanceForm()  # Keep balance form intact
            profile_form = ProfileForm(request.POST, instance=user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Address updated successfully.", extra_tags='address-updated')
                return redirect('/profile/#profile-section')
            else:
                 messages.error(request, "Please fill out the address field.",extra_tags='address-empty') 
    else: 
        form = AddBalanceForm()
        profile_form = ProfileForm(instance=user)

    context = {
        'user': user,
        'form': form,
        'profile_form': profile_form
    }
    return render(request, 'main_app/profile.html', context)

# def profile_view(request):
   
#     user = request.user
#     if request.method == 'POST':  
#             form = AddBalanceForm(request.POST)
#             if form.is_valid():
#                 amount = form.cleaned_data['amount']
#                 try:
#                     user.add_balance(amount)
#                     Transaction.objects.create(
#                         user=user,
#                         amount=amount,
#                         transaction_type='ADD',
#                         description='Added to wallet'
#                     )
#                     messages.success(request, f'Rs {amount} added to your balance',extra_tags="amount-added-to-wallet")
#                     return redirect('/profile/#profile-section')
#                 except ValueError as e:
#                     messages.error(request, str(e))
#     else:
#         form = AddBalanceForm()
    
#     context = {
#         'user': user,
#         'form': form
#     }
#     return render(request, 'main_app/profile.html', context)     

def see_more_view(request,vehicle_type):
    Rental.check_returns()
    
    vehicle_type = vehicle_type.strip()
    try:
        cars = Car.objects.filter(vehicle_type=vehicle_type)
        if not cars.exists():
            messages.info(request, "No cars found matching your search criteria.",extra_tags="no-cars-found")
            return redirect(reverse('home') + '#overview-fleets')
    except Exception as e:
        messages.error(request, f"Error while searching: {e}",extra_tags="search-error")
        return redirect(reverse('home') + '#overview-fleets')

    paginator = Paginator(cars, 9)
    page_obj = paginator.get_page(1)

    context = {
        'page_obj': page_obj,
        'total_pages': paginator.num_pages,
        'scroll_to_section': True,
        'current_page': 1
    }
    return render(request, "main_app/all-cars.html", context)

    



# THIS RENT CAR VIEW NEEDS TO BE CHANGED since now we are handling per hour rentals and starting day selection flexibility as well.
@login_required
def rent_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    if Rental.objects.filter(user=request.user, is_active=True).exists():
                messages.error(request, 'You already have an active rental',extra_tags="rental-already-active")
                return redirect(reverse('car_detail', args=[car.id]) + '#car-details-section')
    # even we have marked the unavailable cars as disbale to rent in the home view
    # but since backend must always validate the state, therefore we check again 
    if not car.available:
        messages.error(request, "This car is not available for rent.",extra_tags="rental-not-available")
        return redirect(reverse('car_detail', args=[car.id]) + '#car-details-section')

    if request.method == 'POST':
        
        user = request.user
        start_str = request.POST.get('start_datetime')
        end_str = request.POST.get('end_datetime')

        try:
            start_datetime = datetime.strptime(start_str, '%Y-%m-%dT%H:%M')
            end_datetime = datetime.strptime(end_str, '%Y-%m-%dT%H:%M')
            if is_naive(start_datetime) :
                start_datetime = make_aware(start_datetime)
            if is_naive(end_datetime):    
                end_datetime = make_aware(end_datetime)

            if start_datetime >= end_datetime:
                messages.error(request, "End time must be after start time.", extra_tags="rental-time-error")
                return redirect(reverse('car_detail', args=[car.id]) + '#car-details-section')
            if  start_datetime < timezone.now() or end_datetime <= timezone.now():
                messages.error(request, "Please select a valid time range.", extra_tags="rental-future-time-error")
                return redirect(reverse('car_detail', args=[car.id]) + '#car-details-section')
            total_rental_duration_seconds = (end_datetime - start_datetime).total_seconds()   
            rental_duration_days = total_rental_duration_seconds / (24 * 60 * 60) # into days
            integer_duration_days=int(rental_duration_days)
            remaining_seconds= total_rental_duration_seconds - (integer_duration_days*86400)
            rental_duration_minutes = int(remaining_seconds/(60))
        except (TypeError, ValueError):
            messages.error(request, "Invalid date and time input.", extra_tags="datetime-parse-error")
            return redirect(reverse('car_detail', args=[car.id]) + '#car-details-section') 

        
        total_cost = int(round(car.rent_per_day * rental_duration_days, 0))


        if not user.has_sufficient_balance(total_cost):
            messages.error(request, "Insufficient balance to rent this car.",extra_tags="rental-insufficient-balance")
            return redirect(reverse('car_detail', args=[car.id]) + '#car-details-section')

        # Deduct and create rental
        user.balance -= total_cost
        user.save()

        car.mark_unavailable()

        Rental.objects.create(
            user=user,
            car=car,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            total_cost=total_cost,
            is_active=True
        )

        Transaction.objects.create(
            user=request.user,
            amount=total_cost,
            transaction_type='PAYMENT',
            description=f'Rented {car.name} for {integer_duration_days} day(s) and {rental_duration_minutes} minutes(s) .'
        )
        if integer_duration_days!=0 and rental_duration_minutes!=0 :    
                messages.success(request, f'You have successfully rented {car.name} for {integer_duration_days} day(s) and {rental_duration_minutes} minutes(s) .',extra_tags="rental-success-minutes-days")
                return redirect(reverse('rental_history') + '#rental_history') 
        elif integer_duration_days!=0 and rental_duration_minutes==0 : 
            messages.success(request, f'You have successfully rented {car.name} for {integer_duration_days} day(s) .',extra_tags="rental-success-days")
            return redirect(reverse('rental_history') + '#rental_history')
        elif integer_duration_days==0 and rental_duration_minutes!=0 : 
            messages.success(request, f'You have successfully rented {car.name} for {rental_duration_minutes} minutes(s) .',extra_tags="rental-success-minutes")
            return redirect(reverse('rental_history') + '#rental_history')
        
    # below-- here is a safe fallback for non-POST requests like if the user directly visits the URL
    # or is the user refreshing the page without submitting the form
    return redirect('car_detail', car_id=car.id)

@login_required
def car_detail_view(request, car_id):
      
    if (request.user.address == '' or not request.user.address) and (not request.user.is_superuser):
        
        messages.error(request, "Please update your address so we can deliver rented cars to you!", extra_tags="address-required")
        return redirect(reverse('profile') + '#profile-section') 
    else:
        car = get_object_or_404(Car, id=car_id)
        context = {
            'car': car,
            'total_rentals':car.rentals.count(),
        }
        return render(request, 'main_app/car_detail.html', context)

# view to return a rented car if the rental period is not over
# when the rental period is over, the car will be automatically returned
@login_required
def return_car(request, rental_id):
    rental = get_object_or_404(Rental, id=rental_id, user=request.user)

    if not rental.is_active:
        messages.warning(request, "This car rental is already completed.")
        return redirect('profile',extra_tags="already-completed-rental")

    rental.is_active = False
    rental.returned_early = True
    rental.save()

    rental.car.mark_available()

    messages.success(request, f"You have successfully returned {rental.car.name}.",extra_tags="returned-by-user")
    return redirect(reverse('profile') + '#profile-section') 

# User Account Views


@login_required
def rental_history_view(request):
    rentals = Rental.objects.filter(user=request.user).order_by('-created_at')
    today = timezone.now()
    return render(request, 'main_app/rental_history.html', {
        'rentals': rentals,
        'today': today
    })

@login_required
def transaction_history(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-created_at') # this minus sign before "created_at" will sort the transactions in descending order
    return render(request, 'main_app/transaction_history.html', {'transactions': transactions})


def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if not name or not email or not message:
            return render(request, 'main_app/contact_us.html', {
                'error': "All fields are required."
            })

        # Save message
        ContactMessage.objects.create(name=name, email=email, message=message)

        # doing simple redirect with query param
        messages.success(request, " Thank you for contacting us. We'll get back to you soon!",extra_tags="msg-sent")
        return redirect(reverse('contact_us') + '?success=true#contact-form')
    user = request.user
    return render(request, 'main_app/contact_us.html',{ 'user':user })

def services_view(request):
    return render(request, 'main_app/services.html')



# Till here we had views--  for the normal users and for checking the admin 
 


# NOW FOR PDF GENERATION
def render_to_pdf(template_src, context_dict):
    """Helper function to generate PDF from HTML template"""
    # render_to_string : A Django shortcut that loads a template and renders it as a plain string (HTML string).
    template = render_to_string(template_src, context_dict)
    # io.BytesIO(): here below, initially you just instantiated a Python object that acts like a file in memory . It temporarily holds the PDF content.
    result = io.BytesIO()
    # result: This will store the final binary PDF data.
    pdf = pisa.pisaDocument(io.BytesIO(template.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('Error generating PDF', status=400)





# Now, below are the views for the admins


@login_required
@user_passes_test(is_admin)
def admin_contact_messages(request):
    if request.method == "POST":
        message_id = request.POST.get('message_id')
        reply = request.POST.get('reply')
        if message_id and reply:
            
            ContactMessage.objects.filter(id=message_id).delete()
        return redirect('admin_contact_messages')
    else:
        messages = ContactMessage.objects.all().order_by('-created_at') 
        return render(request, 'main_app/admin/admin_contact_messages.html', {'messages': messages})

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    total_cars = Car.objects.count()
    total_users = CustomUser.objects.filter(is_superuser=False).count()
    active_rentals = Rental.objects.filter(is_active=True).count()
    
    context = {
        'total_cars': total_cars,
        'total_users': total_users,
        'active_rentals': active_rentals,
    }
    
    return render(request, 'main_app/admin/admin_dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def admin_customer_report(request):
    users = CustomUser.objects.filter(is_superuser=False)
    customers_data = []

    for user in users:
        total_rentals = Rental.objects.filter(user=user).count()
        completed_rentals = Rental.objects.filter(user=user, is_active=False)
        current_rental = Rental.objects.filter(user=user, is_active=True).first()
        total_spent = sum(rental.total_cost for rental in completed_rentals)

        customers_data.append({
            'username': user.username,
            'full_name': f"{user.first_name} {user.last_name}",
            'total_rentals': total_rentals,
            'completed_rentals': completed_rentals.count(),
            'total_spent': total_spent,
            'current_car': current_rental.car.name if current_rental else "No current rental"
        })

    return render(request, 'main_app/admin/customer_report.html', {
        'customers_data': customers_data
    })

@login_required
@user_passes_test(is_admin)
def pdf_customer_report(request):
    """Generate PDF customer report"""
    users = CustomUser.objects.filter(is_superuser=False)
    user_data = []
    
    for user in users:
        active_rentals = Rental.objects.filter(user=user, is_active=True)
        past_rentals = Rental.objects.filter(user=user, is_active=False)
        
        user_data.append({
            'user': user,
            'active_rentals': active_rentals,
            'past_rentals': past_rentals,
            'total_spent': sum(rental.total_cost for rental in past_rentals)
        })
    
    context = {
        'user_data': user_data,
        'timestamp': timezone.now()
    }
    
    return render_to_pdf('main_app/admin/pdf_customer_report.html', context)



@login_required
@user_passes_test(is_admin)
def admin_reserved_cars_report(request):
    """Admin view for reserved cars report"""
    rentals = Rental.objects.filter(is_active=True).order_by('end_datetime')
    return render(request, 'main_app/admin/reserved_cars_report.html', {'rentals': rentals})

@login_required
@user_passes_test(is_admin)
def pdf_reserved_cars_report(request):
    """Generate PDF of currently reserved (active) cars"""
    reserved_cars = Car.objects.filter(available=False)
    active_reservations = []

    for car in reserved_cars:
        rental = Rental.objects.filter(car=car, is_active=True).select_related('user').first()
        if rental:
            active_reservations.append(rental)

    context = {
        'active_reservations': active_reservations,
        'total_active_reservations': len(active_reservations),
        'now': timezone.now()
    }

    return render_to_pdf('main_app/admin/pdf_reserved_cars_report.html', context)

@login_required
@user_passes_test(is_admin)
def admin_add_car(request):
    if request.method == 'POST':
        form = AdminCarForm(request.POST, request.FILES)  
        if form.is_valid():
            car = form.save(commit=False)
            car.added_by = request.user
            # Save a readable version of name
            if request.user.first_name and request.user.last_name:
                former_admin_name = f"Former Admin ({request.user.first_name} {request.user.last_name})".strip()
            else:
                former_admin_name = f"Former Admin ({request.user.username})"
            car.former_admin_name = former_admin_name
            car.save()
            messages.success(request, f'"{car.name}" added successfully!', extra_tags="car-added-successfully")
            return redirect(f"{reverse('admin_dashboard')}#admin-dashboard-section")
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AdminCarForm()
    return render(request, 'main_app/admin/add_car.html', {'form': form})

from django.http import FileResponse, Http404
import os
from django.conf import settings

def car_image(request, filename):
    filepath = os.path.join(settings.MEDIA_ROOT, 'car_images', filename)
    if os.path.exists(filepath):
        return FileResponse(open(filepath, 'rb'), content_type='image/jpeg')
    else:
        raise Http404()


@login_required
@user_passes_test(is_admin)
def admin_remove_cars(request):   #
    if request.method == 'POST':
        car_ids = request.POST.getlist('car_ids')
        deleted_count = 0

        for car_id in car_ids:
            car = get_object_or_404(Car, id=car_id)
            if car.available or not Rental.objects.filter(car=car, is_active=True).exists():
                car.delete()
                deleted_count += 1
            else:
                messages.warning(request, f'"{car.name}" is currently rented and was not removed.',extra_tags='car-can-not-be-removed')
                  
        if deleted_count:
            messages.success(request, f'{deleted_count} car(s) removed successfully.',extra_tags='car-removed-successfully')
        return redirect(reverse('remove_cars') + '#remove-cars-section')

    cars = Car.objects.all()
    return render(request, 'main_app/admin/admin_remove_cars.html', {'cars': cars})

