import os
from setuptools import setup

setup(
    name = 'peachweb-api',
    description = 'Peach Web Proxy API module',
    long_description = open('README.rst').read(),
    author = 'Peach Fuzzer, LLC',
    author_email = 'contact@peachfuzzer.com',
    url = 'http://peachfuzzer.com',
    version = os.getenv('BUILDTAG', '0.0.0'),
    
    py_modules = ['peachproxy'],
    install_requires = ['requests>=2.11'],
    
    license = 'MIT',
    keywords = 'peach fuzzing security test rest',
    
    classifiers = [
        'Development Status :: 4 - Beta',
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
