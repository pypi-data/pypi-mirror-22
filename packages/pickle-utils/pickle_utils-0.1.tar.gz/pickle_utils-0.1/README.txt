Available functions:

load(filename_or_object):
    Load a Pickle file, from a file name or a file-like object. If the argument
    is a file name, it must end in ".pkl" or ".pkl.gz". In the second case the
    file will be compressed.

dump(data, filename_or_object): same as before but dump data to disk.

@memoize(filename, log_level=info):
    Decorator to memoize the output of a function to `filename` with pickle. The
    function will be executed only if `filename` does not exist.

Use `help(pickle_utils)` in an interactive session for slightly more detailed docs.
