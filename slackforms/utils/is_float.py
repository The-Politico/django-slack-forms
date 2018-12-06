def is_float(string):
    """
    Return whether or not a string is a parseable float.
    """
    try:
        float(string)
        return True
    except ValueError:
        return False
