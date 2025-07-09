from django.http import HttpResponse, FileResponse
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from io import BytesIO
from xhtml2pdf import pisa
from .forms import PersonalInfoForm, MarksEntryForm
from django.contrib.auth.decorators import login_required
from .models import MarksEntry
from django.contrib.auth import login, authenticate, get_backends
from .forms import AdminSignupForm, AdminLoginForm

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
        form = AdminLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_admin:
                login(request, user)
                return redirect('admin_dashboard')
    else:
        form = AdminLoginForm()
    error_message = request.GET.get('error')
    return render(request, 'counseling_app/admin_login.html', {'form': form, 'error_message': error_message})

@login_required
def admin_dashboard(request):
    user_role = request.user.role  # Get the role of the logged-in user
    context = {
        'user_role': user_role,
    }
    return render(request, 'counseling_app/admin_dashboard.html', context)

def landing_page(request):
    return render(request, 'counseling_app/landing_page.html')
