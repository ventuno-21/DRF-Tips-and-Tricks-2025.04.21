🧠 DRF Tips a🧠 DRF Tips and Tricks — Annotated Guide
=====================================================

This document breaks down each commit from the DRF Tips and Tricks repo into digestible explanations and examples. Each section corresponds to a commit and highlights a specific DRF concept.

✅ serializer save method
------------------------

### 🔍 Explanation

The save() method in DRF serializers is a wrapper around create() and update(). It’s commonly overridden to customize object creation logic.

### 🧪 Example
```
class ArticleSerializer(serializers.ModelSerializer):
    def save(self, **kwargs):
        instance = super().save(**kwargs)
        instance.slug = slugify(instance.title)
        instance.save()
        return instance
```

✅ serializer create method
--------------------------

### 🔍 Explanation

Used when creating new instances. DRF calls create() when serializer.save() is invoked on a new object.

### 🧪 Example

```
class ArticleSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return Article.objects.create(**validated_data)
```

✅ serializer update method
--------------------------

### 🔍 Explanation

Used to update existing instances. DRF calls update() when serializer.save() is invoked on an existing object.

### 🧪 Example

```
class ArticleSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        return instance
```

✅ serializer data vs validated\_data
------------------------------------

### 🔍 Explanation

*   validated\_data: Available after is\_valid() is called.
    
*   data: Available after serialization, includes all fields (even unvalidated).
    

### 🧪 Example

```
serializer = ArticleSerializer(data=request.data)
serializer.is_valid()
print(serializer.validated_data)  # Cleaned input
print(serializer.data)            # Serialized output
```

✅ serializer context
--------------------

### 🔍 Explanation

Context allows passing extra data (like request) into the serializer.

### 🧪 Example

```
serializer = ArticleSerializer(data=request.data, context={'request': request})
```

Inside the serializer:

```
user = self.context['request'].user
```
✅ serializer fields customization
---------------------------------

### 🔍 Explanation

You can customize fields using extra\_kwargs, read\_only\_fields, or override to\_representation.

### 🧪 Example

```
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'author']
        read_only_fields = ['author']
```

✅ serializer to\_representation
-------------------------------

### 🔍 Explanation

Used to customize the output of serialized data.

### 🧪 Example
```
def to_representation(self, instance):
    rep = super().to_representation(instance)
    rep['author_name'] = instance.author.username
    return rep
```
✅ serializer validate method
----------------------------

### 🔍 Explanation

Use validate() to apply custom validation across multiple fields.

### 🧪 Example
```
def validate(self, attrs):
    if attrs['start_date'] > attrs['end_date']:
        raise serializers.ValidationError("Start date must be before end date.")
    return attrs
```
✅ serializer field-level validation
-----------------------------------

### 🔍 Explanation

Use validate\_() for field-specific validation.

### 🧪 Example
```
def validate_title(self, value):
    if 'django' not in value.lower():
        raise serializers.ValidationError("Title must include 'django'.")
    return value
```
✅ serializer nested relationships
---------------------------------

### 🔍 Explanation

DRF supports nested serializers for related models.

### 🧪 Example
```
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['name']

class ArticleSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
```
✅ serializer save method
------------------------

### 🔍 Explanation

The save() method wraps create() and update() logic. Override it to customize post-processing after validation.

### 🧪 Example

```
def save(self, **kwargs):
    instance = super().save(**kwargs)
    instance.slug = slugify(instance.title)
    instance.save()
    return instance
```
✅ serializer create method
--------------------------

### 🔍 Explanation

Used to define how new model instances are created from validated data.

### 🧪 Example
```
def create(self, validated_data):
    validated_data['author'] = self.context['request'].user
    return Article.objects.create(**validated_data)
```
✅ serializer update method
--------------------------

### 🔍 Explanation

Defines how existing instances are updated with new data.

### 🧪 Example

```
def update(self, instance, validated_data):
    instance.title = validated_data.get('title', instance.title)
    instance.save()
    return instance
```
✅ serializer data vs validated\_data
------------------------------------

### 🔍 Explanation

*   validated\_data: Cleaned input after is\_valid().
    
*   data: Serialized output after saving.
    

### 🧪 Example
```
serializer = ArticleSerializer(data=request.data)
serializer.is_valid()
print(serializer.validated_data)
print(serializer.data)
```

✅ serializer context
--------------------

### 🔍 Explanation

Pass extra data (like request) to serializers via context.

### 🧪 Example

```
serializer = ArticleSerializer(data=request.data, context={'request': request})
```

✅ serializer fields customization
---------------------------------

### 🔍 Explanation

Customize fields using extra\_kwargs, read\_only\_fields, or override to\_representation.

### 🧪 Example

```
class Meta:
    model = Article
    fields = ['id', 'title', 'author']
    read_only_fields = ['author']
```
✅ serializer to\_representation
-------------------------------

### 🔍 Explanation

Customize output representation of serialized data.

### 🧪 Example

```
def to_representation(self, instance):
    rep = super().to_representation(instance)
    rep['author_name'] = instance.author.username
    return rep
```

✅ serializer validate method
----------------------------

### 🔍 Explanation

Use validate() for cross-field validation.

### 🧪 Example

```
def validate(self, attrs):
    if attrs['start_date'] > attrs['end_date']:
        raise serializers.ValidationError("Start date must be before end date.")
    return attrs
```

✅ serializer field-level validation
-----------------------------------

### 🔍 Explanation

Use validate\_() for individual field validation.

### 🧪 Example
```
def validate_title(self, value):
    if 'django' not in value.lower():
        raise serializers.ValidationError("Title must include 'django'.")
    return value
```

✅ serializer nested relationships
---------------------------------

### 🔍 Explanation

Use nested serializers to represent related models.

### 🧪 Example

```
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['name']

class ArticleSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
```

✅ serializer depth
------------------

### 🔍 Explanation

Use depth to auto-serialize related models.

### 🧪 Example

```
class Meta:
    model = Article
    fields = '__all__'
    depth = 1
```
✅ serializer source
-------------------

### 🔍 Explanation

Use source to map serializer fields to model attributes or methods.

### 🧪 Example

```
author_name = serializers.CharField(source='author.username')
```
✅ serializer method field
-------------------------

### 🔍 Explanation

Use SerializerMethodField for custom computed fields.

### 🧪 Example

```
author_name = serializers.SerializerMethodField()

def get_author_name(self, obj):
    return obj.author.username
```

✅ serializer hidden field
-------------------------

### 🔍 Explanation

Use HiddenField to auto-populate fields like created\_by.

### 🧪 Example

```
created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
```
✅ serializer slug related field
-------------------------------

### 🔍 Explanation

Use SlugRelatedField to represent related objects using a slug field.

### 🧪 Example

```
author = serializers.SlugRelatedField(read_only=True, slug_field='username')
```

✅ serializer primary key related field
--------------------------------------

### 🔍 Explanation

Use PrimaryKeyRelatedField to represent related objects by their ID.

### 🧪 Example

```
author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
```

✅ serializer string related field
---------------------------------

### 🔍 Explanation

Use StringRelatedField to represent related objects using their \_\_str\_\_() method.

### 🧪 Example

```
author = serializers.StringRelatedField()
```
✅ serializer read only field
----------------------------

### 🔍 Explanation

Use ReadOnlyField for fields that should not be editable.

### 🧪 Example

```
created_at = serializers.ReadOnlyField()
```

✅ serializer write only field
-----------------------------

### 🔍 Explanation

Use WriteOnlyField for fields used only during input (e.g. passwords).

### 🧪 Example

```
password = serializers.CharField(write_only=True)
```

✅ serializer choice field
-------------------------

### 🔍 Explanation

Use ChoiceField to restrict input to predefined choices.

### 🧪 Example

```
status = serializers.ChoiceField(choices=['draft', 'published'])
```

✅ serializer multiple choice field
----------------------------------

### 🔍 Explanation

Use MultipleChoiceField for multi-select inputs.

### 🧪 Example

```
tags = serializers.MultipleChoiceField(choices=['django', 'drf', 'api'])
```

✅ serializer email field
------------------------

### 🔍 Explanation

Use EmailField to validate email input.

### 🧪 Example
```
email = serializers.EmailField()
```
✅ serializer url field
----------------------

### 🔍 Explanation

Use URLField to validate URLs.

### 🧪 Example

```
website = serializers.URLField()
```
✅ serializer ip address field
-----------------------------

### 🔍 Explanation

Use IPAddressField to validate IP addresses.

### 🧪 Example

```
ip_address = serializers.IPAddressField()
```

✅ serializer decimal field
--------------------------

### 🔍 Explanation

Use DecimalField for precise decimal values.

### 🧪 Example

```
price = serializers.DecimalField(max_digits=6, decimal_places=2)
```

✅ serializer date field
-----------------------

### 🔍 Explanation

Use DateField for date input.

### 🧪 Example

```
published_date = serializers.DateField()
```

✅ serializer time field
-----------------------

### 🔍 Explanation

Use TimeField for time input.

### 🧪 Example
```
published_time = serializers.TimeField()
```

✅ serializer datetime field
---------------------------

### 🔍 Explanation

Use DateTimeField for datetime input.

### 🧪 Example

```
created_at = serializers.DateTimeField()
```

✅ serializer duration field
---------------------------

### 🔍 Explanation

Use DurationField for time durations.

### 🧪 Example
```
duration = serializers.DurationField()
```

✅ serializer file field
-----------------------

### 🔍 Explanation

Use FileField to handle file uploads.

### 🧪 Example

```
document = serializers.FileField()
```

✅ serializer image field
------------------------

### 🔍 Explanation

Use ImageField to handle image uploads.

### 🧪 Example
```
photo = serializers.ImageField()
```
✅ serializer boolean field
--------------------------

### 🔍 Explanation

Use BooleanField for true/false values.

### 🧪 Example

```
is_active = serializers.BooleanField()
```

✅ serializer integer field
--------------------------

### 🔍 Explanation

Use IntegerField for integer input.

### 🧪 Example

```
views = serializers.IntegerField()
```

✅ serializer float field
------------------------

### 🔍 Explanation

Use FloatField for floating-point numbers.

### 🧪 Example

```
rating = serializers.FloatField()
```
