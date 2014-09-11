
# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2008-2014 AvanzOSC (Daniel). All Rights Reserved
#    Date: 10/07/2014
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

from openerp import models, fields, api


class MrpRoutingWorkcenter(models.Model):
    _inherit = 'mrp.routing.workcenter'

    operation = fields.Many2one('mrp.routing.operation', string='Operation')
    op_wc_lines = fields.One2many('mrp.operation.workcenter',
                                  'routing_workcenter',
                                  'Workcenter Info Lines')

    @api.one
    @api.onchange('operation')
    def onchange_operation(self):
        if self.operation:
            self.name = self.operation.name
            self.note = self.operation.description
            op_wc_lst = []
            data = {}
            for operation_wc in self.operation.workcenters:
                data = {'workcenter': operation_wc.id,
                        'capacity_per_cycle': operation_wc.capacity_per_cycle,
                        'time_efficiency': operation_wc.time_efficiency,
                        'time_cycle': operation_wc.time_cycle,
                        'time_start': operation_wc.time_start,
                        'time_stop': operation_wc.time_stop,
                        'default': False
                        }
                op_wc_lst.append(data)
            self.op_wc_lines = op_wc_lst

    @api.one
    @api.onchange('op_wc_lines')
    def onchange_default(self):
        for opwc_line in self.op_wc_lines:
            if opwc_line.default:
                self.workcenter_id = opwc_line.workcenter.id
                break
