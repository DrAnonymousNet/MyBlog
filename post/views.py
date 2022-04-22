from django.shortcuts import render, redirect, reverse, get_object_or_404, get_list_or_404
from .models import Post, Category, Comment, Author, Subscriber
from .forms import SubscriberForm, CommentForm, CategoryCreateForm, PostCreateForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .forms import ContactForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from datetime import datetime
from django.http import HttpResponseNotAllowed, HttpResponseForbidden, Http404, HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail, BadHeaderError
from django.template.defaultfilters import slugify

def recently_viewed(request, post_id):
    if "recently_viewed" in request.session:
        if post_id in request.session["recently_viewed"]:
            request.session["recently_viewed"].remove(post_id)
        recently_viewed_qs = Post.objects.filter(pk__in = request.session["recently_viewed"])

        request.session["recently_viewed"].insert(0, post_id)
        if len(request.session["recently_viewed"]) > 5:
            request.session["recently_viewed"].pop()

        request.session.modified = True


        return recently_viewed_qs
    else:
        request.session["recently_viewed"] = []
    request.session.modified =True
    return


def pagination(request, queryset, num_per_page):
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    paginator = Paginator(queryset, num_per_page)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)
    return (page_request_var, page, paginated_queryset)


def index(request):
    posts = Post.objects.filter(featured=True, date_posted__isnull=False)
    latests = Post.objects.filter(date_posted__isnull=False).order_by('-date_posted')[:3]
    form = SubscriberForm()
    page_request_var, page, paginated_queryset = pagination(request, posts, 3)
    if request.method == "POST":
        email = request.POST["email"]
        form = SubscriberForm()
        if form.is_valid():
            form.instance.email = email
            form.save()
    context = {
        "form": form,
        "latests": latests,
        "page": page,
        "queryset": paginated_queryset,
        "page_request_var": page_request_var,
    }
    return render(request, "index.html", context)


def blog(request):
    category = Category.objects.all()
    page_request_var, page, paginated_queryset = pagination(request, category, num_per_page=3)
    latests = Post.objects.filter(date_posted__isnull=False).order_by('-date_posted')[:3]
    context = {
        "category": category[:],
        "page": page,
        "queryset": paginated_queryset,
        "page_request_var": page_request_var,
        "latests": latests
    }
    return render(request, "blog.html", context)


def category_post(request, slug):
    category = Category.objects.all()
    cat = category.get(slug=slug)
    posts = Post.objects.filter(category=cat, date_posted__isnull=False)
    latests = Post.objects.filter(date_posted__isnull=False).order_by('-date_posted')[:3]
    page_request_var, page, paginated_queryset = pagination(request, posts, num_per_page=3)
    context = {
        "category": category[:],
        "cat": cat, "slug": slug,
        "queryset": paginated_queryset,
        "page": page,
        "page_request_var": page_request_var,
        "latests": latests

    }
    return render(request, "category.html", context)


def post(request, slug, id):
    post = Post.objects.get(id=id)
    category = Category.objects.all()
    cat = Category.objects.get(slug=slug)
    latests = Post.objects.filter(date_posted__isnull=False).order_by('-date_posted')[:3]
    context = {}
    if post.date_posted:
        next = post.get_next_by_id()
        previous = post.get_previous_by_id()
        context = {
            "previous": previous,
            "next": next,
        }

    comment = Comment.objects.filter(post=post)
    page_request_var, page, paginated_queryset = pagination(request, comment, num_per_page=10)
    form = CommentForm()
    recently_viewed_qs = recently_viewed(request, id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            author = Author.objects.get(author=request.user)
            form.instance.author = author
            form.instance.post = post
            form.save()
            form = CommentForm()

    cont = {"post": post,
            "category": category,
            "latests": latests,
            "cat": cat, "form": form,
            "queryset": paginated_queryset,
            "page": page, "slug": slug,
            "page_request_var": page_request_var,
            }
    for c in cont.keys():
        context[c] = cont[c]
    if recently_viewed_qs:
        context["recently_viewed_posts"] = recently_viewed_qs

    return render(request, "post.html", context)


def search(request):
    queryset = Post.objects.all()
    query = request.GET.get("search")
    if query:
        queryset = queryset.filter(
            Q(content__icontains=query) |
            Q(title__icontains=query) |
            Q(overview__icontains=query) |
            Q(category__title__icontains=query)
        ).distinct()

        context = {"queryset": queryset}
        return render(request, "search.html", context)
    return render(request, "search.html")



@login_required()
def post_create(request, slug):
    if not request.user.is_superuser:
        raise HttpResponseForbidden
    form = PostCreateForm()
    if request.method == "POST":
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            cat = Category.objects.get(slug=slug)
            form.instance.category = cat
            author = Author.objects.get(author=request.user)
            form.instance.author = author
            form.instance.date_posted = None
            form.instance.save()
            return redirect(reverse('post', kwargs={
                'slug': slug, 'id': form.instance.id
            }))

    context = {
        "form": form,
        "title": "Create",

    }
    return render(request, "post_create.html", context)


@login_required
def category_create(request):
    if not request.user.is_superuser:
        raise HttpResponseForbidden
    form = CategoryCreateForm()
    if request.method == "POST":

        form = CategoryCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.slug = slugify(form.instance.title)
            form.instance.save()
            return redirect(form.instance.get_absolute_url())
    context = {
        "form": form
    }
    return render(request, "category_create.html", context)

@login_required
def post_update(request, slug, id):
    post = get_object_or_404(Post, id=id)
    author = Author.objects.get(author=post.author.author)
    if request.user.is_superuser:
        form = PostCreateForm(request.POST or None, request.FILES or None, instance=post)
        if request.method == 'POST':
            if form.is_valid():
                form.instance.author = author
                form.instance.save()
                return redirect(form.instance.get_absolute_url())
        context = {
            "form": form,
            "title": 'Update',
            "slug": slug
        }
        return render(request, "post_create.html", context)
    else:
        raise Http404


def post_delete(request, slug, id):
    post = get_object_or_404(Post, id=id)
    if request.user.is_superuser:
        if request.method == "POST":
            post.delete()
            return redirect("category_post", slug=slug)

        context = {
            "slug": slug,
            "id": id,
            "post": post,
        }
        return render(request, "post_delete.html", context)
    else:
        raise Http404


def draft(request, slug):
    cat = get_object_or_404(Category, slug=slug)
    post_ = get_list_or_404(Post, date_posted__isnull=True, category=cat)
    page_request_var, page, paginated_queryset = pagination(request, post_, num_per_page=10)
    context = {
        "queryset": paginated_queryset,
        "cat": cat,
        "page": page,
        "page_request_var": page_request_var,
        "slug": slug,

    }
    return render(request, "draft.html", context)


@login_required()
def post_publish(request, slug, id):
    posts = get_object_or_404(Post, pk=id)
    if not request.user.is_superuser:
        raise Http404
    posts.date_posted = datetime.now()
    posts.save()
    return redirect("post", slug=slug, id=id)


def send_email(request):
    form = ContactForm()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data.get('message')
            from_email = form.cleaned_date.get('from_email')
            subject = form.cleaned_data.get('subject')
            if subject and message and from_email:
                try:
                    send_mail(subject, message, from_email, ['haryourdejijb@gmail.com'])
                except BadHeaderError:
                    return HttpResponse('Invalid header found')

                return redirect('/')
            else:
                return
    context = {
        'form': form
    }
    return render(request, 'contact.html', context=context)
