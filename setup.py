from setuptools import setup

setup(
  name = "homophones",
  version = "1.0.0",
  author = "John Baber-Lucero",
  author_email = "pypi@frundle.com",
  description = ("Find homophones for a given word"),
  license = "GPLv3",
  url = "https://github.com/jbaber/homophones",
  packages = ['homophones'],
  package_data = {
    '': ['original_cmudict_files/cmudict-0.7b'],
  },
  include_package_data = True,
  install_requires = ['docopt', 'vlog'],
  tests_require=['pytest'],
  entry_points = {
    'console_scripts': ['homophones=homophones.homophones:main'],
  }
)
