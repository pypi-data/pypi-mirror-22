#-*- coding: utf-8 -*-
"""
@brief      test log(time=280s)
"""

import sys
import os
import unittest
import warnings

try:
    import src
except ImportError:
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..")))
    if path not in sys.path:
        sys.path.append(path)
    import src

try:
    import pyquickhelper as skip_
except ImportError:
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..",
                "..",
                "pyquickhelper",
                "src")))
    if path not in sys.path:
        sys.path.append(path)
    import pyquickhelper as skip_


from pyquickhelper.loghelper import fLOG
from pyquickhelper.pycode import get_temp_folder, add_missing_development_version
from pyquickhelper.pycode import fix_tkinter_issues_virtualenv


class TestLONGNotebookPopulation2(unittest.TestCase):

    def setUp(self):
        add_missing_development_version(
            ["pyensae", "pymyinstall", "pyrsslocal"], __file__)

    def test_notebook_population(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        fix_tkinter_issues_virtualenv()

        if "travis" in sys.executable:
            # matplotlib is still failing
            warnings.warn(
                "travis, unable to test TestNotebookPopulation.test_notebook_population")
            return

        from src.actuariat_python.automation.notebook_test_helper import ls_notebooks, execute_notebooks, clean_function_notebook, unittest_raise_exception_notebook
        temp = get_temp_folder(__file__, "temp_population")
        keepnote = [_ for _ in ls_notebooks(
            "population") if "seance6_graphes_ml_enonce" in _]
        assert len(keepnote) > 0
        for k in keepnote:
            fLOG(k)
        res = execute_notebooks(temp, keepnote,
                                lambda i, n: "deviner" not in n,
                                fLOG=fLOG,
                                clean_function=clean_function_notebook)
        unittest_raise_exception_notebook(res, fLOG)


if __name__ == "__main__":
    unittest.main()
