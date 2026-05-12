"""
Setup configuration with optional Cython extension compilation.
Falls back to pre-compiled C files if Cython is not available or .pyx not found.
"""

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import sys
import os

HAS_CYTHON = False
extensions = []

try:
    from Cython.Build import cythonize
    HAS_CYTHON = True
except ImportError:
    pass


class BuildExtCommand(build_ext):
    """Custom build_ext command to handle optional Cython compilation."""
    
    def run(self):
        if not extensions:
            print("INFO: No extensions to compile")
            return
        try:
            build_ext.run(self)
        except Exception as e:
            print(f"WARNING: Build extension failed: {e}")
            print("Continuing without C extensions...")


# Define extensions - try Cython first, fallback to pre-compiled C
if HAS_CYTHON and os.path.exists("ALYODCLI/text_core.pyx"):
    print("Building Cython extension from .pyx")
    try:
        extensions = [
            Extension(
                "ALYODCLI.text_core",
                ["ALYODCLI/text_core.pyx"],
                language="c",
                extra_compile_args=["-O3"] if sys.platform != "win32" else ["/O2"],
            )
        ]
        extensions = cythonize(extensions, language_level="3")
    except Exception as e:
        print(f"WARNING: Cythonization failed: {e}")
        extensions = []

elif os.path.exists("ALYODCLI/text_core.c"):
    print("Building C extension from pre-compiled .c")
    extensions = [
        Extension(
            "ALYODCLI.text_core",
            ["ALYODCLI/text_core.c"],
            language="c",
            extra_compile_args=["-O3"] if sys.platform != "win32" else ["/O2"],
        )
    ]
else:
    print("INFO: No Cython source found. Extensions will be skipped.")


setup(
    ext_modules=extensions,
    cmdclass={"build_ext": BuildExtCommand},
)
