from django.shortcuts import render
from .models import Product
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .forms import ProductForm  
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 5)  # Show 5 posts per page

    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {'page_obj': page_obj}
    return render(request, 'index.html', context)

def product_list(request):
    """
    List view of all products.

    This view renders a list of all product objects in a template, passing the
    list of products as a variable to the template.

    :param request: The current request
    :return: The rendered template
    """
    products = Product.objects.all()
    return render(request, 'myapp/index.html', {'products': products})

def product_detail(request, pk):
    """
    Detail view of a product given its primary key.

    This view renders a single product object in a template, passing the
    product object as a variable to the template.

    :param request: The current request
    :param pk: The primary key of the product to display
    :return: The rendered template
    """
    product = Product.objects.get(pk=pk)
    return render(request, 'myapp/index2.html', {'product': product})


def edit_product(request, pk):
    """Edit a product given its primary key.

    If the request is a POST, the product will be updated and the user
    will be redirected to the product list page. If the request is a GET,
    the product will be rendered in a template to edit its details."""
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'myapp/edit.html', {'form': form})

def delete_product(request, pk):
    """Delete a product given its primary key.

    If the request is a POST, the product will be deleted and the user
    will be redirected to the product list page. If the request is a GET,
    the product will be rendered in a template to confirm deletion.

    :param request: The current request
    :param pk: The primary key of the product to delete
    :return: The rendered template or the redirect response
    """
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'myapp/delete.html', {'product': product})


def home(request):
    """
    Return a simple "Hello, World!" message.
    """
    return HttpResponse('Hello, World!')