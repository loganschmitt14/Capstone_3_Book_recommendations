from setuptools import find_packages, setup

setup(
    name='src',
    packages=find_packages(include = ['src', 'setup_webdriver.*']),
    version='0.1.0',
    description='Building a book recommendation system in Python',
    author='Logan Schmitt',
    license='MIT',
)
