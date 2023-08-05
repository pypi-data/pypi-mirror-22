
from setuptools import setup, find_packages

NAME = 'batchcompute-cli'
VERSION= '1.3.12a6'

setup(
    name = NAME,
    version =  VERSION,
    keywords = ('batchcompute-cli','batchcompute','bcs'),
    description = 'Alicloud BatchCompute command line interface',
    license = 'MIT License',

    url = 'http://www.aliyun.com/product/batchcompute',
    author = 'guangchun.luo',
    author_email = 'guangchun.luo@alibaba-inc.com',

    packages = find_packages('src'),
    package_dir = {'' : 'src'},

    package_data = {
       'batchcompute_cli': ['templates/*.zip','templates/*.py']
    },

    platforms = 'any',

    install_requires = ['batchcompute==2.0.8a6','oss2','terminal','blessings','drawille'],
    entry_points='''
        [console_scripts]
        batchcompute=batchcompute_cli.cli:main
        bcs=batchcompute_cli.cli:main
    '''
)
