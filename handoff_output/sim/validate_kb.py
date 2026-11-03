"""Run the upgraded communication-path KB validation, not the legacy gap check."""
from pathlib import Path
import os,sys
if __name__=='__main__':
    target=Path(__file__).resolve().parent/'run_validation.py'
    os.execv(sys.executable,[sys.executable,str(target),'--part','kb',*sys.argv[1:]])
