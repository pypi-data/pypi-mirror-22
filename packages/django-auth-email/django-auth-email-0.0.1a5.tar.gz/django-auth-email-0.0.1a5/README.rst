Using
=====

``settings.py``::

    INSTALLED_APPS = [
        ...
        'django_auth_email',
        ...
    ]

And run command::

    ./manage.py makemigrations django_auth_email
    ./manage.py migrate

Will be create a table in the DB -- ``django_auth_email_option``. Model::

    class Option(models.Model):
        user = models.ForeignKey(User)
        code = models.CharField(max_length=56)
        expiry = models.DateTimeField()

Sign-in/up::

    >>> from django_auth_email.models import DEAMng
    >>> auth = DEAMng()
    >>> code = auth.set_code(form.instance.email)
    >>> print(code)
    c0fca3619e2a0692a0f7bc79388cc51b5c805b22f5718e342bafd986


Authorization::

    >>> check = DEAMng()
    >>> if check.is_valid(code):
    >>>     check.login(request)

