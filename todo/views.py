from django.shortcuts import render, redirect,get_object_or_404
from .models import  RecordRow,  TaskDone, PDFDocument, UserProfile,SubTask
from slide_profile.models import Image
from django.utils import timezone
from datetime import datetime
from django.contrib import messages
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test,login_required
from django.core.mail import EmailMessage
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.db.models.signals import post_save
from assigntask.models import AssignedTask
from teams.models import TeamMember
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
@login_required
@user_passes_test(lambda user: user.is_staff)
def home(request):
    task = RecordRow.objects.filter(user=request.user)
    context = {"tasks":task}
    return render(request, "todo/index.html", context)

@login_required
@user_passes_test(lambda user: user.is_staff)
def addRecord(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        start_date_str = request.POST.get('starting-date')
        end_date_str = request.POST.get('ending-date')
        image_file = request.FILES.get('image')  # File upload handling

        if title and description:
            try:
                # Parse dates with defaults for missing values
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d') if start_date_str else timezone.now()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d') if end_date_str else None

                # If no image is uploaded, handle it (optional default image or None)
                if not image_file:
                    # Set a default image path if necessary (ensure your model supports it)
                    image_file = None  # or "/static/images/default.jpg"

                # Save record
                RecordRow.objects.create(
                    user=request.user,  # Ensure user is authenticated
                    title=title,
                    description=description,
                    start_date=start_date,
                    end_date=end_date,
                    image=image_file
                )
                return redirect("home")  # Redirect on success
            except ValueError:
                error = "Invalid date format. Please use YYYY-MM-DD."
        else:
            error = "Title and description are required."

        # Render the form with an error message
        return render(request, "todo/addrecord.html", {"error": error})

    return render(request, "todo/addrecord.html")


def deleteRow(request, pk):
    item = get_object_or_404(RecordRow, pk=pk)
    if request.method == "POST":
        item.delete()
        messages.success(request, "The record was deleted successfully.")
        return redirect("home")  # Replace "home" with the name of the view or URL to redirect to after deletion
    return render(request, "todo/delete.html", {"item": item})


def updateRecord(request, pk):
    record = get_object_or_404(RecordRow, pk=pk)

    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        start_date_str = request.POST.get('starting-date')
        end_date_str = request.POST.get('ending-date')
        image_file = request.FILES.get('image')

        # Ensure that title and description are provided
        if title and description:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d') if start_date_str else record.start_date
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d') if end_date_str else record.end_date

                # Update the record
                record.title = title
                record.description = description
                record.start_date = start_date
                record.end_date = end_date
                record.image=image_file
                record.save()

                messages.success(request, "The record was updated successfully.")
                return redirect("home")  # Redirect to home or any other page after update

            except ValueError:
                messages.error(request, "Invalid date format. Please use YYYY-MM-DD.")
                return render(request, "todo/update.html", {"record": record, "error": "Invalid date format."})

        messages.error(request, "Title and description are required.")
        return render(request, "todo/update.html", {"record": record, "error": "Title and description are required."})

    return render(request, "todo/update.html", {"record": record})



def search(request):
    query = request.GET.get('search', '')  # Get the search query from the GET request
    redirect_from = request.GET.get('redirect', '')  # Check where the search came from
    results = []

    if query:
        # Filter records based on the search query (e.g., search by title or description)
        results = RecordRow.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))  # Case-insensitive search

    # Redirect based on the 'redirect' parameter
    if redirect_from == 'regular':
        return render(request, 'todo/searchforregular.html', {'results': results, 'query': query})
    else:
        return render(request, 'todo/search.html', {'results': results, 'query': query})


def calendar(request):
    # Get tasks assigned to the currently logged-in user
    assigned_tasks = AssignedTask.objects.filter(user=request.user)

    # Prepare event list with necessary data
    event_list = [
        {
            "date": task.task.start_date.strftime('%Y-%m-%d') if task.task.start_date else None,
            "end_date": task.task.end_date.strftime('%Y-%m-%d') if task.task.end_date else None,
            "title": task.task.title,
        }
        for task in assigned_tasks
        if task.task.start_date
    ]

    return render(request, "todo/calendar.html", {
        "events": json.dumps(event_list, cls=DjangoJSONEncoder),
        "has_events": bool(event_list)
    })


def upload_pdf(request):
    if request.method == 'POST' and request.FILES['pdf']:
        title = request.POST.get('title')
        pdf_file = request.FILES['pdf']
        
        # Save the PDF file
        fs = FileSystemStorage()
        filename = fs.save(pdf_file.name, pdf_file)
        uploaded_file_url = fs.url(filename)

        # Save the document info to the database
        PDFDocument.objects.create(title=title, pdf=uploaded_file_url)

        return redirect('pdf_list')
    
    return render(request, 'upload_pdf.html')

def pdf_list(request):
    pdfs = PDFDocument.objects.all()
    return render(request, 'pdf_list.html', {'pdfs': pdfs})


@login_required
def task_done_view(request):
    # Retrieve all completed tasks for the logged-in user
    image = RecordRow.objects.all()
    task_done_list = TaskDone.objects.filter(user=request.user).order_by('-completed_at')
    context = {
        'task_done_list': task_done_list,"image":image
    }
    return render(request, 'todo/task_done.html', context)


def today_view(request):
    today = timezone.localdate()  # Local date without time
    events_today = RecordRow.objects.filter(start_date__date=today)
    return render(request, 'todo/today.html', {'events_today': events_today})


def dashboard_view(request):
    total_tasks = RecordRow.objects.filter(user=request.user).count()+AssignedTask.objects.filter(user=request.user).count()
    task_done_list = TaskDone.objects.filter(user=request.user).order_by('-completed_at')
    total_tasks_completed = task_done_list.count()  # Count completed tasks
    assigned_tasks = AssignedTask.objects.filter(user=request.user).count()
    teams = TeamMember.objects.filter(user=request.user).count()

    context = {
        'task_done_list': task_done_list,
        'total_tasks': total_tasks,
        'tasks_completed': total_tasks_completed, # Pass count to template
        'assigned_tasks':assigned_tasks,
        'teams':teams,
    }
    return render(request, 'todo/dashboard.html', context)


"""def login_view(request):
    user = None  # Initialize user variable

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Or any other page after login

        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')  # Stay on the login page

    return render(request, 'todo/login.html')"""

def login_view(request):
    try:
        error_message = None  # Initialize error message
        background_images = Image.objects.all()
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("dashboard")  # Redirect to home or dashboard page
            else:
                error_message = "Invalid username or password"

        return render(request, "todo/login.html", {"error_message": error_message, 
                                                "background_images":background_images})
    except(TypeError):
        message = "username and password"


@login_required
def update_profile_picture(request):
    if request.method == 'POST' and request.FILES.get('profile_picture'):
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        user_profile.profile_picture = request.FILES['profile_picture']
        user_profile.save()
        return redirect('dashboard')
    return render(request, 'todo/user_profile.html')


@login_required
def upload_task(request):
    if request.method == 'POST':
        # Create a new task
        task_name = request.POST.get('task_name')
        task = RecordRow.objects.create(name=task_name, user=request.user)
        request.session['new_task'] = True  # Set a session flag for the new task

        return redirect('task_list')  # Redirect to task list or wherever you want

    return render(request, 'event.html')


@csrf_exempt
def reset_task_notification(request):
    # Clear the session flag after the task has been seen
    if 'new_task' in request.session:
        del request.session['new_task']
    return JsonResponse({'status': 'success'})

@login_required
def task_detail(request, pk):
    # Retrieve the task based on the primary key (pk) or show 404 if not found
    record = get_object_or_404(RecordRow, pk=pk)
    is_owner = RecordRow.objects.filter(user= request.user)

    # Pass the record (task) and its related subtasks to the template
    context = {
        'record': record,
        'is_owner':is_owner
    }

    return render(request, 'todo/task_detail.html', context)



def team_member_ship(request):
    teams = TeamMember.objects.filter(user = request.user)
    return render(request, "teams/teamMembership.html", {"teams":teams})


def slider_view(request):
    images = Image.objects.all()  # Assuming you have an Image model
    return render(request, 'slide_template.html', {'images': images})


@login_required
def create_subtask(request, record_id):
    record = get_object_or_404(RecordRow, id=record_id)

    if request.method == 'POST':
        title = request.POST.get('title')
        comment = request.POST.get('comment', '')

        if title:  # Basic validation
            SubTask.objects.create(
                record=record,
                title=title,
                comment=comment,
                created=timezone.now()
            )
            return redirect('success')

    return render(request, 'todo/add_subtask.html', {'record': record})

@login_required
def task_dashboard(request):
    if request.user.is_staff:
        tasks = RecordRow.objects.filter(user=request.user)  
    else:
        tasks = None

    assigned_tasks = AssignedTask.objects.filter(user=request.user)  
    task_done_list = [task.title for task in RecordRow.objects.filter(user=request.user)]  

    now = timezone.now()

    context = {
        'tasks': tasks,
        'assigned_tasks': assigned_tasks,
        'task_done_list': task_done_list,
        'now': now
    }

    return render(request, 'todo/total_task.html', context)


def success(request):
    return render(request, "todo/success.html")


"""@login_required
def task_progress(request):
    # Get tasks for the logged-in user
    tasks = RecordRow.objects.filter(user=request.user)

    # Add a 'complete' attribute to each task based on progress
    for task in tasks:
        task.done = task.progress == 100 # If progress >= 100, mark as complete
    
    # Pass tasks to the template
    return render(request, 'todo/index.html', {'tasks': tasks})
"""

def task_user_progress_view(request, task_id):
    tasks = get_object_or_404(RecordRow, id=task_id)
    progress = tasks.get_user_progress(request.user)
    view_progress = RecordRow.objects.filter(id__in=[p.record_id for p in progress])
    view_progress+=progress
    return render(request, 'todo/index.html', {
        'task': tasks,
        'progress': progress,
    })