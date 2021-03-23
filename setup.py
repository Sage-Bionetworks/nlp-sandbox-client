import os
import setuptools


def read(rel_path: str) -> str:
    """Read file"""
    # type: (str) -> str
    here = os.path.abspath(os.path.dirname(__file__))
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with open(os.path.join(here, rel_path)) as fp:
        return fp.read()


def get_version(rel_path: str) -> str:
    """Get version from __init__.py: following pip setup.py example
    https://github.com/pypa/pip/blob/master/setup.py#L11
    """
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            # __version__ = "0.9"
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    # basic
    name='nlpsandbox-client',
    version=get_version("nlpsandboxclient/__init__.py"),
    # packages=setuptools.find_packages(exclude=["tests", "tests.*"]),
    # py_modules=['hello'],
    # scripts=['bin/nlp-evaluate'],

    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': ['nlp-cli=nlpsandboxclient.cli.__main__:main']
    },

    # requirements
    python_requires='>=3.6.*',
    install_requires=[
        'certifi >= 14.05.14',
        'click >= 7.1.2',
        'jsonschema >= 3.2.0',
        'python_dateutil >= 2.5.3',
        'setuptools >= 21.0.0',
        'six >= 1.10',
        'synapseclient >= 2.2.0',
        'urllib3 >= 1.15.1',
        'nulltype >= 2.3.1'
    ],

    # metadata to display on PyPI
    description='NLP Sandbox Client Library for Python',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/nlpsandbox',
    author='The NLP Sandbox Team',
    author_email='thomas.schaffter@sagebionetworks.org',
    license='Apache',
    project_urls={
        "Source Code": "https://github.com/nlpsandbox/nlpsandbox-client",
        "Bug Tracker": "https://github.com/nlpsandbox/nlpsandbox-client/issues",
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Software Development :: Libraries',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Bio-Informatics'
    ]
)
