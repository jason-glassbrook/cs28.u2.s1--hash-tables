############################################################


def int_min(*args, **kwargs):

    return int(min(filter(None, args), **kwargs))


def int_max(*args, **kwargs):

    return int(max(filter(None, args), **kwargs))
