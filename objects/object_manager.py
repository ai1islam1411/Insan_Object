from copy import deepcopy
from random import randrange

class ObjectManager:

    def __init__( self, object_class ):
        self.object_class = object_class
        self._objects = {}


    def __contains__( self, cn_or_obj ):
        return str( cn_or_obj ) in self._objects


    def __getitem__( self, cn_or_obj ):
        return deepcopy( self._objects.get( str( cn_or_obj ) ) )


    def __len__( self ):
        return len( self._objects )


    @property
    def all( self ):
        return self.select()


    def filter( self, func ):
        assert callable( func )
        return deepcopy( [ obj for obj in self._select() if func( obj ) ] )


    def first( self, **kwargs ):
        results = self._select( **kwargs )
        return deepcopy( results[ 0 ] ) if results else None


    def get( self, **kwargs ):
        results = self.select( **kwargs )
        if len( results ) != 1:
            raise ValueError( f"select({kwargs}) found {len(results)} results instead of 1" )
        return results[ 0 ]


    def last( self, **kwargs ):
        results = self._select( **kwargs )
        return deepcopy( results[ -1 ] ) if results else None


    @property
    def max_length( self ):
        if self._objects:
            return max( len( obj ) for obj in self._select() )
        return 0


    def random( self ):
        index = randrange( 0, len( self ) )
        return deepcopy( self._select()[ index ] )


    def select( self, **kwargs ):
        return deepcopy( self._select( **kwargs ) )


    def _append( self, obj ):
        assert isinstance( obj, self.object_class )
        self._objects[ obj.canonical_name ] = obj


    def _select( self, **kwargs ):
        objs = list( self._objects.values() )
        return [ obj for obj in objs if obj._match( **kwargs ) ]
