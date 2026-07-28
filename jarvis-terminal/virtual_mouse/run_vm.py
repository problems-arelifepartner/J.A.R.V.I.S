"""
Wrapper for virtual_mouse main to capture and log errors for easier debugging on diverse platforms.
"""
import traceback
import os
from virtual_mouse import main as vm_main

LOG = os.path.join(os.path.dirname(__file__), "../virtual_mouse_error.log")
try:
    vm_main()
except Exception:
    tb = traceback.format_exc()
    try:
        with open(LOG, "w") as f:
            f.write(tb)
    except Exception:
        pass
    print("Virtual Mouse encountered an error. Traceback written to:", LOG)
    print(tb)
    raise
