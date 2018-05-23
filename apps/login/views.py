from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
import bcrypt
from apps.login.models import *


# Create your views here.
def index(request):
    if "user_uniq" in request.session:
        return redirect("/login/success")

    return render(request, "login/login.html")


def logout(request):
    if request.method == "POST":
        request.session.clear()
        return redirect("/login")

    return redirect("/login/success")


def success(request):
    if not "user_uniq" in request.session:
        return redirect("/login")
    else:
        hashed_uniq_id = request.session["user_uniq"]
        #print("\n", "%" * 40)

        result = User.objects.filter(user_uniq = hashed_uniq_id).first()

        if result:
            return render(request, "login/success.html", { "user": result } )

    return redirect("/login")


def check(request):
    if "user_uniq" in request.session:
        return redirect("/login/success")

    if request.method == "POST":
        email = request.POST["email"]

        result = User.objects.filter(email = email).first()
        # print("POST", request.POST)

        if result:
            if bcrypt.checkpw(request.POST["passcode"].encode(), result.passcode.encode()):
                request.session.clear()
                request.session["user_uniq"] = result.user_uniq

                messages.success(request, "Welcome back!")

                return redirect("/login/success")
            else:
                request.session["email_login"] = request.POST["email"]
                messages.error(request, "You can not login to the website!")
                return redirect("/login")
        else:
            messages.error(request, "You can not login to the website!")
            return redirect("/login")

    return redirect("/login")


def register(request):
    if "user_uniq" in request.session:
        return redirect("/login/success")

    first_name = request.POST["first_name"].strip()
    last_name = request.POST["last_name"].strip()
    email = request.POST["email"].strip()
    birth_date = request.POST["birth_date"]
    passcode = request.POST["passcode"].strip()

    if request.method == "POST":
        errors = User.objects.record_validator(request.POST)

        if len(errors):
            # Return errors to template
            for key, value in errors.items():
                messages.add_message(request, level = 40, message = value, extra_tags = key)
                request.session["first_name"] = first_name
                request.session["last_name"] = last_name
                request.session["email"] = email
                request.session["birth_date"] = birth_date

            return redirect("/login")
        else:
            # Create new user
            hashed_pass = bcrypt.hashpw(passcode.encode(), bcrypt.gensalt())

            rec = User.objects.create(first_name = first_name, last_name = last_name, email = email, passcode = hashed_pass, birth_date = birth_date)

            if rec.user_id > 0:
                # Create user_uniq field and save it back to the table
                uniq_id = str(rec.user_id) + "_" + rec.created_at.strftime("%Y-%m-%d_%H-%M-%S-%f")

                hashed_uniq_id = bcrypt.hashpw(uniq_id.encode(), bcrypt.gensalt()).decode("utf-8")

                rec.user_uniq = hashed_uniq_id
                rec.save()

                request.session.clear()
                request.session["user_uniq"] = rec.user_uniq
                messages.success(request, "You registration was successfull!")
            else:
                messages.add_message(request, level = 40, message = "Something went wrong! Record didn't save.", extra_tags = 'error')
                return redirect("/login")

    return redirect("/login/success")
