from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import user_passes_test, login_required, user_passes_test
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.core.mail import send_mail, EmailMessage
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from todo.models import UserProfile

User = get_user_model()

@user_passes_test(lambda u: u.is_superuser, login_url='no_permission')
def register_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('f-name')
        last_name = request.POST.get('l-name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        #add role.
        is_staff = request.POST.get('is_staff') == 'true'
        is_superuser = request.POST.get('is_superuser') == 'true'
        job_role = request.POST['job_role']
        profile_picture = request.FILES.get('profile_picture')  # Handling the image upload

        # Password match validation
        if password != password1:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        # Username uniqueness validation
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        # Email uniqueness validation
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already in use.")
            return redirect('register')

        # Create inactive user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.is_active = False
        user.job_role = job_role
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save()

        # Create UserProfile instance
        user_profile = UserProfile(user=user, profile_picture=profile_picture)
        user_profile.save()


        # Prepare activation email
        current_site = get_current_site(request)
        mail_subject = 'Activate your account.'
        message = render_to_string('todo/acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })

        # Send email as HTML
        email_message = EmailMessage(
            mail_subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
        )
        email_message.content_subtype = 'html' 

        try:
            email_message.send(fail_silently=False)
        except Exception as e:
            messages.error(request, "There was an error sending the activation email. Please try again later.")
            user.delete()  
            return redirect('register')


        messages.success(request, 'Please confirm your email address to complete the registration.')
        return redirect('login')

    return render(request, 'todo/register.html')



from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    #messages.success(request, "You have been logged out successfully.")
    return redirect('login')





# Password Reset Request
def password_reset_request(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user = User.objects.filter(email=email).first()
        if user:
            subject = "Password Reset Request"
            context = {
                "email": user.email,
                "domain": request.get_host(),
                "protocol": "http",
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": default_token_generator.make_token(user),
            }
            email_content = render_to_string("todo/password_reset_email.html", context)
            email_message = EmailMessage(
                subject=subject,
                body=email_content,
                from_email="admin@example.com",
                to=[user.email],
            )
            email_message.content_subtype = "html"
            email_message.send()
        messages.success(request, "If an account exists with the provided email, a reset link has been sent.")
        return redirect("password_reset_done")
    return render(request, "todo/password_reset_request.html")


def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError):
        user = None

    if user and default_token_generator.check_token(user, token):
        if request.method == "POST":
            password = request.POST.get("password")
            password1 = request.POST.get("password1")
            if password == password1:
                user.set_password(password)
                user.save()
                messages.success(request, "Your password has been reset successfully.")
                return redirect("login")
            else:
                messages.error(request, "Passwords do not match.")
        return render(request, "todo/password_reset_confirm.html")
    else:
        messages.error(request, "The reset link is invalid or has expired.")
        return redirect("password_reset_request")

def password_reset_done(request):
    return render(request, "todo/password_reset_done.html")



def send_activation_email(request, user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    activation_link = request.build_absolute_uri(
        reverse('activate', kwargs={'uidb64': uid, 'token': token})
    )

    subject = 'Activate your account'
    message = f'Hi {user.username},please activate your account by clicking this link:\n{activation_link}'

    send_mail(subject, message, 'rubayitap7@gmail.com', [user.email])
    #return render(request, "todo/sentActivationEmail.html")






def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse(f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Email Confirmed</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        background-color: #f4f4f4;
                        text-align: center;
                        padding-top: 100px;
                    }}
                    .popup {{
                        background-color: #4CAF50;
                        color: white;
                        padding: 20px;
                        border-radius: 8px;
                        width: 400px;
                        margin: auto;
                        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
                        opacity: 0;
                        transform: translateY(-20px);
                        transition: all 0.5s ease;
                    }}
                    .popup.show {{
                        opacity: 1;
                        transform: translateY(0);
                    }}
                </style>
            </head>
            <body>
                <div id="popup" class="popup">
                    ✅ Thank you for confirming your email.<br>
                    Your username is <strong>{user.username}</strong>.<br>
                    You can now log in.
                </div>

                <script>
                    document.addEventListener("DOMContentLoaded", function() {{
                        var popup = document.getElementById("popup");

                        // Show popup after small delay
                        setTimeout(function() {{
                            popup.classList.add("show");
                        }}, 100);

                        // Hide popup and redirect after 5 seconds
                        setTimeout(function() {{
                            popup.classList.remove("show");
                            window.location.href = '/login/'; // change to your login URL name or path
                        }}, 5000);
                    }});
                </script>
            </body>
            </html>
            """)


    else:
        return HttpResponse('Activation link is invalid or expired.')
