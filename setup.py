from distutils.core import setup, Extension
modeling = Extension("modeling", sources = ['modeling.cpp'])
setup(name = "modeling",
      version = "1.0",
      description = "SIR Modeling Module",
      ext_modules = [modeling],
      )