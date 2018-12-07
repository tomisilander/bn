from setuptools import setup, find_packages

setup(name          = "bn",
      version       = "0.1",
      description   = "Bayesian network software",
      author        = "Tomi Silander",
      author_email  = "tomi.silander@iki.fi",
      packages      = find_packages(),
      package_data  = {"":["*.txt"],
                       "bn.learn":["cscore.so", "cdata.so"]},
      long_description = """
    Could be longer.
      """,
      
      install_requires=['coliche>=0.0', 'disdat>=0.0', 'sigpool>=0.0'],
      dependency_links=[
          'http://github.com/tomisilander/coliche#egg=coliche-0.1',       
          'http://github.com/tomisilander/sigpool#egg=sigpool-0.9',      
          'http://github.com/tomisilander/disdat#egg=disdat-0.9'],
      )
