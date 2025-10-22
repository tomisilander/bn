from setuptools import setup
from glob import glob
setup(name          = "bn",
      version       = "0.1",
      description   = "Bayesian network software",
      author        = "Tomi Silander",
      author_email  = "tomi.silander@iki.fi",
      packages      = ["src", "src.learn", "src.model", "src.data"],
      package_data  = {"":["*.txt"],
                       "src.learn":["cscore.so", "cdata.so"]},
      long_description = """
    Could be longer.
      """,
      
      scripts = glob("scripts/bens"),

)
