"""functions in this file prefixed with handle will be picked up by
pyles and handed args for further processing
"""


def create_project(*a, **kw):
    """
    create a project
    """
    print((a, kw))
    print("i would create a project")


def create_view(*a, **kw):
    """
    create a view
    """
    print((a, kw))
    print("i would create a view")


def create_model(*a, **kw):
    """
    create a model
    """
    print((a, kw))
    print("I would create a model")
