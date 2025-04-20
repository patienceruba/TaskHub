from django.contrib.auth import update_session_auth_hash,authenticate, login
from django.http import HttpResponseNotAllowed
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


def profile_edit(request):
    return render(request, "profile_edit/pro_edit.html")


@login_required
def person(request):
    user = request.user
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()

        messages.success(request, 'Profile updated successfully!')
        return redirect('dashboard')  # or any page you want

    return render(request, 'profile_edit/person.html')  # your template path




@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password', '').strip()
        new_password = request.POST.get('new_password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()

        if not request.user.check_password(current_password):
            messages.error(request, "The current password you entered is incorrect.")
        elif new_password != confirm_password:
            messages.error(request, "The new password and confirmation password do not match.")
        else:
            try:
                # Validate new password strength
                validate_password(new_password, user=request.user)
                
                # Save new password
                user = request.user
                user.set_password(new_password)
                user.save()

                # Keep user logged in
                update_session_auth_hash(request, user)

                messages.success(request, "Your password has been successfully updated.")
                return redirect('password_change_done')
            except ValidationError as e:
                for error in e:
                    messages.error(request, error)
    
    elif request.method != 'GET':
        return HttpResponseNotAllowed(['GET', 'POST'])

    return render(request, 'profile_edit/change_password.html')


from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def validate_password_done(request):
    return render(request, 'profile_edit/password_change_done.html')

