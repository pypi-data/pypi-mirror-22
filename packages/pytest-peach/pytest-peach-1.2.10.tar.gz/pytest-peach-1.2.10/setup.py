import os
from setuptools import setup

version = os.getenv('BUILDTAG', '0.0.0')

setup(
    name = 'pytest-peach',
    description = 'pytest plugin for fuzzing with Peach API Security',
    long_description = open('README.rst').read(),
    author = 'Peach Fuzzer, LLC',
    author_email = 'contact@peachfuzzer.com',
    url = 'http://peachfuzzer.com',
    version = version,
    
    py_modules = ['pytest_peach'],
    entry_points = {'pytest11': ['peach = pytest_peach']},
    install_requires = ['pytest>=2.8.7', 'peachweb-api==%s' % version],
    
    license = 'MIT',
    keywords = 'py.test pytest fuzzing peach',
    
    classifiers = [
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Topic :: Security',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Testing',
        'Topic :: Utilities',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ])

# end
