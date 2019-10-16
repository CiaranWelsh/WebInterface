import os, glob
import tellurium as te

from web_interface import SBML_FILE


model_string = ''

if model_string == '':
    with open(SBML_FILE, 'r') as f:
        sbml = f.read()

    model_string = te.sbmlToAntimony(sbml)


if __name__ == '__main__':
    print(model_string)






















