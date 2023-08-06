[![Build Status](https://travis-ci.org/wejhink/django-mailcss.png?branch=master)](https://travis-ci.org/wejhink/django-mailcss)


## About
Sending a mail with CSS for is currently a surprisingly large hassle.
This library aims to make it a breeze in the Django template language.


## Usage

#### Step 1: Dependencies

- BeautifulSoup
- cssutils
- Python 2.7+,3.4+
- Django 1.11+


#### Step 2: Install django_mailcss

Add ```django_mailcss``` to your ```settings.py```:

```python
INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.webdesign',
        'django.contrib.contenttypes',
        '...',
        '...',
        '...',
        'django_mailcss')
```

#### Step 3: Use the templatetag

1. Place your CSS file somewhere staticfiles can find it
2. Create your template:

```html
{% load mailcss %}
{% mailcss "css/extra-padding.css" %}
    <html>
        <body>
            <div class='lots-o-padding'>
                Something in need of styling.
            </div>
        </body>
    </html>
{% endmailcss %}
```

#### Step 4: Prepare to be Wowed

```html
<html>
    <body>
        <div style="padding-left: 10px; padding-right: 10px; padding-top: 10px;" class="lots-o-padding">
            Something in need of styling.
        </div>
    </body>
</html>
```

## Acknowledgements
Thanks to Jeremy Nauta, Philip Kimmey and Keith for [django-inlinecss](https://github.com/roverdotcom/django-inlinecss)

Thanks to Tanner Netterville for his efforts on [Pynliner](https://github.com/rennat/pynliner).

Thanks to Thomas Yip for his unit tests on the `soupselect` module. These tests
helped on getting the core CSS2 selectors to work.

## License

MIT license. See LICENSE.md for more detail.
