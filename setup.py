import os
from setuptools import setup
from collections import deque

from Cython.Build import cythonize


def find_scripts() -> deque:
    scripts = deque()
    for path, dirs, files in os.walk('unnamed'):
        print(f'current path: {path}')
        for file in files:
            if file.endswith(('.py', '.pyx', '.pxd')):
                filepath = os.path.join(path, file)
                print(f'found file {filepath}')
                scripts.append(filepath)
    print(scripts)
    return scripts


setup(
    name='unnamed-launcher',
    ext_modules=cythonize(
        find_scripts(),
        compiler_directives={'language_level': '3'}
    ),
    zip_safe=False,
)
