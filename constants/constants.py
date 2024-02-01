from scipy import constants as sc

from classes import Unit, Quantity, Vector


class Constant:
    g = Quantity(sc.g, Unit([0, 1, -2]), "gravitational constant")
    g_vector = Vector(0, 0, -sc.g, Unit([0, 1, -2]), "gravitational vector")
    pi = sc.pi
    c = Quantity(sc.c, Unit([0, 1, -1]), "speed of light")
    e_0 = Quantity(sc.epsilon_0, Unit([-1, -3, 4, 0, 2]), "dielectric constant")
    coulomb = 1 / (4 * pi * e_0)
    mu_0 = Quantity(sc.mu_0, Unit([1, 1, -2, 0, -2]), "magnetic constant")
    planck = Quantity(sc.Planck, Unit([1, 2, -1]), "Planck constant")
    hbar = planck / (2 * pi)
    el_charge = Quantity(
        sc.elementary_charge, Unit([0, 0, 1, 0, 1]), "elementary charge"
    )
    gas_constant = Quantity(sc.R, Unit([1, 2, -2, -1, 0, -1]), "gas constant")
    boltzmann = Quantity(sc.Boltzmann, Unit([1, 2, -2, -1]), "Boltzmann constant")
    avogadro = Quantity(sc.N_A, Unit([0, 0, 0, 0, 0, -1]), "Avogadro constant")
