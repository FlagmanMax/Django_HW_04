import logging
import random
from datetime import timedelta

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils.datetime_safe import datetime

from seminar2.models import Order, User, Product
from .forms import *
from seminar3.models import Author, Post, Comment

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, filename='logger.log', filemode='a', format='%(levelname)s %(message)s')


def seminar4(request):
    logger.info(f'{request} request received')
    return render(request, 'seminar4.html')


def form1(request):
    if request.method == 'POST':
        form = Form1(request.POST)
        if form.is_valid():
            quant = int(form.data['quant'])
            match form.data['games']:
                case "1":
                    return heads_tails(request, quant)
                case "2":
                    return dice(request, quant)
                case "3":
                    return rand(request, quant)
    else:
        form = Form1()
    return render(request, 'form1.html', {'form': form})


def form2(request):
    if request.method == 'POST':
        form = Form2(request.POST)
        if form.is_valid():
            name = form.data['name']
            email = form.data['email']
            author = Author(name=name,
                            email=email)
            author.save()
            # messages.add_message(request, messages.SUCCESS, 'Автор добавлен')
            return render(request, 'form2.html', {'answer': "Автор добавлен!"})
    else:
        form = Form2()
    return render(request, 'form2.html', {'form': form})


def form3(request):
    if request.method == 'POST':
        form = Form3(request.POST)
        if form.is_valid():
            title = form.data['title']
            content = form.data['content']
            author_id = form.data['author']
            author = Author.objects.filter(id=author_id).first()
            post = Post(title=title,
                        content=content,
                        author=author,
                        showed=1,
                        published=True)
            post.save()
            return render(request, 'form3.html', {'answer': "Статья добавлена"})
    else:
        form = Form3()
    return render(request, 'form3.html', {'form': form})


def form4(request):
    if request.method == 'POST':
        form = Form4(request.POST)
        if form.is_valid():
            comment = form.data['comment']
            post_id = form.data['post']
            post = Post.objects.filter(id=post_id).first()
            author = post.author
            comment = Comment(author=author,
                              post=post,
                              comment=comment)
            comment.save()
            return render(request, 'form4.html', {'answer': "Комментарий добавлен"})
    else:
        form = Form4()
    return render(request, 'form4.html', {'form': form})


def form5(request, arg):
    if request.method == 'POST':
        form = Form5(request.POST)
        if form.is_valid():
            comment = form.data['comment']
            post = Post.objects.filter(id=arg).first()
            author = post.author
            comment = Comment(author=author,
                              post=post,
                              comment=comment)
            post.showed += 1
            post.save()
            comment.save()
            return render(request, 'form5.html', {'answer': "Принято", 'form': form})
    else:
        form = Form5()
        post = Post.objects.filter(pk=arg).first()
        return render(request, 'form5.html', {'form': form, 'post': post})


def form6(request):
    if request.method == 'POST':
        form = Form5(request.POST)
        if form.is_valid():
            name = form.data['name']
            description = form.data['description']
            price = form.data['price']
            prod_quant = form.data['prod_quant']
            product_id = form.data['product']
            product = Product.objects.filter(id=product_id).first()
            product.name = name
            product.description = description
            product.price = price
            product.prod_quant = prod_quant
            product.save()
            return render(request, 'form2.html', {'answer': "it's ok!"})
    else:
        form = Form5()
    return render(request, 'form2.html', {'form': form})


def product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    products = Product.objects.all()
    return render(request, 'detail.html', {'product': product, 'products': products})


def products(request):
    logger.info(f'{request} request received')
    products = Product.objects.all()
    return render(request, 'catalog.html', {'products': products})


def prod_edit(request):
    logger.info(f'{request} request received')
    if request.method == 'POST':
        form = Form6(request.POST, request.FILES)
        if form.is_valid():
            name = form.data['name']
            description = form.data['description']
            price = form.data['price']
            prod_quant = form.data['prod_quant']
            product_id = form.data['product']
            product = Product.objects.filter(id=product_id).first()
            img = request.FILES['img']
            fs = FileSystemStorage()
            fs.save(img.name, img)
            product.img = img.name
            product.name = name
            product.description = description
            product.price = price
            product.prod_quant = prod_quant
            product.save()
            return render(request, 'prod_edit.html', {'answer': "Обновлено!"})
    else:
        form = Form6()
    return render(request, 'prod_edit.html', {'form': form})


def upload_image(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            fs = FileSystemStorage()
            fs.save(image.name, image)
            return render(request, 'upload_image.html', {'answer': "Uploaded!"})
    else:
        form = ImageForm()
    return render(request, 'upload_image.html', {'form': form})


def united(request, n):
    context = {'ht': [],
               'd': [],
               'r': []}
    while n > 0:
        context['ht'].append(random.choice(['Орел', 'Решка']))
        context['d'].append(random.randint(1, 6))
        context['r'].append(random.randint(1, 100))
        n -= 1
    return render(request, 'united.html', context)


def heads_tails(request, n):
    context = {'res': []}
    while n > 0:
        context['res'].append(random.choice(['Орел', 'Решка']))
        n -= 1
    return render(request, 'playya.html', context)


def dice(request, n):
    context = {'res': []}
    while n > 0:
        context['res'].append(random.randint(1, 6))
        n -= 1
    return render(request, 'playya.html', context)


def rand(request, n):
    context = {'res': []}
    while n > 0:
        context['res'].append(random.randint(1, 100))
        n -= 1
    return render(request, 'playya.html', context)


def home(request):
    context = {'home': 'Homepage'}
    logger.info(f'{request} request received')
    return render(request, 'homepage.html', context)


def about(request):
    context = {'about': 'About me'}
    logger.info(f'{request} request received')
    return render(request, 'about.html', context)


def author_posts(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    posts = Post.objects.filter(author=author).order_by('-id')[:10]
    return render(request, 'author_posts.html', {'author': author, 'posts': posts})


def post_full(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.showed += 1
    post.save()
    return render(request, 'post_full.html', {'post': post, 'counter': post.showed})


def post_comm(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = Comment.objects.filter(post=post).all()
    post.showed += 1
    post.save()
    return render(request, 'post_comment.html', {'post': post, 'comments': comments, 'counter': post.showed})


def basket(request, user_id):
    products = []
    user = User.objects.filter(pk=user_id).first()
    orders = Order.objects.filter(customer=user).all()
    for order in orders:
        products.append(order.products.all())
    products.reverse()
    return render(request, 'basket.html', {'user': user, 'orders': orders, 'products': products})


def sorted_basket(request, user_id, days_ago):
    products = []
    now = datetime.now()
    before = now - timedelta(days=days_ago)
    user = User.objects.filter(pk=user_id).first()
    orders = Order.objects.filter(customer=user, date_ordered__range=(before, now)).all()
    for order in orders:
        products.append(order.products.all())
    products.reverse()
    return render(request, 'sorted_basket.html', {'user': user, 'orders': orders, 'products': products})
