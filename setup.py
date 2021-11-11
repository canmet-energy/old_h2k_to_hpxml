from distutils.core import setup


def readme():
    """Import the README.md Markdown file and try to convert it to RST format."""
    try:
        import pypandoc
        return pypandoc.convert('README.md', 'rst')
    except(IOError, ImportError):
        with open('README.md') as readme_file:
            return readme_file.read()


setup(
    name='h2k_hpxml',
    version='0.1',
    description='Create a hpxml from a h2k file',
    long_description=readme(),
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    url='https://github.com/canmet-energy/h2k_to_hpxml',
    author='Rasoul Asaee',
    author_email='rasoul.asaee@nrcan-rncan.gc.ca',
    license='GPL',
    packages=['src'],
    install_requires=[
        'pypandoc>=1.6'
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
