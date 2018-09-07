import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


setup(
    name='acdh-django-sirad',
    version='0.1.0',
    packages=find_packages(
        exclude=['sirad/__pycache__']),
    include_package_data=True,
    license='MIT License',  # example license
    description='Django App to create a django-app out of a SIRAD Package.',
    long_description=README,
    url='https://github.com/acdh-oeaw/acdh-django-sirad',
    author='Peter Andorfer',
    author_email='peter.andorfer@oeaw.ac.at',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.0',  # replace "X.Y" as appropriate
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'lxml>=4.2.4',
        'Django>=2.0.4,<3',
        'Jinja2>=2.10',
        'pandas>=0.23.0',
    ]
)
