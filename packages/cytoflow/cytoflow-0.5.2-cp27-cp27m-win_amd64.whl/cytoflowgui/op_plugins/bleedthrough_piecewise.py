#!/usr/bin/env python2.7
# coding: latin-1

# (c) Massachusetts Institute of Technology 2015-2016
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''
Created on Oct 9, 2015

@author: brian
'''

import warnings

from traitsui.api import View, Item, EnumEditor, Controller, VGroup, \
                         ButtonEditor, Heading, HGroup, InstanceEditor
from envisage.api import Plugin, contributes_to
from traits.api import (provides, Callable, List, Str, HasTraits, File, Event, 
                        Dict, on_trait_change, Property)
from pyface.api import ImageResource

import cytoflow.utility as util

from cytoflow.operations.bleedthrough_piecewise import BleedthroughPiecewiseOp, BleedthroughPiecewiseDiagnostic
from cytoflow.views.i_selectionview import IView

from cytoflowgui.view_plugins.i_view_plugin import ViewHandlerMixin, PluginViewMixin
from cytoflowgui.op_plugins import IOperationPlugin, OpHandlerMixin, OP_PLUGIN_EXT, shared_op_traits
from cytoflowgui.subset import ISubset, SubsetListEditor
from cytoflowgui.color_text_editor import ColorTextEditor
from cytoflowgui.op_plugins.i_op_plugin import PluginOpMixin
from cytoflowgui.vertical_list_editor import VerticalListEditor
from cytoflowgui.workflow import Changed

class _Control(HasTraits):
    channel = Str
    file = File

class BleedthroughPiecewiseHandler(OpHandlerMixin, Controller):
    add_control = Event
    remove_control = Event

    # MAGIC: called when add_control is fired
    def _add_control_fired(self):
        self.model.controls_list.append(_Control())
        
    def _remove_control_fired(self):
        if self.model.controls_list:
            self.model.controls_list.pop()
             
    def control_traits_view(self):
        return View(HGroup(Item('channel',
                                editor = EnumEditor(name = 'handler.context.previous.channels')),
                           Item('file',
                                show_label = False)),
                    handler = self)
    
    def default_traits_view(self):
        return View(VGroup(Item('controls_list',
                                editor = VerticalListEditor(editor = InstanceEditor(view = self.control_traits_view()),
                                                            style = 'custom',
                                                            mutable = False),
                                style = 'custom'),
                    Item('handler.add_control',
                         editor = ButtonEditor(value = True,
                                               label = "Add a control")),
                    Item('handler.remove_control',
                         editor = ButtonEditor(value = True,
                                               label = "Remove a control")),
                    label = "Controls",
                    show_labels = False),
                    VGroup(Item('subset_list',
                                show_label = False,
                                editor = SubsetListEditor(conditions = "handler.context.previous.conditions",
                                                          metadata = "handler.context.previous.metadata",
                                                          when = "'experiment' not in vars() or not experiment")),
                           label = "Subset",
                           show_border = False,
                           show_labels = False),
                    Heading("WARNING: Very slow!"),
                    Heading("Give it a few minutes..."),
                    Item('do_estimate',
                         editor = ButtonEditor(value = True,
                                               label = "Estimate!"),
                         show_label = False),
                    shared_op_traits)

class BleedthroughPiecewisePluginOp(PluginOpMixin, BleedthroughPiecewiseOp):
    handler_factory = Callable(BleedthroughPiecewiseHandler)

    add_control = Event
    remove_control = Event

    controls = Dict(Str, File, transient = True)
    controls_list = List(_Control, estimate = True)

    # MAGIC: called when add_control is set
    def _add_control_fired(self):
        self.controls_list.append(_Control())
        
    # MAGIC: called when remove_control is set
    def _remove_control_fired(self):
        self.controls_list.pop()
        
    @on_trait_change('controls_list_items,controls_list.+', post_init = True)
    def _controls_changed(self, obj, name, old, new):
        self.changed = (Changed.ESTIMATE, ('controls_list', self.controls_list))
    
    # bits to support the subset editor
    
    subset_list = List(ISubset, estimate = True)    
    subset = Property(Str, depends_on = "subset_list.str")
        
    # MAGIC - returns the value of the "subset" Property, above
    def _get_subset(self):
        return " and ".join([subset.str for subset in self.subset_list if subset.str])
    
    @on_trait_change('subset_list.str', post_init = True)
    def _subset_changed(self, obj, name, old, new):
        self.changed = (Changed.ESTIMATE, ('subset_list', self.subset_list))
  
    
    def default_view(self, **kwargs):
        return BleedthroughPiecewisePluginView(op = self, **kwargs)
    
    def estimate(self, experiment):
        for i, control_i in enumerate(self.controls_list):
            for j, control_j in enumerate(self.controls_list):
                if control_i.channel == control_j.channel and i != j:
                    raise util.CytoflowOpError("Channel {0} is included more than once"
                                               .format(control_i.channel))
                                               
        self.controls = {}
        for control in self.controls_list:
            self.controls[control.channel] = control.file
            
        if not self.subset:
            warnings.warn("Are you sure you don't want to specify a subset "
                          "used to estimate the model?",
                          util.CytoflowOpWarning)
                    
        BleedthroughPiecewiseOp.estimate(self, experiment, subset = self.subset)
        
        self.changed = (Changed.ESTIMATE_RESULT, self)
        
    def clear_estimate(self):
        self._splines.clear()
        self._interpolators.clear()
        self._channels.clear()
        
        self.changed = (Changed.ESTIMATE_RESULT, self)
        
    def should_clear_estimate(self, changed):
        if changed == Changed.ESTIMATE:
            return True
        
        return False

class BleedthroughPiecewiseViewHandler(ViewHandlerMixin, Controller):
    def default_traits_view(self):
        return View(Item('context.view_warning',
                         resizable = True,
                         visible_when = 'context.view_warning',
                         editor = ColorTextEditor(foreground_color = "#000000",
                                                 background_color = "#ffff99")),
                    Item('context.view_error',
                         resizable = True,
                         visible_when = 'context.view_error',
                         editor = ColorTextEditor(foreground_color = "#000000",
                                                  background_color = "#ff9191")))

@provides(IView)
class BleedthroughPiecewisePluginView(PluginViewMixin, BleedthroughPiecewiseDiagnostic):
    handler_factory = Callable(BleedthroughPiecewiseViewHandler)
    
    def plot_wi(self, wi):
        self.plot(wi.previous.result)
    
    def should_plot(self, changed):
        if changed == Changed.ESTIMATE_RESULT:
            return True
        
        return False

@provides(IOperationPlugin)
class BleedthroughPiecewisePlugin(Plugin):
    """
    class docs
    """
    
    id = 'edu.mit.synbio.cytoflowgui.op_plugins.bleedthrough_piecewise'
    operation_id = 'edu.mit.synbio.cytoflow.operations.bleedthrough_piecewise'

    short_name = "Piecewise Compensation"
    menu_group = "Gates"
    
    def get_operation(self):
        return BleedthroughPiecewisePluginOp()
    
    def get_icon(self):
        return ImageResource('bleedthrough_piecewise')
    
    @contributes_to(OP_PLUGIN_EXT)
    def get_plugin(self):
        return self
    