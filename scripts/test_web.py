"""Run API tests with isolated web dependencies; fixtures do not load real weights."""
import unittest
from web_runtime import configure


if __name__ == '__main__':
    configure()
    unittest.main(module='tests.test_api', verbosity=2)
