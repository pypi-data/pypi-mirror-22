# This file is part of OMG-tools.
#
# OMG-tools -- Optimal Motion Generation-tools
# Copyright (C) 2016 Ruben Van Parys & Tim Mercy, KU Leuven.
# All rights reserved.
#
# OMG-tools is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

from ..basics.optilayer import OptiChild
from ..basics.spline import BSplineBasis
from ..execution.plotlayer import PlotLayer, mix_with_white
from obstacle import Obstacle
from casadi import inf
import numpy as np


class Environment(OptiChild, PlotLayer):

    def __init__(self, room, obstacles=None):
        obstacles = obstacles or []
        OptiChild.__init__(self, 'environment')
        PlotLayer.__init__(self)

        # create room and define dimension of the space
        self.room, self.n_dim = room, room['shape'].n_dim
        if 'position' not in room:
            self.room['position'] = [0. for k in range(self.n_dim)]
        if not ('orientation' in room):
            if self.n_dim == 2:
                self.room['orientation'] = 0.
            elif self.n_dim == 3:
                self.room['orientation'] = [0., 0., 0.]  # Euler angles
            else:
                raise ValueError('You defined a shape with dimension '
                                 + str(self.n_dim) + ', which is invalid.')
        if 'draw' not in room:
            self.room['draw'] = False

        # add obstacles
        self.obstacles, self.n_obs = [], 0
        for obstacle in obstacles:
            self.add_obstacle(obstacle)

    # ========================================================================
    # Copy function
    # ========================================================================

    def copy(self):
        obstacles = [Obstacle(o.initial, o.shape, o.simulation, o.options)
                     for o in self.obstacles]
        return Environment(self.room, obstacles)

    # ========================================================================
    # Add obstacles/vehicles
    # ========================================================================

    def add_obstacle(self, obstacle):
        if isinstance(obstacle, list):
            for obst in obstacle:
                self.add_obstacle(obst)
        else:
            if obstacle.n_dim != self.n_dim:
                raise ValueError('Not possible to combine ' +
                                 str(obstacle.n_dim) + 'D obstacle with ' +
                                 str(self.n_dim) + 'D environment.')
            self.obstacles.append(obstacle)
            self.n_obs += 1

    def define_collision_constraints(self, vehicle, splines):
        if vehicle.n_dim != self.n_dim:
            raise ValueError('Not possible to combine ' +
                             str(vehicle.n_dim) + 'D vehicle with ' +
                             str(self.n_dim) + 'D environment.')
        degree = 1
        knots = np.r_[np.zeros(degree),
                      vehicle.knots[
                          vehicle.degree:-vehicle.degree],
                      np.ones(degree)]
        basis = BSplineBasis(knots, degree)
        hyp_veh, hyp_obs = {}, {}
        for k, shape in enumerate(vehicle.shapes):
            hyp_veh[shape] = []
            for l, obstacle in enumerate(self.obstacles):
                if obstacle.options['avoid']:
                    if obstacle not in hyp_obs:
                        hyp_obs[obstacle] = []
                    a = self.define_spline_variable(
                        'a'+'_'+vehicle.label+'_'+str(k)+str(l), self.n_dim, basis=basis)
                    b = self.define_spline_variable(
                        'b'+'_'+vehicle.label+'_'+str(k)+str(l), 1, basis=basis)[0]
                    self.define_constraint(
                        sum([a[p]*a[p] for p in range(self.n_dim)])-1, -inf, 0.)
                    hyp_veh[shape].append({'a': a, 'b': b})
                    hyp_obs[obstacle].append({'a': a, 'b': b})
        for obstacle in self.obstacles:
            if obstacle.options['avoid']:
                obstacle.define_collision_constraints(hyp_obs[obstacle])
        for spline in vehicle.splines:
            vehicle.define_collision_constraints(hyp_veh, self, spline)

    def define_intervehicle_collision_constraints(self, vehicles):
        hyp_veh = {veh: {sh: [] for sh in veh.shapes} for veh in vehicles}
        for k in range(len(vehicles)):
            for l in range(k+1, len(vehicles)):
                veh1 = vehicles[k]
                veh2 = vehicles[l]
                if veh1 != veh2:
                    if veh1.n_dim != veh2.n_dim:
                        raise ValueError('Not possible to combine ' +
                                         str(veh1.n_dim) + 'D and ' + str(veh2.n_dim) + 'D vehicle.')
                    degree = 1
                    knots = np.r_[np.zeros(degree), np.union1d(veh1.knots[veh1.degree:-veh1.degree], veh2.knots[veh2.degree:-veh2.degree]), np.ones(degree)]
                    basis = BSplineBasis(knots, degree)
                    for kk, shape1 in enumerate(veh1.shapes):
                        for ll, shape2 in enumerate(veh2.shapes):
                            a = self.define_spline_variable(
                                'a'+'_'+veh1.label+'_'+str(kk)+'_'+veh2.label+'_'+str(ll), self.n_dim, basis=basis)
                            b = self.define_spline_variable(
                                'b'+'_'+veh1.label+'_'+str(kk)+'_'+veh2.label+'_'+str(ll), 1, basis=basis)[0]
                            self.define_constraint(
                                sum([a[p]*a[p] for p in range(self.n_dim)])-1, -inf, 0.)
                            hyp_veh[veh1][shape1].append({'a': a, 'b': b})
                            hyp_veh[veh2][shape2].append({'a': [-a_i for a_i in a], 'b': -b})
        for vehicle in vehicles:
            for spline in vehicle.splines:
                vehicle.define_collision_constraints(hyp_veh[vehicle], self, spline)

    # ========================================================================
    # Optimization modelling related functions
    # ========================================================================

    def init(self):
        for obstacle in self.obstacles:
            obstacle.init()

    # ========================================================================
    # Simulate environment
    # ========================================================================

    def simulate(self, simulation_time, sample_time):
        for obstacle in self.obstacles:
            obstacle.simulate(simulation_time, sample_time)
        self.update_plots()

    def draw(self, t=-1):
        surfaces, lines = [], []
        if self.room['draw']:
            s, l = self.room['shape'].draw()
            surfaces += s
            lines += l
        for obstacle in self.obstacles:
            s, l = obstacle.draw(t)
            surfaces += s
            lines += l
        return surfaces, lines

    def get_canvas_limits(self):
        limits = self.room['shape'].get_canvas_limits()
        return [limits[k]+self.room['position'][k] for k in range(self.n_dim)]

    # ========================================================================
    # Plot related functions
    # ========================================================================

    def init_plot(self, argument, **kwargs):
        s, l = self.draw()
        gray = [60./255., 61./255., 64./255.]
        surfaces = [{'facecolor': mix_with_white(gray, 50), 'edgecolor': 'black', 'linewidth': 1.2} for _ in s]
        lines = [{'color': 'black', 'linewidth': 1.2} for _ in l]
        if self.room['draw']:
            s_, l_ = self.room['shape'].draw()
            for k, _ in enumerate(s_):
                surfaces[k]['facecolor'] = mix_with_white(gray, 90)
        if 'limits' in kwargs:
            limits = kwargs['limits']
        else:
            limits = self.get_canvas_limits()
        labels = ['' for k in range(self.n_dim)]
        if self.n_dim == 2:
            return [[{'labels': labels,'surfaces': surfaces, 'lines': lines, 'aspect_equal': True,
                      'xlim': limits[0], 'ylim': limits[1]}]]
        else:
            return [[{'labels': labels, 'surfaces': surfaces, 'lines': lines, 'aspect_equal': True,
                      'xlim': limits[0], 'ylim': limits[1], 'zlim': limits[2],
                      'projection': '3d'}]]

    def update_plot(self, argument, t, **kwargs):
        s, l = self.draw(t)
        return [[{'surfaces': s, 'lines': l}]]
