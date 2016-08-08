import sys

from setuptools import setup

if sys.version_info[0] < 3:
    sys.exit("Naarad is only supported on Python 3 \n"
             "Current Python version: %d.%d" % sys.version_info[:2])

setup(name='naarad',
      version='0.0.1',
      description='Brings public facebook pages together',
      author='Harsh Gupta',
      author_email='mail@hargup.in',
      license='AGPL',
      packages=['naarad'],
      entry_points={
          'console_scripts': ['naarad = naarad.main:main']
          },
      install_requires=['facepy', 'jinja2']
)
