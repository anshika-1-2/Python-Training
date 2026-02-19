from django.shortcuts import render
from .forms import GeeksForm

def home(request):
    """
    This function renders a home page with a GeeksForm.
    
    If a POST request is made, it validates the form and saves it to the database.
    
    Finally, it renders the home.html template with the form as a variable.
    """
    form = GeeksForm()

    if request.method == 'POST':
        form = GeeksForm(request.POST)
        if form.is_valid():
            form.save()
            form = GeeksForm()

    return render(request, 'home.html', {'form': form})
