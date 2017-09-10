import setuptools

setuptools.setup(
    name='alfred-datetime',
    version='0.0.1',
    url='https://github.com/kdeal/alfred-datetime',

    author='Kyle Deal',
    author_email='kdeal@kyledeal.com',

    description='Handle datetime formatting and math with alfred',
    long_description=open('README.md').read(),

    packages=setuptools.find_packages('.', exclude=('tests*',)),

    install_requires=['requests'],
    entry_points={
        'console_scripts': [
            'alfred-datetime = alfred_datetime.cli:main',
        ]
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
