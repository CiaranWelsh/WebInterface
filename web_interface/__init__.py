import os, glob
from pycotools3 import model, tasks, viz

WORKING_DIRECTORY = os.path.dirname(os.path.dirname(__file__))
WEB_INTERFACE_PACKAGE_DIR = os.path.join(WORKING_DIRECTORY, 'web_interface')
WEB_INTERFACE_DASH_DIR = os.path.join(WEB_INTERFACE_PACKAGE_DIR, 'dash_model')

COPASI_MODEL = os.path.join(WEB_INTERFACE_PACKAGE_DIR, 'model.cps')
SBML_FILE = os.path.splitext(COPASI_MODEL)[0] + '.sbml'

if not os.path.isfile(SBML_FILE):
    mod = model.Model(COPASI_MODEL)
    mod.to_sbml(SBML_FILE)

    












