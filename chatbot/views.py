from django.shortcuts import render
from .forms import UserInputForm
from .suggest_specialist import suggest_specialist

def chatbot(request):
    context = {}
    if request.method == "POST":
        form = UserInputForm(request.POST)
        if form.is_valid():
            user_input = form.cleaned_data["user_input"]
            suggested_specialist = suggest_specialist(user_input)
            context["suggested_specialist"] = suggested_specialist
    else:
        form = UserInputForm()

    context["form"] = form
    return render(request, "chatbot.html", context)