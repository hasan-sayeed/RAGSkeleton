"""
    Setup file for rag_skeleton.
    Use setup.cfg to configure your project.

    This file was generated with PyScaffold 4.6.
    PyScaffold helps you to put up the scaffold of your new Python project.
    Learn more under: https://pyscaffold.org/
"""

# from setuptools import setup

# if __name__ == "__main__":
#     try:
#         setup(use_scm_version={"version_scheme": "no-guess-dev"})
#     except:  # noqa
#         print(
#             "\n\nAn error occurred while building the project, "
#             "please ensure you have the most updated version of setuptools, "
#             "setuptools_scm and wheel with:\n"
#             "   pip install -U setuptools setuptools_scm wheel\n\n"
#         )
#         raise

from setuptools import setup, find_packages

if __name__ == "__main__":
    try:
        setup(
            use_scm_version={"version_scheme": "no-guess-dev"},
            install_requires=[
                "numpy",
                "scipy==1.14.1",
                "tqdm==4.67.0",
                "click==8.1.7",
                "langchain==0.3.7",
                "langchain-community==0.3.5",
                "langchain-chroma==0.1.4",
                "langchain-huggingface==0.1.2",
                "pymupdf==1.24.13",
                "sentence-transformers==3.2.1",
            ],
            entry_points={
                "console_scripts": [
                    "rag_skeleton=src.rag_skeleton.run:main",
                ],
            },
        )
    except Exception as e:
        print(
            "\n\nAn error occurred while building the project. Please ensure "
            "you have the most updated versions of setuptools, setuptools_scm, and wheel with:\n"
            "   pip install -U setuptools setuptools_scm wheel\n\n"
        )
        raise e
