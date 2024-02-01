from constants import Constant
from classes import Quantity, Unit, Vector


Unit.update_dimensions("mechanics")
t3 = Quantity(3, Unit.from_dict("time"))
v0 = Vector(1, 5, 4, Unit.from_dict("speed"))
r0 = Vector(0, 2, -1, Unit.from_dict("length"))
g = Constant.g_vector
speed_10 = g * t3  # * g#  + v0
# pos_v = (v0 * t3)
# pos_acc_rev = (t3**2 * Constant.g_vector)
# pos_10 = r0 + pos_v + pos_acc_rev
print(speed_10)
# print(pos_10)
