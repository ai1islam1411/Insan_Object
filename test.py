#!/usr/bin/env python3

from objects.errorset import BaseError, ErrorSet
from objects.object import Object


print("testing...")


##
##  Object
##


# Form 1
# ------

Color1 = Object.define("Color1", "RED", "GREEN", "BLUE", "FOO_BAR")  # FOO_BAR -> for testing titlecase
assert issubclass( Color1,     Object )
assert isinstance( Color1.RED, Color1  )
assert Color1.RED.canonical_name == "RED"

# Form 2
# ------

Color2 = Object.define( "Color2", RED="ff0000", GREEN="00ff00", BLUE="0000ff" )
assert Color2.RED.canonical_name == "RED"
assert Color2.RED.label == "ff0000"

# Form 3
# ------

Color3 = Object.define(
    "Color3",
    RED=dict( foo=42, like=True ),
    GREEN=dict( foo=43, like=True ),
    BLUE=dict( foo=43, like=False ),
)
assert Color3.RED.canonical_name == "RED"
assert Color3.RED.foo == 42

# Instance Methods
# ----------------

# __eq__
assert Color1.RED == Color1.RED
assert Color1.RED == Color2.RED         # uses value, not identity
# __len__
assert len( Color1.RED ) == 3
# __repr__
assert repr( Color1.RED ) == "RED"
# __str__
assert str( Color1.RED ) == "RED"
# cn_lower
assert Color1.RED.cn_lower == "red"
# cn_title
assert Color1.RED.cn_title == "Red"
assert Color1.FOO_BAR.cn_title == "Foo Bar"
# ordinal
assert Color1.BLUE.ordinal == 3


##
##  ObjectManager
##


# __contains__
assert Color1.RED in Color1.objects
assert Color2.RED in Color1.objects     # uses value, not identity
# __getitem__
assert Color1.objects["RED"] == Color1.objects[Color1.RED] == Color1.RED
# __len__
assert len( Color1.objects ) == 4
# all
assert Color1.objects.all[ 0 ] == Color1.RED
# first
assert Color1.objects.first() == Color1.RED
# last
assert Color1.objects.last() == Color1.FOO_BAR
# max_length
assert Color1.objects.max_length == 7
# random
assert Color1.objects.random() in Color1.objects

# Select-Based Methods
# --------------------

assert len( Color3.objects.select() ) == 3
assert len( Color3.objects.select( foo=42 ) ) == 1
assert len( Color3.objects.select( foo=99 ) ) == 0
assert len( Color3.objects.select( like=True ) ) == 2
assert len( Color3.objects.select( like=False ) ) == 1
assert len( Color3.objects.select( like=True, foo=43 ) ) == 1

assert len( Color3.objects.filter( lambda o: o.like ) ) == 2
assert Color3.objects.get( foo=42 ) == Color3.RED
try:
    Color3.objects.get( foo=99 )
    assert False
except ValueError as e:
    ...


##
##  ErrorSet
##


FooError = ErrorSet( "FooError", "ERROR1", "ERROR2" )

assert issubclass( FooError,        BaseError )
assert issubclass( FooError.ERROR1, FooError  )
assert FooError.errors["ERROR1"] is FooError.ERROR1

try:
    raise FooError.ERROR1( "oh no" )
except FooError as e:
    ...