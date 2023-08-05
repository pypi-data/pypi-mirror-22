from setuptools import setup

fp = open('./bristol/version.py')
exec(fp.read())

setup(
      name='bristol',
      version=__version__,
      description="bristol is set of random matrix tools with parallel processing capabilities. Current modules: circular ensembles, CUE, COE and CSE.",
      url="https://github.com/msuzen/bristol",
      author='M.Suzen, C.Garbers',
      author_email='suzen@acm.org',
      license= 'GPL-3',
      packages=['bristol'],
      install_requires=['numpy >= 1.11', 'future >= 0.16.0'],
      test_suite="test",
      zip_safe=False
     )
