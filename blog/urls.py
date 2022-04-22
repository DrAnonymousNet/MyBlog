from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from post.views import index, post, post_create, blog, post_delete, category_post, category_create, \
    search, post_update, draft, post_publish,send_email
from users.views import login_view, register, logout_view, reset_password, email_verify

from . import settings

extra_patterns = [
    path('', blog, name="blog"),
    path("create/", category_create, name="category_create"),
    path("<slug:slug>/create/", post_create, name="post_create"),
    path("<slug:slug>/", category_post, name="category_post"),
    path("<slug:slug>/draft", draft, name="draft"),
    path("<slug:slug>/<int:id>/", post, name="post"),
    path("<slug:slug>/<int:id>/update", post_update, name="post_update"),
    path("<slug:slug>/<int:id>/delete", post_delete, name="post_delete"),
    path("<slug:slug>/<int:id>/publish", post_publish, name="post_publish"),

]

urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),
    path('', index, name="index"),
    path('blog/', include(extra_patterns)),
    path('search/', search, name="search"),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register, name='register'),
    path('contact/', send_email, name= 'contact'),
    path('reset-password/',reset_password, name="reset_password"),
    path('email-verify/', email_verify, name="email_verify"),
    path('tinymce/', include('tinymce.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
