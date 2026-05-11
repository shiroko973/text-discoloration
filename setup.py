from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="text_discoloration",
    version="3.0.1",
    author="shiroko",
    author_email="3207774253@qq.com",
    description="终端彩色工具 + 安全密钥生成",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shiroko973/text-discoloration",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    license="MIT",
    entry_points={
        "console_scripts": [
            "tcd = text_discoloration.__main__:main",
            "ra = text_discoloration.cli:main",
        ]
    },
)