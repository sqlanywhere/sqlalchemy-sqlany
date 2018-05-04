import os,re
from setuptools import setup

with open( os.path.join( os.path.dirname(__file__), 'sqlalchemy_sqlany',
                              '__init__.py' ) ) as v:
    VERSION = re.compile(r".*__version__ = '(.*?)'", re.S).match(v.read()).group(1)

setup(
    name = 'sqlalchemy_sqlany'
    , version = VERSION
    , description='SAP Sybase SQL Anywhere dialect for SQLAlchemy'
    , long_description=open( 'README.rst' ).read()
    , keywords='SAP Sybase SQLAnywhere SQLAlchemy'
    , author='Graeme Perrow'
    , author_email='graeme.perrow@sap.com'
    , install_requires=['sqlanydb >= 1.0.6']
    , packages = ['sqlalchemy_sqlany','test']
    , url='https://github.com/sqlanywhere/sqlalchemy-sqlany'
    , tests_require=['nose >= 0.11']
    , test_suite='nose.collector'
    , zip_safe = False
    , entry_points={
        'sqlalchemy.dialects': [
            'sqlalchemy_sqlany = sqlalchemy_sqlany:base.dialect'
            ]
        }
    , license='Apache 2.0'
    , classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.4',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Database',
        'Topic :: Software Development :: Libraries :: Python Modules'
        ]

)
