from distutils.core import setup
setup(
    name='testgres',
    packages=['testgres'],
    version='0.3.1',
    description='Testing utility for postgresql and its extensions',
    license='PostgreSQL',
    author='Ildar Musin',
    author_email='zildermann@gmail.com',
    url='https://github.com/postgrespro/testgres',
    keywords=['testing', 'postgresql'],
    classifiers=[],
    install_requires=["pg8000", "six"]
)
