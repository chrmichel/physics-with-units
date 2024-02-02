from constants import Constant
from classes import Quantity, Unit, Vector


Unit.update_dimensions("em")

e = Vector(6.8, 0, 0, "electric field")
h = Vector(0, 9.3, 0, "magnetic field")
s = e.cross(h)
print(s)
