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

Check testapp/urls.py to enable apps urls. I commented them out for less pollution.