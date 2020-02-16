import os
import traceback
from contextlib import contextmanager
from typing import ContextManager, Union
from time import time
from pathlib import Path
from tempfile import TemporaryFile

@contextmanager
def atomic_write(file: Union[str, os.PathLike], mode: str = "w", as_file: bool = True, **kwargs) -> ContextManager:
    """Write a file atomically

    :param file: str or :class:`os.PathLike` target to write
    :param mode: the mode in which the file is opened, defaults to "w" (writing in text mode)
    :param bool as_file:  if True, the yielded object is a :class:File.
        (eg, what you get with `open(...)`).  Otherwise, it will be the
        temporary file path string

    :param kwargs: anything else needed to open the file

    :raises: FileExistsError if target exists

    Example::

        with atomic_write("hello.txt") as f:
            f.write("world!")

    """

    if os.path.exists(file): raise FileExistsError("You must enter a unique destination. You entered '{}'".format(str(file)))

    # Get filetype
    file_extension = "".join(Path(file).suffixes)


    # Make a temporary file with the datetime as the name
    temp_file_name = str(time()).replace(".","")+"_tempfile"+file_extension

    # Open a new tempfile
    temp = open(temp_file_name, mode,**kwargs)

    try:
        # yield the temp file to permit writing as a ContextManager
        # if as_file:
        #     yield temp
        # else:
        #     yield temp_file_name

        yield (temp if as_file else temp_file_name)

    except Exception:
        # Print last exception
        traceback.print_exc()
        raise
    else:
        # In the following code we need to ensure that the tempfile is written to disk.
        # First, we flush the internal buffer.
        # Why? file.write() will return before the writing operation is actually complete.
        temp.flush()

        # Then we force syncronization of the file to the hard disk.
        # https://www.geeksforgeeks.org/python-os-fsync-method/
        os.fsync(temp.fileno())

        # Close the file.
        temp.close()

        # Rename it.
        os.rename(temp_file_name, file)
    finally:
        # If the temp file exists, then it was not renamed, and must be closed and deleted.
        if os.path.exists(temp_file_name):
            temp.close()
            os.remove(temp_file_name)
