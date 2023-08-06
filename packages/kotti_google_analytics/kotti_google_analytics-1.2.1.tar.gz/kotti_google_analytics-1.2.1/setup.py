import os

from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.rst')).read()
except IOError:
    README = ''
try:
    CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()
except IOError:
    CHANGES = ''

version = "1.2.1"

install_requires = [
    'Kotti>=1.0.0',
    'unidecode',
    'googleanalytics>=0.23.0',
    'kotti_controlpanel>=1.0.9'
]


setup(
    name='kotti_google_analytics',
    version=version,
    description="Google Analytics for Kotti",
    long_description='\n\n'.join([README, CHANGES]),
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "License :: Repoze Public License",
    ],
    author='Oshane Bailey',
    author_email='b4.oshany@gmail.com',
    url='https://github.com/b4oshany/kotti_google_analytics',
    keywords=('google analytics kotti web cms wcms pylons pyramid'
              'sqlalchemy bootstrap tracking users'),
    license="BSD-derived (http://www.repoze.org/LICENSE.txt)",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    tests_require=[],
    entry_points={
        'fanstatic.libraries': [
            'kotti_google_analytics = kotti_google_analytics.fanstatic:library',
        ],
    },
    extras_require={},
)
