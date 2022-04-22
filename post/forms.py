from .models import Subscriber, Comment, Post, Category
from django import forms
from tinymce import TinyMCE


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ["email"]
        labels = {"email": ""}




class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'name': "usercomment",
        'id': "usercomment",
        'placeholder': "Type your comment",
        'class': "form-control", }))

    class Meta:
        model = Comment
        fields = ["content"]
        labels = {"content": ""}


class PostCreateForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCEWidget(attrs={
        'required': False, 'cols': 30, 'rows': 10}
    ))

    class Meta:
        model = Post
        # fields = ["thumbnail", "title" , "overview", "content", "featured",]
        exclude = ['category', 'date_posted', "author"]


class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["thumbnail", "title", "overview"]


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.Textarea()
    from_email = forms.EmailField()
