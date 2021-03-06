from .models import Post
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

content_type = ContentType.objects.get_for_model(Post)
permission = Permission.objects.create(
    codename="can_publish",
    name='Can Publish Post',
    content_type=content_type,)
