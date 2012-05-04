from setuptools import setup, find_packages

version = '1.0dev'

install_requires = [
        'pyramid >=1.2',
        'rq',
        ]

tests_require = [
        'mock',
        ]

setup(name='pyramid_rq',
      version=version,
      description='Support using the rq queueing system with pyramid',
      long_description=open('README.rst').read() + '\n' +
                       open('CHANGES.rst').read(),
      classifiers=[
        'Framework :: Pylons',
        'Framework :: Pyramid',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        ],
      keywords='pyramid rq redis queueing',
      author='Wichert Akkerman',
      author_email='wichert@wiggynet',
      url='https://github.com/wichert/pyramid_rq/',
      license='BSD',
      packages=find_packages('src'),
      include_package_data=True,
      package_dir={'': 'src'},
      zip_safe=False,
      install_requires=install_requires,
      tests_require=tests_require,
      extras_require={
          'tests': tests_require,
      },
      test_suite='pyramid_rq'
      )
