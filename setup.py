from setuptools import setup

__version__ = "0.0.1"

# Importing the "multiprocessing" module is required for the "nose.collector".
# See also: http://bugs.python.org/issue15881#msg170215
try:
    import multiprocessing
except ImportError:
    pass

# Define the test runner.
# See also:
# http://fgimian.github.io/blog/2014/04/27/running-nose-tests-with-plugins-using-the-python-setuptools-test-command/
from setuptools.command.test import test as test_command


class NoseTestCommand(test_command):
    def finalize_options(self):
        test_command.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # Run nose ensuring that argv simulates running nosetests directly.
        import nose
        nose.run_exit(argv=['nosetests'])

version = __version__
readme = open('README.rst').read()

setup(name="JPKforceparse",
      version=version,
      long_description=readme,
      packages=["JPKforceparse"],
      cmdclass={"test": NoseTestCommand},
      install_requires=['matplotlib',
                        'numpy'],
      tests_require=["nose", "coverage"],
)
