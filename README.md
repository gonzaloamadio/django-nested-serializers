# django-nested-serializers
Test different options to implement nested serializers

# TODO

* Make custom serializers (like version 9 serializer) work with open api schema (see link in serializers field). 
* Make custom serializers (like version 9 serializer) work with browsable API (see link in serializers field). 
* If you are using a third party package, for example drf_spectacular see (https://drf-spectacular.readthedocs.io/en/latest/customization.html#step-3-extend-schema-field-and-type-hints)
* Let post accept a list of ids with custom field. Probably with this is enough:
```
    def to_internal_value(self, data):
        model = self.model # pass model name as argument
        self.fields[self.field] = serializers.PrimaryKeyRelatedField(queryset=model.objects.all(), many=self.many)
        return super().to_internal_value(data)
```
* Check this other repositories : https://github.com/beda-software/drf-writable-nested, https://github.com/yezyilomo/django-restql

# Repo usage

* Clone repo
* Create a venv
* pip install -r requirements.txt
* Run `./manage.py migrate`
* Run `python manage.py createsuperuser --username=admin --email=admin@example.com`
* Run `./manage.py runserver 0.0.0.0:8000` and play around.


# Tests

Assume I have created an album called "Black Album" with two songs: "Enter Sandman" and "Sad But True".


## Get

```text
❯ http http://localhost:8000/api/songsv1/
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "album": {
                "id": 1,
                "name": "Black Album"
            },
            "name": "Enter Sandman"
        },
        {
            "album": {
                "id": 1,
                "name": "Black Album"
            },
            "name": "Sad But True"
        }
    ]
}

❯ http http://localhost:8000/api/songsv1/1/
{
    "album": {
        "id": 1,
        "name": "Black Album"
    },
    "name": "Enter Sandman"
}


❯ http http://localhost:8000/api/songsv1/5/
{
    "detail": "Not found."
}
```

```text
❯ http http://localhost:8000/api/songsv2/
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "album": {
                "id": 1,
                "name": "Black Album"
            },
            "id": 1,
            "name": "Enter Sandman"
        },
        {
            "album": {
                "id": 1,
                "name": "Black Album"
            },
            "id": 2,
            "name": "Sad But True"
        }
    ]
}

❯ http http://localhost:8000/api/songsv2/1/
{
    "album": {
        "id": 1,
        "name": "Black Album"
    },
    "name": "Enter Sandman"
}


❯ http http://localhost:8000/api/songsv2/5/
{
    "detail": "Not found."
}
```

```text
❯ http http://localhost:8000/api/songsv3/
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "album": {
                "id": 1,
                "name": "Black Album"
            },
            "id": 1,
            "name": "Enter Sandman"
        },
        {
            "album": {
                "id": 1,
                "name": "Black Album"
            },
            "id": 2,
            "name": "Sad But True"
        }
    ]
}

❯ http http://localhost:8000/api/songsv3/1/
{
    "album": {
        "id": 1,
        "name": "Black Album"
    },
    "name": "Enter Sandman"
}

❯ http http://localhost:8000/api/songsv3/5/
{
    "detail": "Not found."
}
```
```text
❯ http http://localhost:8000/api/songsv4/
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "album": {
                "id": 1,
                "name": "Black Album"
            },
            "id": 1,
            "name": "Enter Sandman"
        },
        {
            "album": {
                "id": 1,
                "name": "Black Album"
            },
            "id": 2,
            "name": "Sad But True"
        }
    ]
}

❯ http http://localhost:8000/api/songsv41/
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "album": {
                "id": 1,
                "name": "Black Album"
            },
            "id": 1,
            "name": "Enter Sandman"
        },
        {
            "album": {
                "id": 1,
                "name": "Black Album"
            },
            "id": 2,
            "name": "Sad But True"
        }
    ]
}

❯ http http://localhost:8000/api/songsv4/1/
{
    "album": {
        "id": 1,
        "name": "Black Album"
    },
    "name": "Enter Sandman"
}

❯ http http://localhost:8000/api/songsv4/5/
{
    "detail": "Not found."
}

❯ http http://localhost:8000/api/songsv41/1/
{
    "album": {
        "id": 1,
        "name": "Black Album"
    },
    "name": "Enter Sandman"
}

❯ http http://localhost:8000/api/songsv41/5/
{
    "detail": "Not found."
}

```
```text
❯ http http://localhost:8000/api/songsv5/
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "album": {
                "name": "Black Album",
                "tracks": [
                    {
                        "name": "Enter Sandman"
                    },
                    {
                        "name": "Sad But True"
                    }
                ]
            },
            "id": 1,
            "name": "Enter Sandman"
        },
        {
            "album": {
                "name": "Black Album",
                "tracks": [
                    {
                        "name": "Enter Sandman"
                    },
                    {
                        "name": "Sad But True"
                    }
                ]
            },
            "id": 2,
            "name": "Sad But True"
        }
    ]
}

❯ http http://localhost:8000/api/songsv5/1/
{
    "album": {
        "id": 1,
        "name": "Black Album",
        "tracks": [
            {
                "name": "Enter Sandman"
            },
            {
                "name": "Sad But True"
            }
        ]
    },
    "id": 1,
    "name": "Enter Sandman"
}
```

```text
❯ http http://localhost:8000/api/songsv6/
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "album": {
                "name": "Black Album",
                "tracks": [
                    {
                        "name": "Enter Sandman"
                    },
                    {
                        "name": "Sad But True"
                    }
                ]
            },
            "id": 1,
            "name": "Enter Sandman"
        },
        {
            "album": {
                "name": "Black Album",
                "tracks": [
                    {
                        "name": "Enter Sandman"
                    },
                    {
                        "name": "Sad But True"
                    }
                ]
            },
            "id": 2,
            "name": "Sad But True"
        }
    ]
}

❯ http http://localhost:8000/api/songsv6/1/
{
    "album": {
        "id": 1,
        "name": "Black Album",
        "tracks": [
            {
                "name": "Enter Sandman"
            },
            {
                "name": "Sad But True"
            }
        ]
    },
    "id": 1,
    "name": "Enter Sandman"
}
```

```text
❯ http http://localhost:8000/api/songsv7/
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "album": {
                "name": "Black Album",
                "tracks": [
                    {
                        "name": "Enter Sandman"
                    },
                    {
                        "name": "Sad But True"
                    }
                ]
            },
            "id": 1,
            "name": "Enter Sandman"
        },
        {
            "album": {
                "name": "Black Album",
                "tracks": [
                    {
                        "name": "Enter Sandman"
                    },
                    {
                        "name": "Sad But True"
                    }
                ]
            },
            "id": 2,
            "name": "Sad But True"
        }
    ]
}

❯ http http://localhost:8000/api/songsv7/1/
{
    "album": {
        "id": 1,
        "name": "Black Album",
        "tracks": [
            {
                "name": "Enter Sandman"
            },
            {
                "name": "Sad But True"
            }
        ]
    },
    "id": 1,
    "name": "Enter Sandman"
}
```
```text
❯ http http://localhost:8000/api/songsv8/
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "album": {
                "name": "Black Album",
                "tracks": [
                    {
                        "name": "Enter Sandman"
                    },
                    {
                        "name": "Sad But True"
                    }
                ]
            },
            "id": 1,
            "name": "Enter Sandman"
        },
        {
            "album": {
                "name": "Black Album",
                "tracks": [
                    {
                        "name": "Enter Sandman"
                    },
                    {
                        "name": "Sad But True"
                    }
                ]
            },
            "id": 2,
            "name": "Sad But True"
        }
    ]
}

❯ http http://localhost:8000/api/songsv8/1/
{
    "album": {
        "id": 1,
        "name": "Black Album",
        "tracks": [
            {
                "name": "Enter Sandman"
            },
            {
                "name": "Sad But True"
            }
        ]
    },
    "id": 1,
    "name": "Enter Sandman"
}
```
```text
❯ http http://localhost:8000/api/songsv9/
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "album": {
                "name": "Black Album",
                "tracks": [
                    {
                        "name": "Enter Sandman"
                    },
                    {
                        "name": "Sad But True"
                    }
                ]
            },
            "id": 1,
            "name": "Enter Sandman"
        },
        {
            "album": {
                "name": "Black Album",
                "tracks": [
                    {
                        "name": "Enter Sandman"
                    },
                    {
                        "name": "Sad But True"
                    }
                ]
            },
            "id": 2,
            "name": "Sad But True"
        }
    ]
}

❯ http http://localhost:8000/api/songsv9/1/
{
    "album": {
        "id": 1,
        "name": "Black Album",
        "tracks": [
            {
                "name": "Enter Sandman"
            },
            {
                "name": "Sad But True"
            }
        ]
    },
    "id": 1,
    "name": "Enter Sandman"
}
```
```text
❯ http http://localhost:8000/api/songsv10/
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "album": 1,
            "id": 1,
            "name": "Enter Sandman"
        },
        {
            "album": 1,
            "id": 2,
            "name": "Sad But True"
        }
    ]
}

❯ http http://localhost:8000/api/songsv10/1/
{
    "album": 1,
    "id": 1,
    "name": "Enter Sandman"
}
```
```text
❯ http http://localhost:8000/api/songsv11/
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "album": {
                "name": "Black Album",
                "tracks": [
                    {
                        "name": "Enter Sandman"
                    },
                    {
                        "name": "Sad But True"
                    }
                ]
            },
            "id": 1,
            "name": "Enter Sandman"
        },
        {
            "album": {
                "name": "Black Album",
                "tracks": [
                    {
                        "name": "Enter Sandman"
                    },
                    {
                        "name": "Sad But True"
                    }
                ]
            },
            "id": 2,
            "name": "Sad But True"
        }
    ]
}

❯ http http://localhost:8000/api/songsv11/1/
{
    "album": {
        "id": 1,
        "name": "Black Album",
        "tracks": [
            {
                "name": "Enter Sandman"
            },
            {
                "name": "Sad But True"
            }
        ]
    },
    "id": 1,
    "name": "Enter Sandman"
}
```

## Post

```text
❯ http http://localhost:8000/api/songsv1/ album=10000 name=testv1
{
    "album_id": [
        "This field is required."
    ]
}

❯ http http://localhost:8000/api/songsv1/ album=10000 name=testv1
EXCEPTION RAISED ON SERVER:
    IntegrityError: FOREIGN KEY constraint failed

❯ http http://localhost:8000/api/songsv1/ album_id=1 name=testv1
{
    "album": {
        "id": 1,
        "name": "Black Album"
    },
    "name": "testv1"
}
```

```
http://localhost:8000/api/songsv2/ : same behaviour as v1
```

```text
❯ http http://localhost:8000/api/songsv3/ album=10 name=testv3
    Server 500 error
    django.db.utils.IntegrityError: NOT NULL constraint failed: music_songs.album_id
    
❯ http http://localhost:8000/api/songsv3/ album_id=10 name=testv3
{
    "album_id": [
        "Invalid pk \"10\" - object does not exist."
    ]
}

http http://localhost:8000/api/songsv3/ album_id=1 name=testv3
    Server 500 error
    TypeError: Field 'id' expected a number but got <Album: Black Album>.
    TypeError: Got a `TypeError` when calling `Songs.objects.create()`. This may be because you have a writable 
        field on the serializer class that is not a valid argument to `Songs.objects.create()`. 
        You may need to make the field read-only, or override the SongsNestedSerializerV3.create() method 
        to handle this correctly.
    TypeError: int() argument must be a string, a bytes-like object or a number, not 'Album'
```

```text
❯ http http://localhost:8000/api/songsv4/ album=10 name=testv4
    Server 500 error
    django.db.utils.IntegrityError: NOT NULL constraint failed: music_songs.album_id
    
❯ http http://localhost:8000/api/songsv4/ album_id=10 name=testv4
{
    "album_id": [
        "Invalid pk \"10\" - object does not exist."
    ]
}
  
    
❯ http http://localhost:8000/api/songsv4/ album_id=1 name=testv4
{
    "album": {
        "id": 1,
        "name": "Black Album"
    },
    "id": 5,
    "name": "testv4"
}
```

```text
❯ http http://localhost:8000/api/songsv5/ album=10 name=testv5
    Server 500 error
    django.db.utils.IntegrityError: NOT NULL constraint failed: music_songs.album_id
    
❯ http http://localhost:8000/api/songsv5/ album_id=10 name=testv5
{
    "album_id": [
        "Invalid pk \"10\" - object does not exist."
    ]
}

❯ http http://localhost:8000/api/songsv5/ album_id=1 name=testv5
{
    "album": {
        "id": 1,
        "name": "Black Album",
        "tracks": [
            {
                "name": "Enter Sandman"
            },
            {
                "name": "Sad But True"
            },
            {
                "name": "testv1"
            },
            {
                "name": "testv2"
            },
            {
                "name": "testv4"
            },
            {
                "name": "testv5"
            }
        ]
    },
    "id": 6,
    "name": "testv5"
}
```

```text
❯ http http://localhost:8000/api/songsv6/ album=10 name=testv6
    Server 500 error
    django.db.utils.IntegrityError: NOT NULL constraint failed: music_songs.album_id
    
❯ http http://localhost:8000/api/songsv6/ album_id=10 name=testv6
{
    "album_id": [
        "Invalid pk \"10\" - object does not exist."
    ]
}

❯ http http://localhost:8000/api/songsv6/ album_id=1 name=testv6
{
    "album": {
        "id": 1,
        "name": "Black Album",
        "tracks": [
            {
                "name": "Enter Sandman"
            },
            {
                "name": "Sad But True"
            },
            {
                "name": "testv1"
            },
            
            ... all other tracks
            
            {
                "name": "testv6"
            }
        ]
    },
    "id": 7,
    "name": "testv6"
}
```

```text
❯ http http://localhost:8000/api/songsv7/ album=10 name=testv7
{
    "album": [
        "Invalid pk \"10\" - object does not exist."
    ]
}

❯ http http://localhost:8000/api/songsv7/ album_id=10 name=testv7
{
    "album": [
        "This field is required."
    ]
}

❯ http http://localhost:8000/api/songsv7/ album=1 name=testv7
{
    "album": {
        "id": 1,
        "name": "Black Album",
        "tracks": [
            {
                "name": "Enter Sandman"
            },
            {
                "name": "Sad But True"
            },
            {
                "name": "testv1"
            },
            
            ... all other tracks
            
            {
                "name": "testv7"
            }
        ]
    },
    "id": 8,
    "name": "testv7"
}

❯ http http://localhost:8000/api/songsv7flat/ album=1 name=testv7flat
{
    "album": {
        "id": 1,
        "name": "Black Album"
    },
    "id": 13,
    "name": "testv7flat"
}
```

```text
❯ http http://localhost:8000/api/songsv8/ album=10 name=testv8
{
    "album": [
        "Invalid pk \"10\" - object does not exist."
    ]
}

❯ http http://localhost:8000/api/songsv8/ album_id=10 name=testv8
{
    "album": [
        "This field is required."
    ]
}

❯ http http://localhost:8000/api/songsv8/ album=1 name=testv8
HTTP/1.1 201 Created
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 248
Content-Type: application/json
Date: Wed, 28 Jul 2021 01:08:45 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.7.6
Vary: Accept
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

{
    "album": {
        "id": 1,
        "name": "Black Album",
        "tracks": [
            {
                "name": "Enter Sandman"
            },
            {
                "name": "Sad But True"
            },
            {
                "name": "testv1"
            },
            
            ... all other tracks
            
            {
                "name": "testv8"
            }
        ]
    },
    "id": 9,
    "name": "testv8"
}
```

```text
❯ http http://localhost:8000/api/songsv9/ album_id=10 name=testv9
{
    "album": [
        "This field is required."
    ]
}

❯ http http://localhost:8000/api/songsv9/ album=10 name=testv9
{
    "album": [
        "Invalid pk \"10\" - object does not exist."
    ]
}

❯ http http://localhost:8000/api/songsv9/ album=1 name=testv9
{
    "album": {
        "id": 1,
        "name": "Black Album",
        "tracks": [
            {
                "name": "Enter Sandman"
            },
            {
                "name": "Sad But True"
            },
            {
                "name": "testv1"
            },
            
            ...other tracks
            
            {
                "name": "testv9"
            }
        ]
    },
    "id": 10,
    "name": "testv9"
}

❯ http http://localhost:8000/api/songsv9flat/ album=1 name=testv9flat
{
    "album": {
        "id": 1,
        "name": "Black Album"
    },
    "id": 14,
    "name": "testv9flat"
}

```

```text
❯ http http://localhost:8000/api/songsv10/ album_id=10 name=testv10
{
    "album": [
        "This field is required."
    ]
}

❯ http http://localhost:8000/api/songsv10/ album=10 name=testv10
{
    "album": [
        "Invalid pk \"10\" - object does not exist."
    ]
}

❯ http http://localhost:8000/api/songsv10/ album=1 name=testv10
{
    "album": 1,
    "id": 11,
    "name": "testv10"
}
```

```text
❯ http http://localhost:8000/api/songsv11/ album_id=1 name=testv11
{
    "album": [
        "This field is required."
    ]
}

❯ http http://localhost:8000/api/songsv11/ album=10 name=testv11
{
    "album": [
        "Invalid pk \"10\" - object does not exist."
    ]
}

❯ http http://localhost:8000/api/songsv11/ album=1 name=testv11
{
    "album": {
        "id": 1,
        "name": "Black Album",
        "tracks": [
            {
                "name": "Enter Sandman"
            },
            {
                "name": "Sad But True"
            },
            
            ... other tracks
            
            {
                "name": "testv11"
            }
        ]
    },
    "id": 12,
    "name": "testv11"
}

❯ http http://localhost:8000/api/songsv11flat/ album=1 name=testv11flat
{
    "album": {
        "id": 1,
        "name": "Black Album"
    },
    "id": 15,
    "name": "testv11flat"
}
```
