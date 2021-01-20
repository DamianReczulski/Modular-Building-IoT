import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl



class FUZZY:
    def __init__(self, pozf=100, openf=255 ):
        self.poz = ctrl.Antecedent(np.arange(0, pozf+1, 1), 'poz')
        self.open = ctrl.Consequent(np.arange(0, openf+1, 1), 'open')

        self.poz['rlow'] = fuzz.trimf(self.poz.universe, [-50, -50, 5])
        self.poz['low'] = fuzz.trimf(self.poz.universe, [4, 5, 16])
        self.poz['ok'] = fuzz.trimf(self.poz.universe, [15, 22, 22])
        self.poz['high'] = fuzz.trimf(self.poz.universe, [21, 31, 31])
        self.poz['rhigh'] = fuzz.trimf(self.poz.universe, [30, 50, 50])

        self.open['none'] = fuzz.trimf(self.open.universe, [0, 1, 87])
        self.open['low'] = fuzz.trimf(self.open.universe, [86, 89, 110])
        self.open['medium'] = fuzz.trimf(self.open.universe, [109, 109, 125])
        self.open['high'] = fuzz.trimf(self.open.universe, [124, 147, 150])
        self.open['full'] = fuzz.trimf(self.open.universe, [149, 250, 255])

        self.output = 0.0

    def update(self,pozf):
        rule0 = ctrl.Rule(self.poz['rhigh'], self.open['none'])
        rule1 = ctrl.Rule(self.poz['high'], self.open['low'])
        rule2 = ctrl.Rule(self.poz['ok'], self.open['medium'])
        rule3 = ctrl.Rule(self.poz['low'], self.open['high'])
        rule4 = ctrl.Rule(self.poz['rlow'], self.open['full'])

        open_ctrl = ctrl.ControlSystem([rule0, rule1, rule2, rule3, rule4])

        s_open = ctrl.ControlSystemSimulation(open_ctrl)

        s_open.input['poz'] = pozf

        # Crunch the numbers
        s_open.compute()

        self.output = s_open.output['open']

    def set(self, x, li):
        self.poz['rlow']  = fuzz.trimf(self.poz.universe, li[x][0])
        self.poz['low'] = fuzz.trimf(self.poz.universe, li[x][1])
        self.poz['ok'] = fuzz.trimf(self.poz.universe, li[x][2])
        self.poz['high'] = fuzz.trimf(self.poz.universe, li[x][3])
        self.poz['rhigh'] = fuzz.trimf(self.poz.universe, li[x][4])

        self.open['none'] = fuzz.trimf(self.open.universe, li[x][5])
        self.open['low'] = fuzz.trimf(self.open.universe, li[x][6])
        self.open['medium'] = fuzz.trimf(self.open.universe, li[x][7])
        self.open['high'] = fuzz.trimf(self.open.universe, li[x][8])
        self.open['full'] = fuzz.trimf(self.open.universe, li[x][9])

        self.output = 0.0