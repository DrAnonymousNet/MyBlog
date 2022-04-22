from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.urls import reverse
from tinymce import HTMLField
from PIL import Image


class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    profile = models.ImageField(default="user.jpg", upload_to="profile_pics")

    def __str__(self):
        return str(self.author.username)



class Category(models.Model):
    title = models.CharField(max_length=50)
    thumbnail = models.ImageField()
    overview = models.CharField(max_length=200,
                                default="Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod "
                                        "tempor incididunt ut labore")
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        super(Category, self).save(*args, **kwargs)
        img = Image.open(self.thumbnail.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.thumbnail.path)



    def get_absolute_url(self):
        return reverse("category_post", kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=30)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = HTMLField()
    date_posted = models.DateTimeField(null=True)
    thumbnail = models.ImageField()
    overview = models.TextField()
    featured = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        ordering = ["date_posted"]

    def get_comment_count(self):
        return self.comment_set.count()

    def get_next_by_id(self):
        obj = list(Post.objects.filter(category__slug=self.category.slug, date_posted__isnull=False))
        curr = Post.objects.get(id=self.id)
        try:
            next_ = obj[obj.index(curr) + 1]
            return next_
        except IndexError:
            return

    def get_previous_by_id(self):
        obj = list(Post.objects.filter(category__slug=self.category.slug, date_posted__isnull=False))
        curr = Post.objects.get(id=self.id)
        ind = obj.index(curr) - 1
        previous = obj[ind]
        if ind < 0:
            return
        return previous

    def get_absolute_url(self):
        return reverse('post', kwargs={'slug': self.category.slug, 'id': self.id})

    def __str__(self):
        return self.title

class Comment(models.Model):
    content = models.TextField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.content


class Subscriber(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email
