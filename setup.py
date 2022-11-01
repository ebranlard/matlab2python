from setuptools import setup, find_packages

setup(
    name='matlab2python',
    version='1.1',
    description='matlab2python script from E. Branlard',
    url='http://github.com/ebranlard/matlab2python/',
    author='Emmanuel Branlard',
    author_email='lastname@gmail.com',
    license='MIT',
    python_requires=">=3.6",
    packages=find_packages(),
    install_requires=[
        'numpy',
        'ply', 
        'networkx',
        'matplotlib', 
        'pytest', 
        'scipy'
    ],
    zip_safe=False
)
