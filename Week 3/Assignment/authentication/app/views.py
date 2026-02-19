from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import RegisterForm, CommentForm
from .models import Comment

def register(request):
    """
    View that renders a registration form. If the form is valid, a new User
    is created with the given username, email, and password. The user
    is then redirected to the login page.
    """
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            return redirect('login')

    return render(request, 'register.html', {'form': form})


@login_required
def home(request):
    """
    View that renders the home page for a logged in user.
    """
    
    return render(request, 'home.html')


@login_required
def comments(request):
    
    """
    View that renders a form for creating a comment and displays all comments.
    The form is validated and the comment is saved to the database.
    The user is redirected back to the comments page after submitting a comment.
    """
    form = CommentForm()
    comments = Comment.objects.all()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('comments')

    return render(request, 'comments.html', {
        'form': form,
        'comments': comments
    })
