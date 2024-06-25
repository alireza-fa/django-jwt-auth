#!/usr/bin/env python3
from io import open

from setuptools import find_packages, setup


def read(f):
    with open(f, 'r', encoding='utf-8') as file:
        return file.read()


setup(
    name='d_jwt_auth',
    version="0.0.6",
    url='https://github.com/alireza-fa/django-jwt-auth',
    license='MIT',
    description='django-jwt-auth is an application for authenticating users with jwt in Django.',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    author='Alireza Feizi',
    author_email='alirezafeyze44@gmail.com',
    packages=find_packages(exclude=['tests*', 'config*', 'accounts*', 'manage.py']),
    include_package_data=True,
    install_requires=["django>=3.2", "djangorestframework>=3.0", "djangorestframework-simplejwt>=5.3.0", "pycryptodome>=3.0"],
    python_requires=">=3.9",
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.0',
        'Framework :: Django :: 4.1',
        'Framework :: Django :: 4.2',
        'Framework :: Django :: 5.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet :: WWW/HTTP',
    ],
    project_urls={
        'Source': 'https://github.com/alireza-fa/django-jwt-auth',
    },
)
