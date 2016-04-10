

def retry(count):
    """
    This wrapper is used for retry the function(f) if has error,
    will continue for count times
    """
    def _f(f):
        def _retry(*args, **kwargs):
            for _ in range(count):
                try:
                    ret = f(*args, **kwargs)
                    return ret
                except Exception, e:
                    _e = e
            raise _e
        return _retry
    return _f
