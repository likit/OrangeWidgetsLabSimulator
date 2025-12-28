from setuptools import setup, find_namespace_packages

setup(
    name="Orange3-LabDES",
    version="0.1.0",
    description="Discrete-event medical laboratory simulation widgets for Orange3",
    author="Likit Preeyanon",
    author_email="likit.pre@mahidol.ac.th",
    url="https://github.com/likit/OrangeWidgetsLabSimulator",
    license="MIT",

    packages=find_namespace_packages(include=["orangecontrib.*"]),
    include_package_data=True,

    install_requires=[
        "Orange3>=3.35",
        "simpy>=4.0",
        "numpy",
    ],

    entry_points={
        "orange.widgets": [
            "DES = orangecontrib.des.widgets",
        ],
    },

    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Orange",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Simulation",
    ],

    python_requires=">=3.12",
)
