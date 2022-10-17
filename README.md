# MyBlog
A Blog Web app built with Django and Template from bootstapious.com.

## Images


![Screenshot from 2022-05-09 12-09-52](https://user-images.githubusercontent.com/64500446/167460541-a32094a2-2810-4fe8-a0ff-9cd5c0ef400b.png)

![Screenshot from 2022-05-09 13-04-12](https://user-images.githubusercontent.com/64500446/167461013-9384f615-fbed-4ef9-863a-6e98428f8076.png)


![Screenshot from 2022-05-09 12-55-49](https://user-images.githubusercontent.com/64500446/167460643-d83d7df0-3de9-4322-b4ce-f28d5993e03a.png)
![Screenshot from 2022-05-09 12-57-17](https://user-images.githubusercontent.com/64500446/167460756-5df9a58e-ffaa-4748-8cbd-db9aa1991044.png)



## LINK
Live at http://ahmadnuggets.pythonanywhere.com/


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

6. Editor

## Known Bug

1. The Email Verification Fails sometimes
2.  You have to manually add the superuser to the author list in the `admin.py` file
