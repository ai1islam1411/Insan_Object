class BaseError( Exception ):
    ...


def ErrorSet( parent_name, *child_names ):

    # create the class representing the set of errors
    parent_class = type(
        parent_name,                    # class name
        ( BaseError, ),                 # parent class
        dict(                           # class attributes
            errors=dict(),              # ( child_name: child_class )
        ),
    )

    # create the class for each error
    for child_name in child_names:

        child_class = type(
            child_name,                 # class name
            ( parent_class, ),          # parent class
            dict(                       # class attributes
                name=child_name,        # for convenience  (alternative to __name__)
                parent=parent_class,    # doubly-linked for convenience
            ),
        )

        # add to parent class as attribute
        setattr( parent_class, child_name, child_class )

        # add to index for lookup & iteration
        parent_class.errors[ child_name ] = child_class

    return parent_class
