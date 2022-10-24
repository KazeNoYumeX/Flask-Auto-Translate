from setuptools import setup, find_packages

from Flask_Auto_Translate import __version__

setup(
    name='Flask_Auto_Translate',
    version=__version__,
    author='www.github.com/KazeNoYumeX',
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.10'
)
