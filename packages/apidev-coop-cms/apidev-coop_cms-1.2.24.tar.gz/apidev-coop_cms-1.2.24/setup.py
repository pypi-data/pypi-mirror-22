#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""package the lib"""

try:
    from setuptools import setup, find_packages
except ImportError:
    import ez_setup
    ez_setup.use_setuptools()
    from setuptools import setup, find_packages

VERSION = __import__('coop_cms').__version__

import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='apidev-coop_cms',
    version=VERSION,
    description='Small CMS built around a tree navigation open to any django models',
    packages=find_packages(),
    include_package_data=True,
    author='Luc Jean',
    author_email='ljean@apidev.fr',
    license='BSD',
    zip_safe=False,
    install_requires=[
        'django >= 1.8, <1.10',
        'django-floppyforms',
        'django-extensions',
        'sorl-thumbnail',
        'apidev-coop_colorbox >= 1.2.7',
        'apidev-coop_bar >= 1.3.2',
        'coop_html_editor >= 1.0.6',
        'feedparser',
        'beautifulsoup4',
        'django-filetransfers',
        'model_mommy',
        'Pillow',
        'unicode-slugify == 0.1.3',
    ],
    #dependency_links=[
    #    'git+https://github.com/ljean/coop_html_editor.git@73e067b3505a193c6244015fe606c30d98bb18de#egg=coop_html_editor',
    #],
    long_description=open('README.rst').read(),
    url='https://github.com/ljean/coop_cms/',
    download_url='https://github.com/ljean/coop_cms/tarball/master',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
        'Natural Language :: English',
        'Natural Language :: French',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
)
