import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()


vars2find = ['__author__', '__version__', '__url__']
varstiner = {}
with open("./tiner/__init__.py") as f:
    for line in f.readlines():
        for v in vars2find:
            if line.startswith(v):
                line = line.replace(" ", '').replace(
                    "\"", '').replace("\'", '').strip()
                varstiner[v] = line.split('=')[1]

setuptools.setup(
    name='tiner',
    url=varstiner['__url__'],
    version=varstiner['__version__'],
    author=varstiner['__author__'],
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
