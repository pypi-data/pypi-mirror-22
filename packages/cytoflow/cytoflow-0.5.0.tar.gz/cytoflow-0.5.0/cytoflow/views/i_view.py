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
Created on Feb 23, 2015

@author: brian
'''

from traits.api import Interface, Str

class IView(Interface):
    """An interface for a visualization of flow data.
    
    Could be a histogram, a density plot, a scatter plot, a statistical
    visualization like a bar chart of population means; even a textual 
    representation like a table.
    
    Attributes
    ----------
    id : Str
        A unique id for this view.  Prefix: "edu.mit.cytoflow.views"

    friendly_id : Str
        The human-readable id of this view: eg, "Histogram"
        
    name : Str
        The name of this view (for serialization, UI, etc.)
        
    subset : Str
        A string specifying the subset of the data to be plotted.
        Passed to pandas.DataFrame.query().
    """

    id = Str      
    friendly_id = Str
     
    name = Str
    subset = Str
    
    def plot(self, experiment, **kwargs):
        """Plot a visualization of flow data using the pyplot stateful interface
        
        Parameters
        ----------
        experiment : Experiment 
            the Experiment containing the data to plot
        kwargs : dict
            additional arguments to pass to the underlying plotting function.
        """
    