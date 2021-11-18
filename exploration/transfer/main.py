import sys
import os.path
# Translator classes (Add as needed)
from translateTRNBld import translateTRNBld as TRNSYS

# Translator definition (Add cases as needed)
def translate_h2k(sHotInput,sOutput):
    # Get output extension
    sExt = os.path.splitext(sOutput)[1][1:]
    if sExt == 'xml':
        print(f"Creating HPXML of {sHotInput}\n")
    elif sExt == 'b18':
        newFile = TRNSYS(sHotInput)
        newFile.translateFile(sOutput)
    else:
        raise Exception(f"Unknown output extension {sExt}.\n")

#########################################################################
#                             Main Program
#########################################################################
# Process command line arguments
if len(sys.argv) != 3:
    raise Exception('Incorrect number of input provided.\nTwo inputs required: <source_h2k> <output>\n')
sHotInput = sys.argv[1]
sOutput = sys.argv[2]

# Translate
translate_h2k(sHotInput,sOutput)
