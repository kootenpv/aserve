from setuptools import find_packages
from setuptools import setup

MAJOR_VERSION = '0'
MINOR_VERSION = '0'
MICRO_VERSION = '7'
VERSION = "{}.{}.{}".format(MAJOR_VERSION, MINOR_VERSION, MICRO_VERSION)

setup(name='mocka',
      version=VERSION,
      description="Mocka mocks APIs",
      url='https://github.com/kootenpv/mocka',
      author='Pascal van Kooten',
      author_email='kootenpv@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'aiohttp',
      ],
      entry_points={
          'console_scripts': ['mocka = mocka.mocka:main']
      },

      classifiers=[
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Operating System :: Microsoft',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Unix',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.5',
          'Topic :: Software Development',
          'Topic :: Software Development :: Build Tools',
          'Topic :: Software Development :: Debuggers',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: System :: Software Distribution',
          'Topic :: System :: Systems Administration',
          'Topic :: Utilities'
      ],
      zip_safe=False,
      platforms='any')
