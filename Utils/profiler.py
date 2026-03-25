import cProfile
import path
from Algorithms.DefaultPlacement import defaultPlacement
from Algorithms.LinearSwitch2People import LinearSwitch2People
from Algorithms.LinearSwitch3People import LinearSwitch3People
from Algorithms.LinearSwitch4People import LinearSwitch4People
from Utils.printer import printArrangementWithValues
from Utils.test import input100People, testLinearSwitch2People, testLinearSwitch3People, testLinearSwitch4People, testLinearSwitch4PeopleSets
pr = cProfile.Profile()

def profile(func):
    def wrapper(*args, **kwargs):
        pr.enable()
        result = func(*args, **kwargs)
        pr.disable()
        pr.print_stats(sort='time')
        return result
    return wrapper



profile(testLinearSwitch4PeopleSets)((defaultPlacement(input100People)))


