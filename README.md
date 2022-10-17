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


Outline

#Introduction

Structural Pattern Matching is a new python feature introduced in Python 3.10 in the [PEP 634](https://peps.python.org/pep-0634/) specification.

The feature verifies that the value of an expression ( called the *subject* ) matches a given structure called the `pattern`.

Among several use cases, this new feature could be used to:

- match the structure of a data structure as shown below:
```
match book_data:
    case {"title":title,"author":author}:
        Book(title, author)
    case {"title":title, "author":author, "isbn":isbn}:
        Book(title, author,isbn)
```

- used to discover the type, and shape of an object.
This use case could be achieved with a chain of `if`, `elif` and `else` used alongside functions like `isinstance`, `hasattr`, and other similar object type checking functions as shown below:

```python
if isinstance(book_data, list) and len(book_data) == 2 :
    title, author = book_data
    isbn = None
elif isinstance(book_data, list) and len(book_data) == 3:
    title, author, isbn = book_data
```

The code snippet above could be written in a more readable syntax with the new structural pattern matching feature as shown below:

```
match book_data:
    case title, author:
        isbn = None
    case title, author, isbn:
        pass
```

The new feature also leverages the python `sequence unpacking assignment` ( Introduced in [PEP 3132](https://peps.python.org/pep-3132) ) to match patterns in sequences.

``` 
match book_data:
    case {"title":title,**kwargs}:
        Book(title, **kwargs)
```
We will explore and explain several other use cases of this new feature in subsequent sections of this tutorial.


# Prerequisite

To follow up with this tutorial, ensure you have a decent level of python knowledge and have python 3.10 Installed.

If you don't have python 3.10 installed, you can [download](https://www.python.org/downloads/release/python-3106/) from the official website for your respective operating system:

## Objectives

In this tutorial, I will explain different use-cases of this new feature with the use of examples in the context of web development.

We will explore this new feature to match the structure and attributes of the response from the [Jsonplaceholder](https://jsonplaceholder.typicode.com/posts
) dummy blog post API.

By the end of this tutorial, you should have enough idea about this new feature and you should be able to use it in your next python project or incorporate it into a codebase you are working on.

> Ensure everyone working on the codebase upgrade their python to 3.10 so that you won't have the “It works on my machine kind of scenario :)”

# Anatomy of the  match-case syntax

```
match <expression>:
    case <pattern 1> [<if guard>]:
        <block to execute if pattern 1 matches>
    case <pattern n> [<if guard>]:
        <code block to execute if pattern n matches>
```
The `match` keyword is a `soft keyword` whose expression evaluates to produce a value called the *subject*. The *subject* then matches against the pattern of each `case` clause. The code block of the case clause is executed based on a first-to-match rule.

After there is a match and the python interpreter executes the block of code of the associated case clause, the python interpreter ignores the remaining `case clauses` just like in the `if-elif` clauses.

> Soft keywords are python built-in keywords that are not reserved. They can be used as variable names outside the block or context where they serve as a keyword. The `match` keyword can be used as a normal variable name outside the `match-case` block.

This might look similar to the `switch-case` statement for those with Javascript or C background. However, this is very different from the `switch-case` statement.

One of the ways this syntax differs from the `switch-case` syntax is that it does not require an explicit `break` statement after a pattern is matched. it also has a lot of powerful features that can not be found in the `switch-case` statement in other languages. We will explore these features later on. 

The `guard` is an optional `if condition` in a `case clause`. It's evaluated after a `pattern` matches the subject. The block of code associated with the case clause will only execute if the `guard` evaluates to `True`. Otherwise, the next pattern will be compared until there is another match with a `guard` that evaluates to True ( if we specified a `guard` ).

# Patterns

The structure of the *subject* matches against the `patterns`.

The values of the *subject* can also be captured and `bound` to a variable that we specified in the pattern.

Binding variables to values is a little different from assigning variables to values. The value captured in the pattern can not be set as a value to an attribute of an object in the `case clause` via the dotted syntax:
```
object.attribute = value 
```
However, any variable bindings outlive the scope of the respective case or match statements just like a normal variable.

There are several classes of structural patterns that can be matched and they include the following:

# Literal Pattern

The literal pattern matches only the same literal value. They include a *subject* with one of the basic data types ( Integer, Float, String and Boolean ) matched against a pattern of the same data type.

The behavior of the `match-case` statement in this case, is similar to the `switch-case` statement present in languages like Javascript.

The `match-case` statement compares the value of the *subject* with the literal values specified as patterns in the case clauses.

This comparison is done via the equality ( == ) sign for all the literal patterns except for `True`, `False`, and `None` which are compared via python's `is` keyword.

All forms of strings ( Byte, Raw, Triple quoted string ) can be specified as a pattern except the `F string`. 

However, based on the consistent rule of equality ( == ) in python, literal patterns like 1 and 1.0 will match as well as all forms of python equality comparison that evaluate to `True`.

Let's take a look at an example of matching a literal integer value:

```
import requests

def main(response):
   status_code = response.status_code #200
   match status_code:
       case 200:
           print("The response is OK")
       case 400:
           print("The response is Bad")

response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
main(response)
```

Output:

```
>>> import pattern_matching
The response is OK
```

In the case above, python compares the *subject* which is the response status code to the literal integer pattern we specified in the case clauses ( 200 and 400 ). After the status code matches the *subject*, the interpreter executes the code under the case clause. 

We can match a string like the encoding of the response as shown below:
```
import requests

def main(response):
   encoding = response.encoding
   match encoding:
       case "utf-8":
           print("The encoding is utf-8")
       case "utf-16":
           print("The encoding is utf-16")

response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
main(response)
```

We have an output below in the shell:
```
>>> import pattern_matching
The encoding is utf-8
```

Similarly, We can match a `bool` value:

```
import requests

def main(response):
    check = response.ok
   match check:
       case True:
           print("The response is ok")
       case False:
           print("The response is not ok")

response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
main(response)
```

We will get an output as shown below:
```
>>> import pattern_matching
The response is ok

```
To match a floating value or a `None` keyword, you can specify an expression that evaluates to a either of them in the `match` statement to compare against them as a literal value in the case clauses.

# Captured Pattern 

We can capture and bind the some or all the values of the *subject* to a variable.

`Capture patterns` are names that capture values that matches the structure in a variable. These variables outlive the scope of their respective case clauses and they can be accessed outside the block of the `match-case` statement.

Binding of values to variables is similar to how arguments capture the values of parameters in a function.

```
def main(response):
   values = [response.status_code, response.encoding, response.json()]
   match values:
       case [status_code, encoding]:
           print("The first pattern matches the subject")
           print(status_code, encoding)
       case [status_code, encoding, response_data] if staus_code <= 399:
           print("The second pattern matches the subject")
           print(status_code, encoding, response_data)
        …
```

In the snippet above, the *subject* is a sequence with three elements, therefore only a pattern with this same structure can match the *subject* successfully.

The `pattern` in the first `case` matches only two of the three elements in the *subject*,  as a result, the match will not be successful.

The pattern in the second `case` matches the structure of the *subject* and the `guard` evaluates to `True`. In addition to that, the interpreter binds the names we specified in the pattern to the values of the elements in the sequence.

When we run the code above, we will get an output as shown below:

[capturedpattern]()

As shown in the output above, Only the second pattern matches the subject and the bound values were printed in the case block. 

# AS Pattern

The capture pattern we discussed above matches and binds values to the names we specified in the pattern. However, it does not give regard to the structure of the individual elements ( in the sequence like the case above ).

The `As pattern` allows us to specify a pattern to match the *subject* or individual elements in a *subject* against and also a name to bind the value of the subject to.

The `AS pattern` uses the `as` keyword to bind a variable to the value after the structure of the subject matches the pattern.

Let us modify the snippet above to match the number of elements in the sequence and the datatypes of the individual elements.

```
    …
def main(response):
   values = [response.status_code, response.encoding, response.json()]
   match values:
       case [int() as status_code, str() as encoding]:
           print("The first pattern matches the subject")
           print(f"status_code:{status_code}, encoding:{encoding}")
          
       case [int() as status_code, str() as encoding, str() as response_data]:
           print("The second pattern matches the subject")
           print(f"status_code:{status_code}, encoding:{encoding}, response_data:{response_data}")

       case [int() as status_code, str() as encoding, dict() as response_data]:
           print("The Third pattern matches the subject")
           print(f"status_code:{status_code}, encoding:{encoding}, response_data:{response_data}")
    …
```

The first pattern fails because it does not match the number of elements in the sequence, but matches the datatype of the `status_code` and the `encoding` which are integer and string respectively.

The second pattern matches the number of the elements but fails to match the data type of the `response_data` which is a `dict` datatype.

The third pattern matches the number of elements and the datatypes of each element.

When we run the code above, we will get the output below:

![aspattern]()

The pattern above can be shortened by passing the variable name as arguments into the datatype class as shown below:

case [int(status_code), str(encoding)]:

# Wildcard pattern

The wildcard pattern denoted by an underscore ( `_` ) matches any structure but doesn't bind the value. It is often used as a fallback pattern if no pattern matches the structure of the subject like in the code below:

```
    …
def main(response):
   status_code = response.status_code
   match status_code:
       case 300:
           print("The response is 300")
       case 400:
           print("The response is 400")
       case _:
           print("No pattern matches the response status !")
    …
```

When you run the code above, you will get an output as shown below:

![wildcardpattern]()

The status code of the response is expected to be 200, hence none of the *literal patterns* matched the status code. Since the *wildcard pattern* ( `_` ) matches any structure, the interpreter will execute the block of code in the last case clause.

We could match the example in the *captured pattern* above with the *wildcard pattern* if we only wanted to bind the value of the `encoding` as shown below:

```
def main(response):
   values = [response.status_code, response.encoding, response.json()]
   match values:
       case [ _, encoding]:
           print("The first pattern matches the subject")
           print(encoding)
       case [ _ , encoding, _ ]:
           print("The second pattern matches the subject")
           print(encoding)
```
The *wildcard pattern* will match the status code and response data.

An attempt to access the value of the wildcard pattern ( `_` ) will give a `NameError` as shown below:

[NameErrorWildcard]()


#OR Pattern

The OR pattern allows you to combine ‘structurally equivalent’ alternatives into a new pattern, i.e. several patterns can share a common handler. If any of an OR pattern’s subpatterns matches the subject, the entire OR pattern succeeds. - [PEP635](https://peps.python.org/pep-0635/#or-patterns)

The OR pattern is specified with a `pipe` ( | ) character in between the structurally equivalent alternatives. 

Once one of the patterns that are separated by the *or character* matches the structure of the *subject*, the pattern matching is successful and the interpreter executes the code under the respective case clause .

The example below checks the encoding scheme of the response by matching the *subject* against patterns with alternatives.

```
             …
def main(response):
   encoding = response.encoding
   match encoding:
       case "utf-8" | "utf-16":
           print("The response was encoded with utf encoding scheme")
       case "base64" | "ascii":
           print("The response was encoded with either a binary encoding scheme or ASCII")
       case _:
           print("No pattern matches the response encoding !")
            …
```
The first pattern will match if the encoding scheme is either `utf-8` or `utf-16`.The second pattern will match if the encoding scheme is either `base64` or `ascii`.

If we run the code above, we will get the output below:

![orpattern]()

Like any other patterns, we can bind the value of the pattern that matches the structure of the *subject* to a variable as shown below: 
```
        …

def main(response):
   encoding = response.encoding
   match encoding:
       case "utf-8" | "utf-16" as encoding:
           print(f"The response was encoded with {encoding}")
       case "base64" | "ascii" as encoding:
           print(f"The response was encoded with {encoding}")
       case _:
           print("No pattern matches the response encoding !")
        …
```

This gives output as shown below:
![aspattern2]()


# Value Pattern

Value patterns come in the form of accessing attributes of an object. Python matches the subject against the value of the attribute that we accessed in the pattern.

This is similar to the *capture pattern*, however the structural pattern matching specification adopted a rule that any dotted name (i.e., attribute access) is to be interpreted as a *value pattern*.


```

from http import HTTPStatus
import requests

def main(response):
   match (response.status_code, response.json()):
       case (HTTPStatus.OK.value, body):
           print(f"The response is OK")
       case (HTTPStatus.BAD_REQUEST.value | HTTPStatus.NOT_FOUND.value, _):
           print(f"Bad request or Not found")
       case _:
           print("No pattern matches the response status code !")


response = requests.get("https://jsonplaceholder.typicode.com/posts/0")  #new
main(response)
```


In the example above:
- we requested for an article with an `id` of `0` which returns a status code of `404 Not Found`.
- we specified the *subject* as a tuple of the response status code and the response json data.
- the pattern in each case clause is a tuple whose first element is an attribute access.

The *subject* is matched against the value the attribute access evaluates to rather than setting the *subject* as a value to the attribute.

The first case pattern evaluates to:
```
case (200, body)
```

The second case pattern evaluates to:
```
case (400 | 404, _)
```
The evaluation of the second pattern contains a *literal pattern*, an *or pattern* and the *wildcard pattern*..

Since the response status code is 404, the second pattern matches and the interpreter executes code block associated with it as shown in the output below:

![valuepattern]()

# Sequence Pattern

Sequence patterns are patterns with comma-separated values and they could be opened or enclosed by `( … )`  or  `[ … ]`.

Depending on whether the sequence pattern contains a wildcard sub-pattern or not, it could be a fixed-length sequence pattern or a variable-length sequence pattern.

The fixed-length sequence pattern has to match the subject length-wise and element-wise. The pattern fails if the length of the subject sequence is not equal to the length of the sequence in the pattern.

The variable-length sequence pattern uses the python iterable packing and unpacking syntax ( the star character `*` ) to pack a slice of the sequence into a variable. The variable-length sequence can contain at most one starred sub-pattern.

As in iterable unpacking, the specification does not distinguish between ‘tuple’ and ‘list’ notation . `[1, 2, 3]` is equivalent to `(1, 2, 3)` as well as `1, 2, 3`.  If we need to match the sequence against its type, we need to wrap the sequence with the datatype class i.e list([1,2,3]) or tuple(1,2,3)

Only the following are recognized as a sequence:

array.array
collections.deque
list
memoryview
range
Tuple

```
import requests

def main(response):
   match response.json():
       case [last_post]:
           print(last_post)
       case first_post, *_, last_post:
           print("first_post: ", first_post)
           print("last_post:", last_post)
       case _:
           print("No pattern matches the response status code !")


response = requests.get("https://jsonplaceholder.typicode.com/posts")
main(response)
```

The code above gives the output shown below:
![sequence pattern]()


The code snippet above requests for a list of posts from the `/posts` endpoint which returned 100 list of posts.

The first pattern failed because the length of the sequence pattern does not match the length of the sequence in the subject.

The second pattern binds the value of the first element in the sequence of the *subject* to the `first_post` pattern and binds the last element in the `last_post` variable. The elements in between are packed and bound into the wildcard pattern, Hence the second pattern matches the structure of the *subject*.

# Mapping Pattern

The mapping pattern allows the us to match and extract the values of keys from a mapping data structures. The values are matched against a given subpattern.
The keys of the mapping pattern must be literals or value patterns while the value could be any of the types of patterns we have discussed earlier.

As an example, we will match the data of the json response of the `posts/1` endpoint. The response data has the following structure:
```
{
“userId”:1,
“id”:1,
title:’sunt aut facere…',
“body”:'quia et suscipit\nsuscipit recusandae…’
}
```

## Matching keys

The patterns in the key could be literal or value patterns. All or some of the keys in the mapping data structure could be specified. If only some of the keys are specified, other keys are ignored and the pattern will match if a key that matches such a pattern is in the mapping data structure that we specified as the *subject*.

```
Import requests

def main(response):
   post_data = response.json()
   match post_data:
        case {"user_id":1}:
            print("Pattern 1 matched")
        case {"userId":1, "postId":1}:
            print("pattern 2 matched")
        case {"userId":1, "id":1}:
            print("pattern 3 matched")
        case _:
            print("No pattern matched")
    
response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
main(response)
```
In the example above:
- the first pattern failed because `user_id` is not a key in the response data ( the *subject* ). 
- the second pattern failed because the *subject* does not have a `post_id` key.
- the third pattern matches because both of the keys we specified are present in the *subject*.


## Matching values

The patterns in the value could be any form of pattern we have discussed so far. 

```
                  ...
def main(response):
   post_data = response.json()
   match post_data:
        case {"userId":2}:
            print("Pattern 1 matched")
        case {"userId":user_id, "id":post_id} if user_id < post_id:
            print("pattern 2 matched")
        case {"userId":user_id, "id":1|2|3} if user_id >= 1:
            print("pattern 3 matched")
        case _:
            print("No pattern matched")
                     ...
```
In the code above:
- the first pattern will fail because the literal pattern `2` does not match the value of the `userId` key in the subject.
- the second pattern will fail because the guard clause will fail since the `user_id` is not less than the `post_id`.
- the pattern will pass because all the keys we specified are present, the `guard` will evaluate to `True` and the `or pattern` will pass.

## Key-Value packing

When we match some part of the key-value pairs in a mapping as shown above, the interpreter ignores the other key-value pairs. if we need them,We can leverage the python `sequence packing` to match and bind several keys and values in the *subject* to a variable as shown below:

```
            ...

def main(response):
   post_data = response.json()
   match post_data:
        case {"user_id":1, **others}:
            print("Pattern 1 matched ", others)
        case {"userId":user_id, "id":post_id, **others} if user_id < post_id:
            print("pattern 2 matched", others)
        case {"userId":user_id, "id":1|2|3, **others} if "title" in others.keys():
            print("pattern 3 matched")
            print(others)
        case _:
            print("No pattern matched")
            ...
```

When we execute the code above, we will get the following output.

![machingpattern]()

The third pattern matched.

The value that the interpreter binds to the `others` variable is a mapping data structure that has all attributes of a normal mapping data structure, hence we can construct a `guard` checking if a key is present in it. 


# Class Pattern
Class patterns checks whether a given subject is an instance of a specific class, if there are no arguments present, the pattern matches once the subject is an instance of the class specified in the pattern.

```
class Post:
    def __init__(self, userId, id, title, body):
        self.userId = userId
        self.title = title
        self.body = body
        self.post_id = id

class Post2:
    pass
```

We have a two classes:
- The `Post` class with attributes that matched with the keys in the single post json response.
- The `Post2` class with no attribute

## Maching an instance of a class

```
import requests

def main(response):
    post = Post(**response.json())
    match post:
        case Post2():
            print("Pattern 1")
        case Post():
            print("Pattern 2")
        case _:
            print("No pattern matches the post class !")


response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
main(response)
```
In the code above, the `match-case` statement behaves like the `isinstance` function.

we created an instance of the `Post` class with the json response and match the post instance against the two classes we specifed. If the subject is an instance of the class we specified as pattern in the case clause, the pattern matching will be successful. Hence in the case above, the second pattern matches.

## Matching Keyword Arguments

The patterns above only match if the *subject* is an instance of the `pattern`.In addition to matching class instances, we can specify keyword arguments in the pattern to match against the keyword arguments in the *subject*. 
If keywords arguments are present in the class pattern:
- they are looked up as an attribute on the subject.
- if the attribute lookup raise an `AttributeError`, the pattern fails.
- if not, the sub pattern associated with the keyword pattern are matched against the attribute value of the subject, if it succeeds, the whole pattern matching succeeds, otherwise it fails.

```
def main(response):
    post = Post(**response.json())
    match post:
        case Post(post_id = 4 | 5):
            print("Pattern 1")
        case Post(post_id = 1 | 2, userId= id) if id >= 2:
            print("Pattern 2")
        case Post(post_id = 1 | 2, userId= id) if id == 1:
            print("Pattern 3")
        case _:
            print("No pattern matches the post class !")

                        ...
```    

In the case above:
- The first pattern above matches the class of the subject but the `post_id` keyword argument fails because the `post_id` is neither 4 nor 5 hence the overall pattern fails.
- The second pattern matches the class, the `post_id` but the `guard` clause failed because the `userId` is less than 2
- The third pattern matches the class, the `post_id` and `guard`, hence the whole pattern matching succeeds.

## Matching positional arguments

If we switch the arguments in the patterns above as shown below:

```
                    ...
def main(response):
    post = Post(**response.json())
    match post:
        case Post(4 | 5):
            print("Pattern 1")
        case Post(1 | 2, id) if id >= 2:
            print("Pattern 2")
        case Post(1 | 2, id) if id == 1:
            print("Pattern 3")
        case _:
            print("No pattern matches the response status code !")
                       ...
```

We will get the following error:
![classpatternerror]()


The python classes don’t have a natural ordering of their attributes, we need to specify the order of the arrangement of these attributes via the `__match_args__` attribute before we can use the positional arguments in the patterns.
```
class Post:
    __match_args__ = ("post_id", "userId", "title", "body")
    def __init__(self, userId, id, title, body):
        self.userId = userId
        self.title = title
        self.body = body
        self.post_id = id
```
The `__match_args__` allows us to order the attributes base on our preference.

In the case above, the first argument in the pattern will match against the equivalent first value in the `__match__args`.
The`post_id` will be the first positional argument, the `userId` will the second while the `title` and `body` will be the third and fourth positional arguments respectively 
The positions As specifie in the `__

if positional patterns are present in a class, they are converted to keyword patterns and the keyword arguments have to be specified in the the pattern else we will get an error as shown below:

![positionalargumenterror]()

 classes don’t have a natural ordering of their attributes so you’re required to use explicit names in your pattern to match with their attribute


# Conclusion

In this tutorial:
- we explored the python *structural pattern matching* feature that was introduce in the python 3.10.
- We explaned what different terms in the context of this feature meant.
- We also introduced different kind of patterns that can be matched.

This new feature is powerful and it will allow you to write a more readable syntax with little line of codes. The use case of this feature is not limted to the context of web development. It can be used in any context that involves matching the structure of values.
