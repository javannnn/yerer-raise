from setuptools import setup, find_packages

setup(
    name='yererraise',
    version='0.1.0',
    description='Hand-raising assistant for hybrid meetings',
    packages=find_packages(),
    install_requires=['requests', 'screeninfo'],
    entry_points={'console_scripts': ['yererraise=yererraise.app:main']},
)
