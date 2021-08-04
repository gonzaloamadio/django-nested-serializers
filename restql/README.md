# Purpose

Toy app to test some django-restql bugs.

# First bug

Patch a model that has a FK to it. Inside the patch try to create a model that violest a unique constraint on 
the nested model.

Result: Server error.

## Reproduce bug

Create an ingredient (>>> Ingredient.objects.create(name='ing1'))

POST api/products

```text
{
    "name" : "firstproductname",
    "ingredients": {
        "create": [
            {"ingredient": 1}
        ]
    }
}
```

Result:

```text
{
    "id": 3,
    "name": "firstproductname"
}
```

GET api/products

```text
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 3,
            "name": "firstproductname"
        }
    ]
}
```