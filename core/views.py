from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.db.models import Q
from .models import Item, Report, Claim, Student, Category
from .forms import ItemForm, ReportForm, ClaimForm, StudentForm
from .forms import RegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import HttpResponse


def home(request):
    return render(request, 'home.html')


def items_list(request):
    q = request.GET.get('q', '')
    status = request.GET.get('status', '')
    items = Item.objects.all().order_by('-item_id')
    if q:
        items = items.filter(Q(name__icontains=q) | Q(description__icontains=q))
    if status:
        items = items.filter(status=status)
    categories = Category.objects.all()
    return render(request, 'items_list.html', {'items': items, 'q': q, 'status': status, 'categories': categories})


def item_detail(request, item_id):
    item = get_object_or_404(Item, item_id=item_id)
    return render(request, 'item_detail.html', {'item': item})


def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('items_list')
    else:
        form = ItemForm()
    return render(request, 'item_form.html', {'form': form})


def lost_items(request):
    items = Item.objects.filter(status='LOST').order_by('-item_id')
    return render(request, 'lost_items.html', {'items': items})


def found_items(request):
    items = Item.objects.filter(status='FOUND').order_by('-item_id')
    return render(request, 'found_items.html', {'items': items})


def unclaimed_found(request):
    items = Item.objects.filter(status='FOUND').exclude(claims__isnull=False).order_by('-item_id')
    return render(request, 'unclaimed_found.html', {'items': items})


def student_reports(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    reports = student.reports.all().order_by('-report_date')
    return render(request, 'student_reports.html', {'student': student, 'reports': reports})


def submit_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('items_list')
    else:
        form = ReportForm()
    return render(request, 'submit_report.html', {'form': form})


def submit_claim(request):
    if request.method == 'POST':
        form = ClaimForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('items_list')
    else:
        form = ClaimForm()
    return render(request, 'submit_claim.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # create linked Student profile
            name = form.cleaned_data.get('name')
            Student.objects.create(user=user, name=name, email=user.email)
            login(request, user)
            return redirect('profile')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def profile(request):
    user = request.user
    try:
        student = user.student_profile
    except Exception:
        student = None
    try:
        adminp = user.admin_profile
    except Exception:
        adminp = None
    return render(request, 'profile.html', {'user': user, 'student': student, 'adminp': adminp})


def students_crud(request):
    students = Student.objects.all()
    return render(request, 'students_list.html', {'students': students})


def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('students')
    else:
        form = StudentForm()
    return render(request, 'student_form.html', {'form': form})
