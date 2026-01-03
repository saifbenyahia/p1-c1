from setuptools import setup, find_packages

setup(
    name="p1-c1-crypto-analyzer",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.21.0",
        "scikit-learn>=1.0.0",
        "pandas>=1.3.0",
        "joblib>=1.1.0",
        "nltk>=3.6.0",
        "click>=8.0.0",
        "rich>=10.0.0",
    ],
    entry_points={
        "console_scripts": [
            "crack-caesar=cli.crack_caesar:main",
        ],
    },
)