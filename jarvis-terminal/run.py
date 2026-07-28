#!/usr/bin/env python3
"""
Wrapper runner that executes jarvis main and catches uncaught exceptions to a log file so users can paste
the traceback here for quick fixes.
"""
import traceback
import sys
from jarvis import main as jarvis_main

LOG = "jarvis-terminal/jarvis_error.log"
try:
    jarvis_main()
except Exception:
    tb = traceback.format_exc()
    print("An unexpected error occurred. The traceback has been written to", LOG)
    with open(LOG, "w") as f:
        f.write(tb)
    print(tb)
    sys.exit(1)
