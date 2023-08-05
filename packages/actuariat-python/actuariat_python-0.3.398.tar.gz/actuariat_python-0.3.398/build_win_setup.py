"""
@file
@brief Builds a setup for the teachings: actuariat_python
"""
try:
    import pymyinstall
except ImportError:
    import sys
    sys.path.append("../pymyinstall/src")
    import pymyinstall

try:
    import pyquickhelper
except ImportError:
    import sys
    sys.path.append("../pyquickhelper/src")
    import pyquickhelper


if __name__ == "__main__":
    import sys
    sys.path.append("src")
    from pyquickhelper import fLOG
    fLOG(OutputPrint=True)

    from actuariat_python.automation.win_setup_helper import last_function
    from pymyinstall import win_python_setup
    from pymyinstall.packaged import ensae_fullset

    list_modules = ensae_fullset()

    win_python_setup(module_list=list_modules, verbose=True,
                     download_only=False,
                     no_setup=False,
                     last_function=last_function,
                     selection={"R"},
                     documentation=False,
                     fLOG=fLOG)
