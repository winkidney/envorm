import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))


install_requires = []


setup(
    name='envorm',
    version='0.0.2',
    packages=find_packages(here, exclude=['tests']),
    url='https://github.com/winkidney/envorm',
    license='MIT',
    description='An ORM-like interface for environment variables.',
    install_requires=install_requires,
)
