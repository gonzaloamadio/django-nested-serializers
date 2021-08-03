# Purpose

Test package: https://github.com/beda-software/drf-writable-nested

# Tests

Beside reading package tests. Play around a bit with it.

## Nice user post with nested objects.

Request: post to {{api}}/users/

```text
{
            "username": "test",
            "profile": {
                "access_key": {
                    "key": "key"
                },
                "sites": [
                    {
                        "url": "http://google.com"
                    }
                ],
                "avatars": [
                    {
                        "image": "image-1.png"
                    }
                ],
                "message_set": [
                    {
                        "message": "Message 1"
                    }
                ]
            }
        }
```

Response

```text
{
    "pk": 4,
    "profile": {
        "pk": 4,
        "sites": [
            {
                "pk": 4,
                "url": "http://google.com"
            }
        ],
        "avatars": [
            {
                "pk": 4,
                "image": "image-1.png"
            }
        ],
        "access_key": {
            "pk": 4,
            "key": "key"
        },
        "message_set": [
            {
                "pk": 1,
                "message": "Message 1"
            }
        ]
    },
    "username": "test"
}
```

## User post with one nested object validation error.

Until here, we have only one element of each kind (that was created in last request, section up here).

Q: Do they all fail, or just the validated one?
A: Nothing is created. 

Why?

Because we have this setting in database settings:
```text
    DATABASE_NAME: {
        'ATOMIC_REQUESTS': True,
        ...
```
Id we do not have this atomic requests in true, we should do it explicitly. 
Refs: 
* https://stackoverflow.com/questions/34678784/do-i-need-to-explicitly-use-transactions-with-django-rest-framework-serializer-u
* https://docs.djangoproject.com/en/3.2/topics/db/transactions/#tying-transactions-to-http-requests


Request: post to {{api}}/users/

```text
{
            "username": "test",
            "profile": {
                "access_key": {
                    "key": "err_value"
                },
                "sites": [
                    {
                        "url": "asd.com"
                    }
                ],
                "avatars": [
                    {
                        "image": "image-1.png"
                    }
                ],
                "message_set": [
                    {
                        "message": "Message 1"
                    }
                ]
            }
        }
```

Response

```text
{
    "profile": {
        "access_key": {
            "key": [
                "Error value"
            ]
        }
    }
}
```

## Update existent object?

GET sites

```text
{
    "count": 1,
    "results": [
        {
            "pk": 4,
            "url": "http://google.com"
        }
    ]
}
```

Update using a POST.(have to add required=False to serializer fields)

```text
{
            "pk": 4,
            "profile": {
                "sites": [
                    {
                        "pk": 4,
                        "url": "http://new-site.com"
                    }
                ]
            }
        }
```
Response. New object is created, m2m related and updated

```text
{
    "pk": 9,
    "profile": {
        "pk": 9,
        "sites": [
            {
                "pk": 4,
                "url": "http://new-site.com"
            }
        ],
        "avatars": [],
        "access_key": null,
        "message_set": []
    },
    "username": "test"
}
```

GET Sites

```text
{
    "count": 1,
    "results": [
        {
            "pk": 4,
            "url": "http://new-site.com"
        }
    ]
}
```

PATCH to /users/9/

```text
{
            "username": "test2",
            "profile": {
                "sites": [
                    {
                        "pk": 4,
                        "url": "http://new-site2.com"
                    }
                ]
            }
        }
```
```text
{
    "pk": 9,
    "profile": {
        "pk": 9,
        "sites": [
            {
                "pk": 4,
                "url": "http://new-site2.com"
            }
        ],
        "avatars": [],
        "access_key": null,
        "message_set": []
    },
    "username": "test2"
}
```