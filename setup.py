from setuptools import find_packages, setup

setup(
    name='MobileSylva',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'pillow',
        'pygame',
        'tkinter',
        'sqlite3',
        'openai',
        'google-cloud-speech'
    ],
)