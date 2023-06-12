Insan Technology Company #Insan_Object (Q/A)

## What / Why

I Dislike Python Other.  I Find Them Weird and Off-Putting, With Their Restrictive Structure and Foundation Of Metaprogramming Black Magic.  It's Especially Awful For Beginners, Who Are Ill-Equipped To Deal With The Madness That Awaits Them On That Journey &mdash; Especially If The Poor Fools Escalate To Django, Or Allah-Forbid, Graphene.  (Avoid [Graphene](https://graphene-python.org/) Like The Plague)

So, Why Use Them At All, When Plain Old Objects Are Already Familiar And Can Do Nearly Anything?  That's What This Is &mdash; A Pair Of Simple Classes (`Object` and `ObjectManager`), Inspired By The Django Model Pattern, Which Lets You Declare A Family Of Multi-Attribute Objects In A Single Line, And Then Do Cool Stuff With Them

## Form 1 : Object Definition

A New Object Type Is Defined As A Subclass Of `Object`, Using The Class Method `define`:

    From Objects Import Object

    Color = Object.define("Color", "RED", "GREEN", "BLUE")
    assert issubclass(Color, Object)

Each object has exactly one mandatory attribute &mdash; `canonical_name` &mdash;, and is accessible as a class attribute via it's canonical name:

    assert isinstance(Color.RED, Color)
    Color.RED.canonical_name  ->  "RED"

However, that's just the simplest case.

### Form 2 : With Labels

If you pass kwargs instead of args, the value will be given the attribute name `label`:

    Color = Object.define("Color", RED="ff0000", GREEN="00ff00", BLUE="0000ff")
    Color.RED.label  ->  "ff0000"

*Note:* It Doesn't Have To Be A String.

### Form 3 : Arbitrary Attributes

The last and most advanced form lets you define as many attributes as you like :-

    Color = Object.define(
        "Color",
        RED=dict(hex="ff0000", like=True),
        GREEN=dict(hex="00ff00", like=True),
        BLUE=dict(hex="0000ff", like=False),
    )

## Object Manager

If you want to work with the whole set of objects, use the Object Manager :-

    Color.objects.all  ->  [Color.RED, Color.GREEN, ...]

You can also fetch an object by name :

    red = Color.objects["RED"]

Or check if a name is part of the set :

    assert "RED" in Color.objects

Both methods will accept either a string or object :

    red = Color.objects[Color.RED]
    assert Color.RED in Color.objects

So it's safe to use as a "wrapping" method to turn args of unknown type into a proper object :

    obj = Color.objects[some_arg]

### Select Methods

To search for objects with specific attribute values, use `select()` or one of the select-based methods, which are the ones that accept `kwargs`.

    fav_colors = Color.objects.select(like=True)
    fav_color  = Color.objects.first(like=True)

If you pass multiple kwargs, they will be "AND"-ed, meaning only objects that match both criteria will be returned

With no kwargs, it behavees identically to `all`

## Cheatsheet

    # Form 1
    Color = Object.define("Color", "RED", "GREEN", "BLUE")

    # Form 2
    Color = Object.define("Color", RED="ff0000", GREEN="00ff00", BLUE="0000ff")

    # Form 3
    Color = Object.define(
        "Color",
        RED=dict(hex="ff0000", like=True),
        GREEN=dict(hex="00ff00", like=True),
        BLUE=dict(hex="0000ff", like=False),
    )

    Object
        # Class
        objects                                 # Object Manager
        create(     cn,          **kwargs )     # create and register one object
        createmany(       *args, **kwargs )     # create and register many objects          (three forms)
        define(     name, *args, **kwargs )     # create a class with objects in one line   (three forms)

        # Instance
        __eq__                                  # compares canonical names
        __hash__                                # returns hash of canonical_name
        __len__                                 # returns length of canonical_name
        __repr__                                # returns canonical_name
        __str__                                 # returns canonical_name
        cn_lower                                # returns lower-cased canonical_name
        cn_title                                # returns titlized canonical_name  (FOO_BAR  ->  "Foo Bar")
        ordinal                                 # returns 1-based index representing creation order

    ObjectManager

        __contains__( cn_or_obj )               # returns True | False
        __getitem__(  cn_or_obj )               # returns obj | None
        __len__                                 # returns count of registered objects
        all                                     # returns list
        filter( func )                          # returns list of 0 or more objects after applying filter function
        first(  **kwargs )                      # returns obj | None
        get(    **kwargs )                      # returns obj or raises ValueError
        last(   **kwargs )                      # returns obj | None
        max_length                              # returns length of longest canonical_name
        random()                                # returns randomly-chosen obj
        select( **kwargs )                      # returns list of 0 or more objects

## Subclassing

If you want to add your own features to Object, just subclass it :

    class MyObject( Object ):
        def my_new_method( self ):
            ...

    Color = MyObject.define("Color", "RED", "GREEN", "BLUE")
    Color.RED.my_new_method()

That works well for defining a project-wide base class, but what if you just want a one-off class to add a feature to a specific object type in your collection?  Easy &mdash; just skip past `define`, which is just a helper method around `createmany`, and use `createmany` directly :

    class Planet( MyObject ):
        @property
        def circumference( self ):
            return self.diameter * 3.14

    Planet.createmany(
        EARTH=dict( diameter=12742 ),
        MARS=dict(  diameter=6794  ),
    )

    Planet.EARTH.circumference

## Bonus : ErrorSet

A Variation on the other theme for Python exceptions.  Declare a family of Exception classes in one line :

    from objects import ErrorSet

    APIError = ErrorSet("APIError", "CERTIFICATE_ERROR", "CONNECTION_ERROR", "VERSION_ERROR")

    raise APIError("...")
    raise APIError.VERSION_ERROR("...")

Catch the most specific errors:

    try:
        ...
    except APIError.VERSION_ERROR as e:
        ...

Or the whole family:

    try:
        ...
    except APIError as e:
        ...

_Notice The Difference &mdash; Objects are classes with instances attached, whereas ErrorSets are classes with subclasses attached_

## Bonus : Help for Django Users

Stop using Django
.
If you must use Django, I suggest adding the following to your personal Object base class :

    def django_pair(self):
        django_value = self.canonical_name
        django_label = self.label if hasattr(self, "label") else self.canonical_name
        return (django_value, django_label)

    @classmethod
    def choices( cls, filter=None ):
        objects = cls.objects.filter( filter ) if filter else cls.objects.all
        return [ obj.django_pair() for obj in objects ]

Then you can use Objects instead of Enums in model fields :

    color = models.CharField(
        choices    = Color.choices(),                                   # use all values
            -or-
        choices    = Color.choices( filter=lambda o: o != "BLUE" ),     # filter out some
        max_length = Color.objects.max_length,
        default    = Color.RED,
    )

## Bonus : Help for Graphene Users

Stop using Graphene

.

Seriously, it's really really bad

.

If you must use Graphene, I suggest adding the following to you personal Object base class:

    from functools import cache
    from graphene import Enum

    def graphene_pair( self ):
        graphene_name  = self.canonical_name
        graphene_value = self.canonical_name
        return ( graphene_name, graphene_value )

    def graphene_description( self ):
        if hasattr( self, "description" ):
            return self.description
        if hasattr( self, "label" ):
            return self.label
        return None

    @classmethod
    @cache
    def graphene( cls, name=None, filter=None ):
        name         = name or cls.__name__
        objects      = cls.objects.filter( filter ) if filter else cls.objects.all
        enum_items   = [ obj.graphene_pair() for obj in objects ]
        descriptions = { obj.graphene_pair()[ 0 ]: obj.graphene_description() for obj in objects }
    def description( enum_obj ):
            return descriptions[ enum_obj.name ] if enum_obj else cls.__doc__
        return graphene.Enum( name, enum_items, description=description )

Then you can use Objects instead of Enums and still generate Graphene enums from them :
    ColorEnum = Color.graphene()
    class Foo( graphene.ObjectType ):
        color = ColorEnum( required=True )
        ...