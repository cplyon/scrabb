import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='scrabb',
    version='1.0',
    description='A simple, Scrabble-like game',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/cplyon/scrabb',
    author='Chris Lyon',
    author_email='chris@cplyon.ca',
    packages=setuptools.find_packages(),
    install_requires=['collections-extended'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
