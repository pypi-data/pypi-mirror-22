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
Created on Sep 2, 2015

@author: brian
'''

from __future__ import division, absolute_import

import math

from traits.api import (HasStrictTraits, Str, File, Dict, Any, Callable,
                        Instance, Tuple, Bool, Constant, provides)
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sklearn.mixture
import sklearn.linear_model
import scipy.optimize
import scipy.interpolate

import cytoflow.views
import cytoflow.utility as util

from .i_operation import IOperation
from .import_op import Tube, ImportOp, check_tube

@provides(IOperation)
class ColorTranslationOp(HasStrictTraits):
    """
    Translate measurements from one color's scale to another, using a two-color
    or three-color control.
    
    To use, set up the `channels` dict with the desired mapping and the 
    `controls` dict with the multi-color controls.  Call `estimate()` to
    paramterize the module; check that the plots look good with 
    `default_view().plot()`; then `apply()` to an Experiment.
    
    Attributes
    ----------
    name : Str
        The operation name (for UI representation; optional for interactive use)
        
    controls : Dict((Str, Str), File)
        Two-color controls used to determine the mapping.  They keys are 
        tuples of *from-channel* and *to-channel*.  The values are FCS files 
        containing two-color constitutive fluorescent expression data 
        for the mapping.
        
    mixture_model : Bool (default = False)
        If "True", try to model the "from" channel as a mixture of expressing
        cells and non-expressing cells (as you would get with a transient
        transfection.)  Make sure you check the diagnostic plots!
        
    Metadata
    --------
    channel_translation : Str
        Which channel was this one translated to?
        
    channel_translation_fn : Callable (pandas.Series --> pandas.Series)
        The function that translated this channel
        
    Notes
    -----
    In the TASBE workflow, this operation happens *after* the application of
    `AutofluorescenceOp` and `BleedthroughPiecewiseOp`.  Both must be applied
    to the single-color controls before the translation coefficients are
    estimated; the autofluorescence and bleedthrough parameters for each channel 
    are retrieved from the channel metadata and applied in `estimate()`.
    

    Examples
    --------
    >>> ct_op = flow.ColorTranslationOp()
    >>> ct_op.controls = {("Pacific Blue-A", "FITC-A") : "merged/rby.fcs",
    ...                   ("PE-Tx-Red-YG-A", "FITC-A") : "merged/rby.fcs"}
    >>> ct_op.mixture_model = True
    >>>
    >>> ct_op.estimate(ex4)
    >>> ct_op.default_view().plot(ex4)
    >>> ex5 = ct_op.apply(ex4)
    """
    
    # traits
    id = Constant('edu.mit.synbio.cytoflow.operations.color_translation')
    friendly_id = Constant("Color translation")
    
    name = Constant("Color Translation")

    translation = util.Removed(err_string = "'translation' is removed; the same info is found in 'controls'", warning = True)
    controls = Dict(Tuple(Str, Str), File)
    mixture_model = Bool(False)
    linear_model = Bool(False)

    # The regression coefficients determined by `estimate()`, used to map 
    # colors between channels.  The keys are tuples of (*from-channel*,
    # *to-channel) (corresponding to key-value pairs in `translation`).  The
    # values are lists of Float, the log-log coefficients for the color 
    # translation (determined by `estimate()`). 
    # TODO - why can't i make the value List(Float)?
    _coefficients = Dict(Tuple(Str, Str), Any, transient = True)
    _trans_fn = Dict(Tuple(Str, Str), Callable, transient = True)

    def estimate(self, experiment, subset = None): 
        """
        Estimate the mapping from the two-channel controls
        """

        if experiment is None:
            raise util.CytoflowOpError("No experiment specified")
        
        if not self.controls:
            raise util.CytoflowOpError("No controls specified")

        tubes = {}
        
        translation = {x[0] : x[1] for x in self.controls.keys()}
        
        for from_channel, to_channel in translation.iteritems():
            
            if from_channel not in experiment.channels:
                raise util.CytoflowOpError("Channel {0} not in the experiment"
                                      .format(from_channel))
                
            if to_channel not in experiment.channels:
                raise util.CytoflowOpError("Channel {0} not in the experiment"
                                      .format(to_channel))
            
            if (from_channel, to_channel) not in self.controls:
                raise util.CytoflowOpError("Control file for {0} --> {1} "
                                      "not specified"
                                      .format(from_channel, to_channel))
                
            tube_file = self.controls[(from_channel, to_channel)]
            
            if tube_file not in tubes: 
                # make a little Experiment
                check_tube(tube_file, experiment)
                tube_exp = ImportOp(tubes = [Tube(file = tube_file)],
                                    channels = {experiment.metadata[c]["fcs_name"] : c for c in experiment.channels},
                                    name_metadata = experiment.metadata['name_metadata']).apply()
                
                # apply previous operations
                for op in experiment.history:
                    tube_exp = op.apply(tube_exp) 

                # subset the events
                if subset:
                    try:
                        tube_exp = tube_exp.query(subset)
                    except:
                        raise util.CytoflowOpError("Subset string '{0}' isn't valid"
                                              .format(subset))
                                    
                    if len(tube_exp.data) == 0:
                        raise util.CytoflowOpError("Subset string '{0}' returned no events"
                                              .format(subset))
                
                tube_data = tube_exp.data                

                tubes[tube_file] = tube_data

                
            data = tubes[tube_file][[from_channel, to_channel]].copy()
            data = data[data[from_channel] > 0]
            data = data[data[to_channel] > 0]
            
            _ = data.reset_index(drop = True, inplace = True)
            
            data[from_channel] = np.log10(data[from_channel])
            data[to_channel] = np.log10(data[to_channel])
            
            if self.mixture_model:    
                gmm = sklearn.mixture.BayesianGaussianMixture(n_components=2)
                fit = gmm.fit(data)

                # pick the component with the maximum mean
                idx = 0 if fit.means_[0][0] > fit.means_[1][0] else 1
                weights = [x[idx] for x in fit.predict_proba(data)]
            else:
                weights = [1] * len(data.index)
            
            # this estimation method yields different results than the TASBE
            # method.  TASBE ..... does something with binned means, or
            # something ..... I can't read the MATLAB code too well, and I 
            # don't know if the code I have is the same as is running on the
            # TASBE website ...... anyways.  It computes a linear, multiplicative
            # scaling constant.  Ie, OUT = m * IN, where OUT is the color we're
            # translating TO and IN is the color we're translating FROM.
            
            # this code uses a different approach: it uses a log-linear model,
            # computing the linear Y = a * X + b coefficients on a log-log
            # plot.  this is a more general model of the underlying physical
            # behavior -- but it may not be more "correct."
            
            # which is better?  idunno.  i'd love to try EQUIP predictions with
            # both.  i'd like to note that i can't reproduce the TASBE method
            # precisely anyways; if i replace this with a linear model, i get
            # coefficients that are close to (but not quite the same as) the
            # TASBE website, and WAY off the color model I have in the same
            # directory as my test data.
             
            lr = np.polyfit(data[from_channel], 
                            data[to_channel], 
                            deg = 1, 
                            w = weights)
                        
            # remember, these (linear) coefficients came from logspace, so 
            # if the relationship in log10 space is Y = aX + b, then in
            # linear space the relationship is x = 10**X, y = 10**Y,
            # and y = (10**b) * x ^ a
            
            # also remember that the result of np.polyfit is a list of
            # coefficients with the highest power first!  so if we
            # solve y=ax + b, coeff #0 is a and coeff #1 is b
                 
            a = lr[0]
            b = 10 ** lr[1]
            trans_fn = lambda x, a=a, b=b: b * np.power(x, a)
  
            self._coefficients[(from_channel, to_channel)] = lr
            self._trans_fn[(from_channel, to_channel)] = trans_fn


    def apply(self, experiment):
        """Applies the color translation to an experiment
        
        Parameters
        ----------
        experiment : Experiment
            the old_experiment to which this op is applied
            
        Returns
        -------
            a new experiment with the color translation applied.
        """

        if experiment is None:
            raise util.CytoflowOpError("No experiment specified")
        
        if not self.controls:
            raise util.CytoflowOpError("No controls specified")
        
        if not self._trans_fn:
            raise util.CytoflowOpError("Transfer functions aren't set. "
                                  "Did you call estimate()?")
            
        translation = {x[0] : x[1] for x in self.controls.keys()}
        from_channels = [x[0] for x in self.controls.keys()]

        for key, val in translation.iteritems():
            if (key, val) not in self._coefficients:
                raise util.CytoflowOpError("Coefficients aren't set for translation "
                                      "{1} --> {2}.  Did you call estimate()?"
                                      .format(key, val))
                       
        new_experiment = experiment.clone()
        
        for channel in from_channels:
            new_experiment.data = \
                new_experiment.data[new_experiment.data[channel] > 0]
        
        for from_channel, to_channel in translation.iteritems():
            trans_fn = self._trans_fn[(from_channel, to_channel)]
                        
            new_experiment[from_channel] = trans_fn(experiment[from_channel])
            new_experiment.metadata[from_channel]['channel_translation_fn'] = trans_fn
            new_experiment.metadata[from_channel]['channel_translation'] = to_channel
            
        new_experiment.history.append(self.clone_traits(transient = lambda t: True))
            
        return new_experiment
    
    def default_view(self, **kwargs):
        """
        Returns a diagnostic plot to see if the bleedthrough spline estimation
        is working.
        
        Returns
        -------
            IView : An IView, call plot() to see the diagnostic plots
        """

        return ColorTranslationDiagnostic(op = self, **kwargs)
    
@provides(cytoflow.views.IView)
class ColorTranslationDiagnostic(HasStrictTraits):
    """
    Attributes
    ----------
    name : Str
        The instance name (for serialization, UI etc.)
    
    op : Instance(ColorTranslationOp)
        The op whose parameters we're viewing
    """
    
    # traits   
    id = "edu.mit.synbio.cytoflow.view.colortranslationdiagnostic"
    friendly_id = "Color Translation Diagnostic" 
    
    name = Str
    subset = Str
    
    # TODO - why can't I use ColorTranslationOp here?
    op = Instance(IOperation)
    
    def plot(self, experiment, **kwargs):
        """
        Plot the plots
        """
        
        if experiment is None:
            raise util.CytoflowViewError("No experiment specified")
        
        if not self.op.controls:
            raise util.CytoflowViewError("No controls specified")
        
        if not self.op._trans_fn:
            raise util.CytoflowViewError("Transfer functions aren't set. "
                                  "Did you call estimate()?")

        tubes = {}
        
        translation = {x[0] : x[1] for x in self.op.controls.keys()}
        
        plt.figure()
        num_plots = len(self.op.controls.keys())
        plt_idx = 0
        
        for from_channel, to_channel in translation.iteritems():
            
            if (from_channel, to_channel) not in self.op.controls:
                raise util.CytoflowViewError("Control file for {0} --> {1} not specified"
                                   .format(from_channel, to_channel))
            tube_file = self.op.controls[(from_channel, to_channel)]
            
            if tube_file not in tubes: 
                # make a little Experiment
                try:
                    check_tube(tube_file, experiment)
                    tube_exp = ImportOp(tubes = [Tube(file = tube_file)],
                                        channels = {experiment.metadata[c]["fcs_name"] : c for c in experiment.channels},
                                        name_metadata = experiment.metadata['name_metadata']).apply()
                except util.CytoflowOpError as e:
                    raise util.CytoflowViewError(e.__str__())
                
                # apply previous operations
                for op in experiment.history:
                    tube_exp = op.apply(tube_exp)
                    
                tube_data = tube_exp.data

                # subset the events
                if self.subset:
                    try:
                        tube_exp = tube_exp.query(self.subset)
                    except:
                        raise util.CytoflowViewError("Subset string '{0}' isn't valid"
                                              .format(self.subset))
                                    
                    if len(tube_exp.data) == 0:
                        raise util.CytoflowViewError("Subset string '{0}' returned no events"
                                              .format(self.subset))
                
                tube_data = tube_exp.data                

                tubes[tube_file] = tube_data               
                
            from_range = experiment.metadata[from_channel]['range']
            to_range = experiment.metadata[to_channel]['range']
            data = tubes[tube_file][[from_channel, to_channel]]
            data = data[data[from_channel] > 0]
            data = data[data[to_channel] > 0]
            _ = data.reset_index(drop = True, inplace = True)

            if self.op.mixture_model:    
                plt.subplot(num_plots, 2, plt_idx * 2 + 2)
                plt.xscale('log', nonposx='mask')
                hist_bins = np.logspace(1, math.log(from_range, 2), num = 128, base = 2)
                _ = plt.hist(data[from_channel],
                             bins = hist_bins,
                             histtype = 'stepfilled',
                             antialiased = True)
                plt.xlabel(from_channel)
                
                gmm = sklearn.mixture.GaussianMixture(n_components=2)
                fit = gmm.fit(np.log10(data[from_channel][:, np.newaxis]))
                    
                plt.axvline(10 ** fit.means_[0][0], color = 'r')
                plt.axvline(10 ** fit.means_[1][0], color = 'r')

            
            num_cols = 2 if self.op.mixture_model else 1
            plt.subplot(num_plots, num_cols, plt_idx * num_cols + 1)
            plt.xscale('log', nonposx = 'mask')
            plt.yscale('log', nonposy = 'mask')
            plt.xlabel(from_channel)
            plt.ylabel(to_channel)
            plt.xlim(1, from_range)
            plt.ylim(1, to_range)
            
            kwargs.setdefault('alpha', 0.2)
            kwargs.setdefault('s', 1)
            kwargs.setdefault('marker', 'o')
            
            plt.scatter(data[from_channel],
                        data[to_channel],
                        **kwargs)          

            xs = np.logspace(1, math.log(from_range, 2), num = 256, base = 2)
            trans_fn = self.op._trans_fn[(from_channel, to_channel)]
            plt.plot(xs, trans_fn(xs), "--g")
            
            
            plt_idx = plt_idx + 1
        
        plt.tight_layout(pad = 0.8)
