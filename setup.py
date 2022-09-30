import setuptools
import tiner

with open('README.md', 'r') as fh:
    long_description = fh.read()


setuptools.setup(
    name='tiner',
    url=tiner.__url__,
    version=tiner.__version__,
    author=tiner.__author__,
    description='Block-wise timer for Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['tiner'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=['tabulate']
)
