"""
from distutils.core import setup
from Cython.Build import cythonize

setup(ext_modules=cythonize("call_eztrans.pyx", compiler_directives={"language_level": 3}))
"""
import sys
import multiprocessing
from pyximport import install

install()
import call_eztrans


if __name__ == "__main__":
    if sys.argv[0][-4:] == ".exe":
        setattr(sys, "frozen", True)
    multiprocessing.freeze_support()
    call_eztrans.main("새 폴더")


# call_eztrans()
