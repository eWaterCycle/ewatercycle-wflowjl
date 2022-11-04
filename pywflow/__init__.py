"""Documentation about pywflow"""
import logging
from .wflow import WflowBMI


logging.getLogger(__name__).addHandler(logging.NullHandler())

__author__ = "Bart Schilperoort"
__email__ = "b.schilperoort@esciencecenter.nl"
__version__ = "0.1.0"
