from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages

@login_required
def delete_user(request):
    if request.method == "POST":
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, "Your account has been deleted.")
        return redirect('home')
    return render(request, 'delete_account.html')
