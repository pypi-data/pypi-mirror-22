import attr


@attr.s
class Error(object):
    """
    Represents an error found validating against the schema.
    """
    message = attr.ib()
    pointer = attr.ib(default=None)
