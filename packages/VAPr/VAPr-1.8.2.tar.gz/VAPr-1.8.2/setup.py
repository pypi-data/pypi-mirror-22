from setuptools import setup

setup(name='VAPr',
      version='1.8.2',
      description='Package for NoSQL variant data storage, annotation and prioritization.',
      url='https://github.com/ucsd-ccbb/VAPr',
      author='Carlo Mazzaferro',
      author_email='cmazzafe@ucsd.edu',
      install_requires=['pymongo', 'myvariant', 'pyvcf', 'watchdog', 'pandas'],
      license='MIT',
      packages=['VAPr'],
      zip_safe=False)
