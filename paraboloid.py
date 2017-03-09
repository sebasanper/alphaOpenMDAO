from __future__ import print_function

from openmdao.components.paramcomp import ParamComp
from openmdao.core.component import Component
from openmdao.core.problem import Problem, Group
from openmdao.drivers.scipy_optimizer import ScipyOptimizer
from openmdao.components.constraint import ConstraintComp
from openmdao.recorders.shelverecorder import ShelveRecorder

class Paraboloid(Component):
    """ Evaluates the equation f(x,y) = (x-3)^2 + xy + (y+4)^2 - 3 """

    def __init__(self):
        super(Paraboloid, self).__init__()

        self.add_param('x', val=0.0)
        self.add_param('y', val=0.0)

        self.add_output('f_xy', shape=1)

    def solve_nonlinear(self, params, unknowns, resids):
        """f(x,y) = (x-3)^2 + xy + (y+4)^2 - 3
        Optimal solution (minimum): x = 6.6667; y = -7.3333
        """

        x = params['x']
        y = params['y']

        unknowns['f_xy'] = (x - 3.0) ** 2 + x * y + (y + 4.0) ** 2 - 3.0

    def jacobian(self, params, unknowns, resids):
        """ Jacobian for our paraboloid."""

        x = params['x']
        y = params['y']
        J = {}

        J['f_xy', 'x'] = 2.0 * x - 6.0 + y
        J['f_xy', 'y'] = 2.0 * y + 8.0 + x
        return J

if __name__ == "__main__":

    top = Problem()

    root = top.root = Group()

    root.add('p1', ParamComp('x', 3.0), promotes=['*'])
    root.add('p2', ParamComp('y', - 4.0), promotes=['*'])
    root.add('p', Paraboloid(), promotes=['*'])

    # Constraint Equation
    # root.add('con', ConstraintComp('x - y > 15.0', out='c'))

    # root.connect('p1.x', 'p.x')
    # root.connect('p2.y', 'p.y')
    # root.connect('p.x', 'con.x')
    # root.connect('p.y', 'con.y')

    top.driver = ScipyOptimizer()
    top.driver.options['optimizer'] = 'SLSQP'

    # top.driver.add_param('p1.x', low=-50.0, high=50.0)
    # top.driver.add_param('p2.y', low=-50.0, high=50.0)
    # top.driver.add_objective('p.f_xy')
    top.driver.add_param('x', low=-50.0, high=50.0)
    top.driver.add_param('y', low=-50.0, high=50.0)
    top.driver.add_objective('f_xy')
    # top.driver.add_constraint('con.c')

    # recorder = ShelveRecorder('saved_data')
    # top.driver.add_recorder(recorder)

    top.setup()
    top.run()

    # import shelve
    # f = shelve.open('saved_data')
    # print(f)
    # # data = f['SLSQP/6']
    # # print(data)
    # # p = data['Parameters']
    # # print(p)
    # # u = data['Unknowns']
    # # print(u)
    print(root.p.unknowns['f_xy'])
    print('\n')
    print('Minimum of %f found at (%f, %f)' % (top['f_xy'], top['x'], top['y']))