
import sys
import re
import os.path
from setuptools import setup


# reading package's version (same way sqlalchemy does)
with open(os.path.join(os.path.dirname(__file__), 'maryjane.py')) as v_file:
    package_version = re.compile(r".*__version__ = '(.*?)'", re.S).match(v_file.read()).group(1)


if sys.version_info < (3, 6, 0):
    print('Error: `Python < 3.6` is not supported.', file=sys.stdout)
    sys.exit(-1)


long_description = """
Simple Task runner and build tool.
"""

setup(
    name='maryjane',
    version=package_version,
    author='Vahid Mardani',
    author_email='vahid.mardani@gmail.com',
    url='http://github.com/pylover/maryjane',
    description='Python file watcher and task manager',
    long_description=long_description,
    install_requires=['watchdog'],
    py_modules=['maryjane'],
    entry_points={
        'console_scripts': [
            'maryjane = maryjane:main'
        ]
    },
    license='WTFPL',
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Development Status :: 4 - Beta',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development',
        'Topic :: Utilities'
        ]
    )
