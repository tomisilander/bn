from setuptools import setup
from glob import glob
setup(name          = "bn",
      version       = "0.1",
      description   = "Bayesian network software",
      author        = "Tomi Silander",
      author_email  = "tomi.silander@iki.fi",
      packages      = ["bn", "bn.learn", "bn.model", "bn_console_scripts"],
      package_data  = {"":["*.txt"],
                       "bn.learn":["cscore.so", "cdata.so"]},
      long_description = """
    Could be longer.
      """,
      
      scripts = glob("scripts/*"),

      entry_points = {
          'console_scripts': [
              'bn_nofnets=bn_console_scripts.bn_nofnets:main',
              ]
          }
)
