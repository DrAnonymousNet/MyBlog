# MyBlog
A Blog Web app built with Django and Template from bootstapious.com.

# LINK
[My blog is hosted here](ahmadnuggets.pythonanywhere.com)


## Installation

1. Create a virtual environment [creating a virtual environment(link)]

2. In your terminal, install all the required library for the project using the ``` pip install -r requirements.txt```

3. Run `python manage.py makemigrations` and `python manage.py migrate` to create the database for our Installed app.

4. Run `python manage.py createsuperuser` to create a super user.

5. Fire up the development server with `python manage.py runserver` and check for errors. Hopefully, there is none.

6. After installation, Create a handful number of dummy posts from the admin website.
7. Open the `blog/settings.py` and add your gmail in the `EMAIL_HOST_USER` variable and your password in `EMAIL_HOST_USER_PASSWORD`

## Features

1. Authentication System ( Log in, Log out, Forget Password, Reset Password, Email Verification)

2. Post Creation, Deletion, Update (Only Superuser)

3. Comment Posting

4. Unique Post view count

5. User specific recently viewed post

## Known Bug

1. The Email Verification Fails sometimes
2.  You have to manually add the superuser to the author list in the `admin.py` file


