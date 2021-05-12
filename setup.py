from setuptools import find_packages
from setuptools import setup


setup(
    author="Henri Kestiö",
    author_email="henri.kestio@gmail.com",
    name="improvement-api",
    packages=find_packages(exclude=["tests"]),
    platforms=["POSIX"],
)
