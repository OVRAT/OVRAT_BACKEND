# OVRAT_BACKEND
These are all backend modules for the OVRAT project structure


Sure, here's a markdown file for installing and configuring a Django Rest Framework project with SimpleJWT authentication using mkvirtualenv:

# Installing and Configuring Django Rest Framework Project with SimpleJWT Authentication

## Prerequisites
- Python 3 installed on your machine
- pip package manager installed on your machine
- virtualenvwrapper installed on your machine

## Installation

1. Install virtualenvwrapper:

```bash
pip install virtualenvwrapper
```

2. Add the following lines to your `~/.bashrc` or `~/.zshrc` file:

```bash
export WORKON_HOME=$HOME/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh
```

3. Create a new virtual environment:

```bash
mkvirtualenv myprojectenv
```

4. Activate the virtual environment:

```bash
workon myprojectenv
```

5. Install Django and Django Rest Framework:

```bash
pip install django
pip install djangorestframework
```

6. Install SimpleJWT:

```bash
pip install djangorestframework-simplejwt
```

## Configuration

1. Create a new Django project:

```bash
django-admin startproject myproject
```

2. Create a new Django app:

```bash
cd myproject
python manage.py startapp myapp
```

3. Add `'rest_framework'` and `'rest_framework_simplejwt'` to the `INSTALLED_APPS` list in `settings.py`:

```python
INSTALLED_APPS = [
    # ...
    'rest_framework',
    'rest_framework_simplejwt',
]
```

4. Configure SimpleJWT authentication in `settings.py`:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
}
```

5. Configure URL routing in `urls.py`:

```python
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # ...
]
```

6. Create a serializer in `serializers.py`:

```python
from rest_framework import serializers
from .models import MyModel

class MyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyModel
        fields = '__all__'
```

7. Create a view in `views.py`:

```python
from rest_framework import generics, permissions
from .models import MyModel
from .serializers import MyModelSerializer

class MyModelList(generics.ListCreateAPIView):
    queryset = MyModel.objects.all()
    serializer_class = MyModelSerializer
    permission_classes = [permissions.IsAuthenticated]
```

8. Configure URL routing for the view in `urls.py`:

```python
from django.urls import path
from .views import MyModelList

urlpatterns = [
    path('mymodel/', MyModelList.as_view()),
    # ...
]
```

9. Migrate your database:

```bash
python manage.py migrate
```

10. Run your server:

```bash
python manage.py runserver
```

That's it! You should now have a functioning Django Rest Framework project with SimpleJWT authentication.
