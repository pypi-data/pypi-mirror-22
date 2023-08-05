from setuptools import setup, find_packages
import codecs
import os
from commands import (docker_build, docker_start, docker_stop, setup_riak,
                      create_bucket_types, Test)


HERE = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    """
    Build an absolute path from *parts* and and return the contents of the
    resulting file.  Assume UTF-8 encoding.
    """
    with codecs.open(os.path.join(HERE, *parts), "rb", "utf-8") as f:
        return f.read()

setup(
    name='aioriak',
    version='0.1.8',
    description='Async implementation of Riak DB python client',
    long_description=read("README.rst"),
    author='Makc Belousov',
    author_email='m.belousov@rambler-co.ru',
    url='https://github.com/rambler-digital-solutions/aioriak',
    keywords='riak asyncio client',
    packages=find_packages(exclude=('*.tests',)),
    include_package_data=True,
    zip_safe=False,
    license='MIT',
    install_requires=[
        'riak==2.7.0',
    ],
    tests_require=['nose==1.3.7',
                   'coverage==4.0.3'],
    cmdclass={
        'test': Test,
        'docker_build': docker_build,
        'docker_start': docker_start,
        'docker_stop': docker_stop,
        'setup_riak': setup_riak,
        'create_bucket_types': create_bucket_types,
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Database',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
