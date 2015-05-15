from setuptools import setup, find_packages

setup(
  name='suropy',
  version='0.1',
  url='http://github.com/signal/suropy/',
  license='Apache 2.0',
  author='Stephen Mullins',
  author_email='smullins7@gmail.com',
  description='A Suro client for Python.',
  long_description=__doc__,
  packages=find_packages(),
  include_package_data=True,
  zip_safe=False,
  platforms='any',
  install_requires=['thrift==0.9.2'],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Environment :: Server Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.7',
    'Topic :: System :: Monitoring',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Utilities'
  ]
)
