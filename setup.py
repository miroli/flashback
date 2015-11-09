from distutils.core import setup
setup(
    name='flashback',
    packages=['flashback'],
    version='0.2',
    description='The handiest Flashback scraper in the game',
    author='Robin Linderborg',
    author_email='robin.linderborg@gmail.com',
    install_requires=[
        'beautifulsoup4==4.4.1',
        'requests==2.8.0'
    ],
    url='https://github.com/vienno/flashback',
    download_url='https://github.com/vienno/flashback/tarball/0.2',
    keywords=['flashback', 'scraping'],
    classifiers=[],
)
