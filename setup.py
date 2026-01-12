"""jvlink-db-python パッケージのセットアップスクリプト"""

from setuptools import find_packages, setup

setup(
    name="jvlink-db-python",
    version="0.1.0",
    packages=find_packages(exclude=["test*"]),
    python_requires=">=3.8",
)
