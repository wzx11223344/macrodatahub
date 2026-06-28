from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="macrodatahub",
    version="1.0.0",
    author="wzx11223344",
    author_email="3521257027@QQ.com",
    description="全球宏观经济数据自动化获取、清洗与可视化工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wzx11223344/macrodatahub",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pandas>=1.3.0",
        "requests>=2.25.0",
    ],
)
