Calico is a utility for checking command-line programs in terms of their
input and output. It checks whether a program generates the correct output
when given some inputs. It was developed to evaluate simple programming
assignments in an introductory programming course.

:PyPI: https://pypi.python.org/pypi/calico/
:Repository: https://bitbucket.org/uyar/calico
:Documentation: https://calico.readthedocs.io/

Calico has been tested with Python 3.4. You can install the latest version
from PyPI::

   pip install calico

Calico uses `pexpect`_ for interacting with the program it is checking.
The file that specifies the inputs and outputs for the checks
is in `YAML`_ format.

.. _pexpect: https://pexpect.readthedocs.io/
.. _YAML: http://www.yaml.org/
