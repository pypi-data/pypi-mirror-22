# django-modeltrans

[![Travis CI](https://travis-ci.org/zostera/django-modeltrans.svg?branch=master)](https://travis-ci.org/zostera/django-modeltrans)

Translates Django model fields in a `JSONField` using a registration approach.

# Features/requirements

- Uses one `django.contrib.postgres.JSONField` (PostgreSQL jsonb field) for every record.
- Django 1.9, 1.10, 1.11 for now
- PostgreSQL >= 9.4 and Psycopg2 >= 2.5.4.

# Usage

 - Add `'modeltrans'` your list of `INSTALLED_APPS`.
 - Add a list of available languages to your `settings.py`:
   `AVAILABLE_LANGUAGES = ('en', 'nl', 'de', 'fr')`
 - Add a `translation.py` in each app you want to translate models for.
 - For each model you want to translate, create a `TransltionOptions` object and register the model using that object:
```python
# models.py
from django.db import models


class Blog(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField(null=True)

# translation.py
from modeltrans.translator import TranslationOptions, translator

from .models import Blog, Category


class BlogTranslationOptions(TranslationOptions):
    fields = ('title', 'body')

translator.register(Blog, BlogTranslationOptions)
```
 - Run `./manage.py makemigrations` to add the `i18n` JSONField to each model containing
   translations.
 - Each method now has some extra virtual fields. In the example above:
   - `title_nl`, `title_de`, ... allow getting/setting the specific languages
   - `title_i18n` follows the currently active translation in Django, and falls
     back to the default language:

```python
>>> b = Blog.objects.create(title='Falcon', title_nl='Valk')
>>> b.title
'Falcon'
>>> b.title_nl
'Valk'
>>> b.title_i18n
'Falcon'
>>> from django.utils.translation import override
>>> with override('nl'):
...   b.title_i18n
...
'Valk'
# translations are stored in the field `i18n` in each model:
>>> b.i18n
{u'title_nl': u'Valk'}
# if a translation is not available, None is returned.
>>> print(b.title_de)
None
# fallback to the default language
>>> with override('de'):
...     b.title_i18n
'Falcon'
# now, if we set the German tranlation, it it is returned from title_i18n:
>>> b.title_de = 'Falk'
>>> with override('de'):
...     b.title_i18n
'Falk'
```

# Migrating from django-modeltranslation

This is how to migrate from django-modeltranslation (version 0.12.1) to
django-modeltrans:

1. Make sure you have a recent backup available!
2. Add `modeltrans` to your `INSTALLED_APPS`
3. Copy the django-modeltranslation registrations to use django-modeltrans
   alongside it, while disabling the virtual fields for now:
```python

# if this whas your configuration:
from modeltranslation.translator import translator, TranslationOptions
from .models import Blog

class BlogTranslationOptions(TranslationOptions):
    fields = ('name', 'title', )

translator.register(Blog, BlogTranslationOptions)

# this is what you add:
def i18n_migrate():
    from modeltrans import translator, TranslationOptions

    translator.disable_create_virtual_fields()


    class BlogTranslationOptions(TranslationOptions):
        fields = ('name', 'title', )

    translator.register(Blog, BlogTranslationOptions)


# and make sure it gets executed
i18n_migrate()
```
3. Run `./manage.py makemigrations <apps>`. This will create the
   migration adding the`i18n`-fields required by django-modeltrans. Apply
   them with `./manage.py migrate`
4. We need to create a migration to copy the values of the translated
   fields into the newly created `i18n`-field. django-modeltrans provides
   a management command to do that:
     `./manage.py i18n_makemmigrations <apps>`
5. Now, remove django-modeltranslation by:
    - Removing the translation registrations for `modeltranslation` from your
      `translation.py`'s. Also remove the function around the new registrations.
    - Remove the use of `modeltranslation.admin.TranslationAdmin` in your `admin.py`'s

   Run `./manage.py makemigrations <apps>`. This will remove the translated
   fields from your registered models. You can now safely remove the line
   `translator.disable_create_virtual_fields()` and let django-modeltrans add
   the virtual fields to your models.
5. Update your code and cleanup:
    - Remove `modeltranslation` from `INSTALLED_APPS`.
    - Use `<field>_i18n` field names for places where you would use `<field>`
      with django-modeltranslation. Less magic, but
      [explicit is better than implicit](https://www.python.org/dev/peps/pep-0020/)!

'''
# Running the tests

`tox`

Running the tests only for the current environment, use `make test`


# Attribution
Some concepts and code from https://github.com/deschler/django-modeltranslation,
which is in turn inspired by https://github.com/zmathew/django-linguo

We started this solution at Zostera because we did not like:
- The way django-modeltranslation adds one field per language (and thus requires a migration
when adding language)
- The unpredictability of the original field.

Since JSONB is supported by Postgres now, we developed this approach.

# alternatives
- [django-nence](https://github.com/tatterdemalion/django-nece/)
  Also uses a `jsonb` PostgreSQL field, but has a bunch of custom `QuerySet` and `Model` methods to get translated values. It also requires one to inherit from a `TranslationModel`.
- [django-i18nfield](https://github.com/raphaelm/django-i18nfield)
  Stores JSON in a `TextField`, so does not allow lookup, searching or ordering by the translated fields.

# relevant 3rd party documentation
- [PostgreSQL jsonb functions](https://www.postgresql.org/docs/9.5/static/functions-json.html)
