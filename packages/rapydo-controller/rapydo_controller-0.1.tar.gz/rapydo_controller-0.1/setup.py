
import os
import codecs
from rapydo.do import __version__

from distutils.core import setup
# from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    return codecs.open(os.path.join(here, *parts), 'r').read()


setup(
    name='rapydo_controller',
    description='Do development and deploy with the RAPyDo framework',
    # long_description=__doc__,
    long_description=read('README.rst'),
    version=__version__,
    author="Paolo D'Onorio De Meo",
    author_email='p.donorio.de.meo@gmail.com',
    url='https://github.com/rapydo/do',
    license='MIT',
    packages=[
        'rapydo.do',
    ],
    package_data={
        'rapydo.do': [
            'argparser.yaml'
        ],
    },
    python_requires='>=3.4',
    entry_points={
        'console_scripts': [
            'rapydo=rapydo.do.__main__:main',
        ],
    },
    install_requires=[
        "rapydo-utils",
        "requests==2.11.1",
        "docker",
        "docker-compose>=1.13",
        "gitpython",
        "dockerfile-parse",
        "better_exceptions"
    ],
    # tests_require=[  # from PIP code
    #     'pytest',
    #     'mock',
    #     'pretend',
    #     'scripttest>=1.3',
    #     'virtualenv>=1.10',
    #     'freezegun',
    # ],
    # extras_require={
    #     'testing': tests_require,
    # },
    classifiers=[
        'Programming Language :: Python',
        'Intended Audience :: Developers',
    ],
    keywords=['http', 'api', 'rest', 'web', 'backend', 'rapydo'],
    zip_safe=False,
)
