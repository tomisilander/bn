from setuptools import setup, find_packages

setup(name          = "bn",
      version       = "0.1",
      description   = "Bayesian network software",
      author        = "Tomi Silander",
      author_email  = "tomi.silander@iki.fi",
      packages      = find_packages()
      package_data  = {"":"[*.txt"],
                       "bn.learn":["cscore.so", "cdata.so"]},
      long_description = """
    Could be longer.
      """

      )
