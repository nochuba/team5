from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm
from django.http import HttpResponse
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})

def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})

def about(request):
 return render(request,'shop/about.html',{})


def contact(request):
 return render(request,'shop/contact.html',{})

def submit(request):
    name=request.GET['Name']
    print (name)
    message = Mail(
        from_email='from_email@example.com',
        to_emails='nochuba@unomaha.edu',
        subject=name,
        html_content='<strong>and easy to do anywhere, even with Python</strong>')
    try:
        sg = SendGridAPIClient('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')
        response = sg.send(message)
        if response.status_code == 202:
            print('email sent')
        else:
            print(response.status_code)
            print(response.body)
            print(response.headers)
    except Exception as e:
        print(str(e))
    return render(request, 'shop/contact.html', {})