from objects.functools import cached_class_property
from objects.object_manager import ObjectManager

class Object:

    ##
    ##  Class
    ##


    @cached_class_property
    def objects( cls ):
        return ObjectManager( cls )


    @classmethod
    def create( cls, canonical_name, **kwargs ):

        # create instance
        obj = cls( canonical_name, **kwargs )

        # add to class as attribute
        setattr( cls, canonical_name, obj )

        # add to ObjectManager
        cls.objects._append( obj )

        return obj


    # Form 1:  createmany( "cn1", "cn2", ... )
    # Form 2:  createmany( cn1=label1, cn2=label2, ... )
    # Form 3:  createmany( cn1=dict( attr1=val1, attr2=val2 ), ... )
    @classmethod
    def createmany( cls, *args, **kwargs ):

        # Form 1
        for arg in args:
            assert isinstance( arg, str )
            cls.create( arg )

        for cn, payload in kwargs.items():

            # Form 2
            if isinstance( payload, str ):
                cls.create( cn, label=payload )

            # Form 3
            elif isinstance( payload, dict ):
                cls.create( cn, **payload )

            else:
                raise Exception( f"invalid payload - {type(payload)}:{payload}" )


    @classmethod
    def define( cls, name, *args, **kwargs ):

        # create object class
        subcls = type(
            name,           # class name
            ( cls, ),       # parent class
            dict(),         # class attributes
        )

        # create object instances
        subcls.createmany( *args, **kwargs )

        return subcls


    ##
    ##  Instance
    ##


    def __init__( self, canonical_name, **kwargs ):

        # set cn
        self.canonical_name = canonical_name

        # set arbitrary attributes
        for k, v in kwargs.items():
            setattr( self, k, v )


    def __eq__( self, other ):
        return self.canonical_name == str( other )


    def __hash__( self ):
        return hash( self.canonical_name )


    def __len__( self ):
        return len( self.canonical_name )


    def __repr__(self):
        return self.canonical_name  # TODO: better


    def __str__(self):
        return self.canonical_name


    @property
    def cn_lower( self ):
        return self.canonical_name.lower()


    @property
    def cn_title( self ):
        return self.canonical_name.replace( "_", " " ).title()


    @property
    def ordinal( self ):
        return self.objects._select().index( self ) + 1


    def _match( self, **kwargs ):
        for k, v in kwargs.items():
            assert hasattr( self, k )
            if getattr( self, k ) != v:
                return False
        return True
