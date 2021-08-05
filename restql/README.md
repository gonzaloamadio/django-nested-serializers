# Purpose

Toy app to test some django-restql bugs.

# First bug (DB integrity error)

Patch a model that has a FK to it. Inside the patch try to create a model that violest a unique constraint on 
the nested model.

Result: Server error.

## Reproduce bug

Create an ingredient (>>> Ingredient.objects.create(name='ing1'))

POST api/products

```text
{
    "name" : "firstproductname",
    "ingredient_mixes": {
        "create": [
            {"ingredient": 1}
        ]
    }
}
```

Result:

```text
{
    "id": 10,
    "ingredient_mixes": [
        {
            "id": 5,
            "ingredient": {
                "id": 1,
                "name": "ing1"
            },
            "product": 10,
            "name": "somename"
        }
    ],
    "name": "firstproductname"
}
```

GET api/products

```text
{
    "count": 4,
    "results": [
        {
            "id": 10,
            "ingredient_mixes": [
                {
                    "id": 5,
                    "ingredient": {
                        "id": 1,
                        "name": "ing1"
                    },
                    "product": 10,
                    "name": "somename"
                }
            ],
            "name": "firstproductname"
        }
    ]
}
```
PATCH {{api}}/products/10/
```
{
    "name" : "first product name",
    "ingredient_mixes": {
        "create": [
            {"ingredient": 1}
        ]
    }
}
```

Error on server's console

```text
Internal Server Error: /api/products/6/
Traceback (most recent call last):
  File "/Users/gonzaloamadio/.virtualenvs/django-basic/lib/python3.7/site-packages/django/core/handlers/exception.py", line 47, in inner
    response = get_response(request)
  File "/Users/gonzaloamadio/.virtualenvs/django-basic/lib/python3.7/site-packages/django/core/handlers/base.py", line 181, in _get_response
    response = wrapped_callback(request, *callback_args, **callback_kwargs)
  File "/Users/gonzaloamadio/.virtualenvs/django-basic/lib/python3.7/site-packages/django/views/decorators/csrf.py", line 54, in wrapped_view
    return view_func(*args, **kwargs)
  File "/Users/gonzaloamadio/.virtualenvs/django-basic/lib/python3.7/site-packages/rest_framework/viewsets.py", line 125, in view
    return self.dispatch(request, *args, **kwargs)
  File "/Users/gonzaloamadio/.virtualenvs/django-basic/lib/python3.7/site-packages/rest_framework/views.py", line 509, in dispatch
    response = self.handle_exception(exc)
  File "/Users/gonzaloamadio/.virtualenvs/django-basic/lib/python3.7/site-packages/rest_framework/views.py", line 469, in handle_exception
    self.raise_uncaught_exception(exc)
  File "/Users/gonzaloamadio/.virtualenvs/django-basic/lib/python3.7/site-packages/rest_framework/views.py", line 480, in raise_uncaught_exception
    raise exc
  File "/Users/gonzaloamadio/.virtualenvs/django-basic/lib/python3.7/site-packages/rest_framework/views.py", line 506, in dispatch
    response = handler(request, *args, **kwargs)
  File "/Users/gonzaloamadio/.virtualenvs/django-basic/lib/python3.7/site-packages/rest_framework/mixins.py", line 82, in partial_update
    return self.update(request, *args, **kwargs)
  File "/Users/gonzaloamadio/.virtualenvs/django-basic/lib/python3.7/site-packages/rest_framework/mixins.py", line 68, in update
    self.perform_update(serializer)
  File "/Users/gonzaloamadio/.virtualenvs/django-basic/lib/python3.7/site-packages/rest_framework/mixins.py", line 78, in perform_update
    serializer.save()
  File "/Users/gonzaloamadio/.virtualenvs/django-basic/lib/python3.7/site-packages/rest_framework/serializers.py", line 200, in save
    self.instance = self.update(self.instance, validated_data)
  File "/Users/gonzaloamadio/.virtualenvs/django-basic/lib/python3.7/site-packages/django_restql/mixins.py", line 1046, in update
    fields["many_to"]["one_related"]
  File "/Users/gonzaloamadio/.virtualenvs/django-basic/lib/python3.7/site-packages/django_restql/mixins.py", line 921, in update_many_to_one_related
    values[operation]
  File "/Users/gonzaloamadio/.virtualenvs/django-basic/lib/python3.7/site-packages/django_restql/mixins.py", line 843, in bulk_create_many_to_one_related
    obj = serializer.save()
  File "/Users/gonzaloamadio/.virtualenvs/django-basic/lib/python3.7/site-packages/rest_framework/serializers.py", line 178, in save
    'You cannot call `.save()` on a serializer with invalid data.'
AssertionError: You cannot call `.save()` on a serializer with invalid data.
```


# Second Bug (Have to put full object for patching)

The problem is that to do a patch to a model with a nested field serializer, we have to send full object just to modify one field.

Get an ingredient mix:

GET {{api}}/ingredientmixes/6/
```text
{
    "id": 6,
    "ingredient": {
        "id": 1,
        "name": "ing1"
    },
    "product": 6,
    "name": "Other name"
}
```

PATCH with all fields:

PATCH {{api}}/ingredientmixes/6/
```text
{
    "name" : "New name",
    "ingredient": 1
}
```
Response:

```text
{
    "id": 6,
    "ingredient": {
        "id": 1,
        "name": "ing1"
    },
    "product": 6,
    "name": "New name"
}
```


PATCH only name

PATCH {{api}}/ingredientmixes/6/
```text
{
    "name" : "New name"
}
```
Response:

```text
Internal Server Error: /api/ingredientmixes/6/
Traceback (most recent call last):
  File "/Users/gonzaloamadio/.virtualenvs/django-basic/lib/python3.7/site-packages/django/core/handlers/exception.py", line 47, in inner
    response = get_response(request)
  File "/Users/gonzaloamadio/.virtualenvs/django-basic/lib/python3.7/site-packages/django/core/handlers/base.py", line 181, in _get_response
    response = wrapped_callback(request, *callback_args, **callback_kwargs)
  File "/Users/gonzaloamadio/.virtualenvs/django-basic/lib/python3.7/site-packages/django/views/decorators/csrf.py", line 54, in wrapped_view
    return view_func(*args, **kwargs)
  File "/Users/gonzaloamadio/.virtualenvs/django-basic/lib/python3.7/site-packages/rest_framework/viewsets.py", line 125, in view
    return self.dispatch(request, *args, **kwargs)
  File "/Users/gonzaloamadio/.virtualenvs/django-basic/lib/python3.7/site-packages/rest_framework/views.py", line 509, in dispatch
    response = self.handle_exception(exc)
  File "/Users/gonzaloamadio/.virtualenvs/django-basic/lib/python3.7/site-packages/rest_framework/views.py", line 469, in handle_exception
    self.raise_uncaught_exception(exc)
  File "/Users/gonzaloamadio/.virtualenvs/django-basic/lib/python3.7/site-packages/rest_framework/views.py", line 480, in raise_uncaught_exception
    raise exc
  File "/Users/gonzaloamadio/.virtualenvs/django-basic/lib/python3.7/site-packages/rest_framework/views.py", line 506, in dispatch
    response = handler(request, *args, **kwargs)
  File "/Users/gonzaloamadio/.virtualenvs/django-basic/lib/python3.7/site-packages/rest_framework/mixins.py", line 82, in partial_update
    return self.update(request, *args, **kwargs)
  File "/Users/gonzaloamadio/.virtualenvs/django-basic/lib/python3.7/site-packages/rest_framework/mixins.py", line 68, in update
    self.perform_update(serializer)
  File "/Users/gonzaloamadio/.virtualenvs/django-basic/lib/python3.7/site-packages/rest_framework/mixins.py", line 78, in perform_update
    serializer.save()
  File "/Users/gonzaloamadio/.virtualenvs/django-basic/lib/python3.7/site-packages/rest_framework/serializers.py", line 200, in save
    self.instance = self.update(self.instance, validated_data)
  File "/Users/gonzaloamadio/.virtualenvs/django-basic/lib/python3.7/site-packages/rest_framework/serializers.py", line 981, in update
    setattr(instance, attr, value)
  File "/Users/gonzaloamadio/.virtualenvs/django-basic/lib/python3.7/site-packages/django/db/models/fields/related_descriptors.py", line 220, in __set__
    self.field.remote_field.model._meta.object_name,
ValueError: Cannot assign "<class 'rest_framework.fields.empty'>": "IngredientMix.ingredient" must be a "Ingredient" instance.
```
