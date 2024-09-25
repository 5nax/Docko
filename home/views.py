from django.http import HttpResponse
from django.shortcuts import render


def index0(request):
   # Simulate storing user information in the session if not already stored
   if 'username' not in request.session:
      request.session['username'] = "Guest"

   # Access session data
   username = request.session.get('username', 'Guest')

   # Pass session data to the template
   context = {
      'username': username,
   }

   return render(request, 'home/homepage.html', context)


# Clearing session data
def clear_session(request):
    request.session.flush()  # Clear all session data
    return HttpResponse("Session data cleared.")
