from django.http import HttpResponse, FileResponse
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from io import BytesIO
from xhtml2pdf import pisa
from .forms import PersonalInfoForm, MarksEntryForm
from django.contrib.auth.decorators import login_required
from .models import MarksEntry, AdminUser  # Add AdminUser to the imports
from django.contrib.auth import login, authenticate, get_backends
from .forms import AdminSignupForm, AdminLoginForm
from django.core.mail import send_mail
from django.conf import settings  # Import settings
import random
from django.contrib.admin.views.decorators import staff_member_required
from .forms import StudentInfoForm

# Remove or update the home view
# def home(request):
#     return HttpResponse("Welcome to the Counseling App!")

def dashboard(request):
    return HttpResponse("Welcome to the Dashboard!")

@login_required
def personal_info_view(request):
    if request.method == 'POST':
        form = PersonalInfoForm(request.POST)
        if form.is_valid():
            personal_info = form.save(commit=False)
            personal_info.user = request.user
            personal_info.save()
            return redirect('marks_entry')
    else:
        form = PersonalInfoForm()
    return render(request, 'counseling_app/personal_info_form.html', {'form': form})

@login_required
def marks_entry_view(request):
    if request.method == 'POST':
        form = MarksEntryForm(request.POST)
        if form.is_valid():
            marks_entry = form.save(commit=False)
            marks_entry.user = request.user
            marks_entry.save()
            return redirect('dashboard')  # Redirect to a dashboard or success page
    else:
        form = MarksEntryForm()
    return render(request, 'counseling_app/marks_entry_form.html', {'form': form})

def upload_payment(request):
    if request.method == 'POST':
        # Handle payment upload logic
        pass
    return render(request, 'counseling_app/upload_payment.html')

def generate_offer_letter(request):
    html = render_to_string('counseling_app/offer_letter.html', {'user': request.user})
    response = BytesIO()
    pisa.CreatePDF(html, dest=response)
    response.seek(0)
    return FileResponse(response, as_attachment=True, filename='offer_letter.pdf')

def admin_signup(request):
    if request.method == 'POST':
        form = AdminSignupForm(request.POST)
        if form.is_valid():
            admin_user = form.save(commit=False)
            admin_user.is_admin = True
            admin_user.save()
            # Explicitly set the backend
            backend = get_backends()[0]  # Use the first backend in the list
            admin_user.backend = f"{backend.__module__}.{backend.__class__.__name__}"
            login(request, admin_user)
            return redirect('admin_dashboard')
    else:
        form = AdminSignupForm()
    return render(request, 'counseling_app/admin_signup.html', {'form': form})

def admin_login(request):
    if request.method == 'POST':
        if 'otp' in request.POST:  # Step 2: Verify OTP
            entered_otp = request.POST.get('otp')
            if entered_otp == request.session.get('admin_otp'):
                user_id = request.session.get('admin_user_id')
                user = AdminUser.objects.get(id=user_id)
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')  # Specify backend
                del request.session['admin_otp']  # Clear OTP from session
                del request.session['admin_user_id']  # Clear user ID from session
                return redirect('admin_dashboard')
            else:
                return render(request, 'counseling_app/admin_login.html', {
                    'error_message': 'Invalid OTP. Please try again.',
                    'otp_step': True
                })

        form = AdminLoginForm(data=request.POST)
        if form.is_valid():  # Step 1: Authenticate user
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if hasattr(user, 'is_admin') and user.is_admin:  # Ensure user is an admin
                    # Generate a 4-digit OTP
                    otp = str(random.randint(1000, 9999))
                    request.session['admin_otp'] = otp
                    request.session['admin_user_id'] = user.id

                    # Send OTP to the user's email
                    send_mail(
                        'Your Admin Login OTP',
                        f'Your OTP for admin login is: {otp}',
                        settings.DEFAULT_FROM_EMAIL,
                        [user.email],
                        fail_silently=False,
                    )

                    return render(request, 'counseling_app/admin_login.html', {
                        'otp_step': True,
                        'message': 'An OTP has been sent to your email. Please enter it below.'
                    })
                else:
                    return render(request, 'counseling_app/admin_login.html', {
                        'form': form,
                        'error_message': 'You are not authorized to log in as an admin.'
                    })
            else:
                return render(request, 'counseling_app/admin_login.html', {
                    'form': form,
                    'error_message': 'Invalid username or password. Please try again.'
                })
    else:
        form = AdminLoginForm()
    error_message = request.GET.get('error')
    return render(request, 'counseling_app/admin_login.html', {
        'form': form,
        'error_message': error_message
    })

@login_required
def admin_dashboard(request):
    user_role = request.user.role  # Get the role of the logged-in user
    context = {
        'user_role': user_role,
    }
    return render(request, 'counseling_app/admin_dashboard.html', context)

@staff_member_required
def manage_admins(request):
    admins = AdminUser.objects.all()  # Fetch all registered admins
    if request.method == 'POST':
        admin_id = request.POST.get('admin_id')
        AdminUser.objects.filter(id=admin_id).delete()  # Delete the selected admin
        return redirect('manage_admins')  # Refresh the page after deletion
    return render(request, 'counseling_app/manage_admins.html', {'admins': admins})

@staff_member_required
def monitor_admins(request):
    admins = AdminUser.objects.all()  # Fetch all registered admins
    admin_count = admins.count()  # Count the number of admins
    return render(request, 'counseling_app/monitor_admins.html', {
        'admins': admins,
        'admin_count': admin_count,
    })

def landing_page(request):
    return render(request, 'counseling_app/landing_page.html')

@login_required
def submit_student_info(request):
    if request.method == 'POST':
        form = StudentInfoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')  # Redirect to the admin dashboard after submission
    else:
        form = StudentInfoForm()
    return render(request, 'counseling_app/submit_student_info.html', {'form': form})
