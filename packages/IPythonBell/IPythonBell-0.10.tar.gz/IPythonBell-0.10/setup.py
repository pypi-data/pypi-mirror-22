import platform

from distutils.core import setup


requirements = [
    'IPython (>=1.00)',
]

if platform.system() == 'Windows':
    requirements += ['winsound']

    if int(platform.release()) >= 10:
        requirements += ['win10toast']

setup(
    name='IPythonBell',
    version='0.10',
    packages=['ipython_bell',],
    license='MIT',
    author='Sam Whitehall',
    author_email='me@samwhitehall.com',
    url='http://www.github.com/samwhitehall/ipython-bell',
    description='IPython/Jupyter notebook magic to notify the programmer when a '
        'line/cell has completed execution',
    long_description=open('README.rst').read(),
    keywords='ipython jupyter notebook notification notification complete alert',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Framework :: IPython',
        'Natural Language :: English',
        'Topic :: Utilities',
    ],
    requires=requirements,
)
