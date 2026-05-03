from setuptools import setup, find_packages

setup(
    name="text_discoloration",
    version="1.0.1",
    author="shiroko",
    author_email="3207774253@qq.com",
    description="Typewriter effect with colorful output, support random color and custom color.",
    long_description=open("README.md",encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6"
)
