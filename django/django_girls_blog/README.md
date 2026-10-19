# Django Girls Blog

A Windows-friendly local project following the Django Girls chapters: Deploy preparation, Django URLs, Django views, HTML, Django ORM, dynamic data in templates, Django templates, CSS, and template extending. It uses the tutorial's `Post` model and SQLite database. Your student registration project is separate and unchanged.


## Run locally on Windows

Open PowerShell in this folder, then create and activate a virtual environment and install Django:

```powershell
py -m venv myvenv
.\myvenv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If PowerShell blocks activation, use Command Prompt with `myvenv\Scripts\activate.bat`, or run `myvenv\Scripts\python.exe` directly for the commands below.

Create the database tables and an admin account, then start the development server:

```powershell
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open <http://127.0.0.1:8000/> for the blog or <http://127.0.0.1:8000/admin/> to sign in and create posts. Django commands are entered in PowerShell; ORM examples are entered after `python manage.py shell`.

The post list loads published posts from the database and passes them to the template as `posts`. `post_list.html` loops over that QuerySet and uses `{{ post.title }}`, `{{ post.text|linebreaksbr }}`, and `{{ post.published_date }}`. It extends `base.html`; shared page structure and the Bootstrap, Lobster font, and app CSS links live in the base template. App styles are in `blog/static/css/blog.css`.

## Django ORM practice

In the Django shell, use your own admin username in place of `YOUR_USERNAME`:

```python
from blog.models import Post
from django.contrib.auth.models import User
from django.utils import timezone

me = User.objects.get(username="YOUR_USERNAME")
Post.objects.all()
post = Post.objects.create(author=me, title="Sample title", text="Test")
Post.objects.filter(author=me)
Post.objects.filter(title__contains="title")
Post.objects.filter(published_date__lte=timezone.now())
post.publish()
Post.objects.order_by("created_date")
Post.objects.order_by("-created_date")
Post.objects.filter(published_date__lte=timezone.now()).order_by("published_date")
```

## Deploy chapter status

The local preparation from the Deploy chapter is represented by `.gitignore` and `requirements.txt`. Publishing requires a GitHub account/repository and a PythonAnywhere account/API token. This workspace project has not been pushed or deployed. When you are ready to deploy, follow the tutorial's GitHub and PythonAnywhere steps using your own accounts, and replace its `my-first-blog` repository URL with this project's repository URL.

The `SECRET_KEY` in `mysite/settings.py` is for local learning only. Do not use this development configuration for a public production deployment.
