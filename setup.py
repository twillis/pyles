"""
opinions pyled on top of a nice foundation of python hotness
"""
from setuptools import setup, find_packages
version = "0.0"

packages = []

setup(name="pyles",
      version=version,
      description="",
      long_description="""\
      """,
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords="",
      author="Thomas G. Willis",
      author_email="me@twillis.me",
      url="",
      license="BSD",
      packages=find_packages(exclude=["tests", ]),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          "jinja2",
          "colander",
          "setuptools>=1.0"
      ],
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      pyles = pyles.scripts.command:main
      """,
      )
