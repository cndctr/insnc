from setuptools import setup, find_packages

setup(
    name="insnc",
    version="0.1",
    packages=find_packages(),
    install_requires=["requests", "pandas", "openpyxl"],
    entry_points={
        "console_scripts": [
            "insnc = insnc.main:main"
        ]
    },
)
