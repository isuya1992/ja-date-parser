from setuptools import setup, find_packages


def _requires_from_file(filename):
    return open(filename).read().splitlines()


setup(
    name="ja-date-parser",
    version="0.2.0",
    license="MIT",
    description="Package which offers handling to Japanese date format strings.",
    author="isuya1992",
    url="https://github.com/isuya1992/ja-date-parser",
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    py_modules=["jadtparser"],
    include_package_data=True,
    zip_safe=False,
    install_requires=_requires_from_file("requirements.txt"),
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "pytest-cov"]
)
