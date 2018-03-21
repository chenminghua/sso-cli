from setuptools import setup

setup(
    author="minghua",
    author_email="minghua.cc@qq.com",
    name="tvsso-cli",
    version="0.0.2",
    license="MIT",
    url="https://minghua.online",
    py_modules=['sso',],
    install_requires=[
        'bs4',
        'requests',
        'demjson',
        'future'],
    description="SSCTV SSO User Manage System CLI Tools",
    entry_points={
        'console_scripts': ['tvsso-cli=sso:command_line_runner']
    }
)
