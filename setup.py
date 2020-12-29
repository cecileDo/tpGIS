from setuptools import setup, find_packages
import os

def setup_package():
    

    packages = find_packages()

    package_dir = {}
    for p in packages:
        package_dir[p] = p.replace('.','/')

    with open('requirements.txt') as reqs:
        requirements = [r.replace('\n','') for r in reqs]

    setup(

        packages=packages,
        package_dir=package_dir,

        install_requires=requirements,

        long_description="""
        Python module for tp gis
        """,
    )


if __name__ == "__main__":
    setup_package()
