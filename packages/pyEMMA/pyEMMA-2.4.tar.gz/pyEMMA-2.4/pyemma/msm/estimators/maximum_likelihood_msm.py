
# This file is part of PyEMMA.
#
# Copyright (c) 2015, 2014 Computational Molecular Biology Group, Freie Universitaet Berlin (GER)
#
# PyEMMA is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import

import numpy as _np
import warnings
from msmtools import estimation as msmest

from pyemma.util.annotators import alias, aliased, fix_docs
from pyemma.util.types import ensure_dtraj_list
from pyemma._base.estimator import Estimator as _Estimator
from pyemma.msm.estimators._dtraj_stats import DiscreteTrajectoryStats as _DiscreteTrajectoryStats
from pyemma.msm.models.msm import MSM as _MSM
from pyemma.util.units import TimeUnit as _TimeUnit
from pyemma.util import types as _types
from pyemma.msm.estimators._OOM_MSM import *


@fix_docs
@aliased
class _MSMEstimator(_Estimator, _MSM):
    r"""Base class for different MSM estimators given discrete trajectory statistics"""

    def __init__(self, lag=1, reversible=True, count_mode='sliding', sparse=False,
                 connectivity='largest', dt_traj='1 step', score_method='VAMP2', score_k=10):
        r"""Maximum likelihood estimator for MSMs given discrete trajectory statistics

        Parameters
        ----------
        lag : int
            lag time at which transitions are counted and the transition matrix is
            estimated.

        reversible : bool, optional, default = True
            If true compute reversible MSM, else non-reversible MSM

        count_mode : str, optional, default='sliding'
            mode to obtain count matrices from discrete trajectories. Should be
            one of:

            * 'sliding' : A trajectory of length T will have :math:`T-\tau` counts
              at time indexes

              .. math::

                 (0 \rightarrow \tau), (1 \rightarrow \tau+1), ..., (T-\tau-1 \rightarrow T-1)

            * 'effective' : Uses an estimate of the transition counts that are
              statistically uncorrelated. Recommended when used with a
              Bayesian MSM.
            * 'sample' : A trajectory of length T will have :math:`T/\tau` counts
              at time indexes

              .. math::

                    (0 \rightarrow \tau), (\tau \rightarrow 2 \tau), ..., (((T/tau)-1) \tau \rightarrow T)

        sparse : bool, optional, default = False
            If true compute count matrix, transition matrix and all derived
            quantities using sparse matrix algebra. In this case python sparse
            matrices will be returned by the corresponding functions instead of
            numpy arrays. This behavior is suggested for very large numbers of
            states (e.g. > 4000) because it is likely to be much more efficient.
        connectivity : str, optional, default = 'largest'
            Connectivity mode. Three methods are intended (currently only 'largest'
            is implemented)

            * 'largest' : The active set is the largest reversibly connected set.
              All estimation will be done on this subset and all quantities
              (transition matrix, stationary distribution, etc) are only defined
              on this subset and are correspondingly smaller than the full set
              of states
            * 'all' : The active set is the full set of states. Estimation will be
              conducted on each reversibly connected set separately. That means
              the transition matrix will decompose into disconnected submatrices,
              the stationary vector is only defined within subsets, etc.
              Currently not implemented.
            * 'none' : The active set is the full set of states. Estimation will
              be conducted on the full set of
              states without ensuring connectivity. This only permits
              nonreversible estimation. Currently not implemented.

        dt_traj : str, optional, default='1 step'
            Description of the physical time of the input trajectories. May be used
            by analysis algorithms such as plotting tools to pretty-print the axes.
            By default '1 step', i.e. there is no physical time unit. Specify by a
            number, whitespace and unit. Permitted units are (* is an arbitrary
            string):

            *  'fs',  'femtosecond*'
            *  'ps',  'picosecond*'
            *  'ns',  'nanosecond*'
            *  'us',  'microsecond*'
            *  'ms',  'millisecond*'
            *  's',   'second*'

        score_method : str, optional, default='VAMP2'
            Score to be used with score function - see there for documentation.

            *  'VAMP1'  Sum of singular values of the symmetrized transition matrix.
            *  'VAMP2'  Sum of squared singular values of the symmetrized transition matrix.

        score_k : int or None
            The maximum number of eigenvalues or singular values used in the
            score. If set to None, all available eigenvalues will be used.

        """
        self.lag = lag

        # set basic parameters
        self.reversible = reversible

        # sparse matrix computation wanted?
        self.sparse = sparse

        # store counting mode (lowercase)
        self.count_mode = str(count_mode).lower()
        if self.count_mode not in ('sliding', 'effective', 'sample'):
            raise ValueError('count mode ' + count_mode + ' is unknown.')

        # store connectivity mode (lowercase)
        self.connectivity = connectivity.lower()
        if self.connectivity == 'largest':
            pass  # this is the current default. no need to do anything
        elif self.connectivity == 'all':
            raise NotImplementedError('MSM estimation with connectivity=\'all\' is currently not implemented.')
        elif self.connectivity == 'none':
            raise NotImplementedError('MSM estimation with connectivity=\'none\' is currently not implemented.')
        else:
            raise ValueError('connectivity mode ' + str(connectivity) + ' is unknown.')

        # time step
        self.dt_traj = dt_traj
        self.timestep_traj = _TimeUnit(dt_traj)

        # score
        self.score_method = score_method
        self.score_k = score_k

    ################################################################################
    # Generic functions
    ################################################################################

    def _get_dtraj_stats(self, dtrajs):
        """ Compute raw trajectory counts

        Parameters
        ----------
        dtrajs : list containing ndarrays(dtype=int) or ndarray(n, dtype=int)
            or :class:`pyemma.msm.util.dtraj_states.DiscreteTrajectoryStats`
            discrete trajectories, stored as integer ndarrays (arbitrary size)
            or a single ndarray for only one trajectory.

        """
        # harvest discrete statistics
        if isinstance(dtrajs, _DiscreteTrajectoryStats):
            dtrajstats = dtrajs
        else:
            # compute and store discrete trajectory statistics
            dtrajstats = _DiscreteTrajectoryStats(dtrajs)
            # check if this MSM seems too large to be dense
            if dtrajstats.nstates > 4000 and not self.sparse:
                self.logger.warning('Building a dense MSM with ' + str(dtrajstats.nstates) + ' states. This can be '
                                    'inefficient or unfeasible in terms of both runtime and memory consumption. '
                                    'Consider using sparse=True.')

        # count lagged
        dtrajstats.count_lagged(self.lag, count_mode=self.count_mode)

        # for other statistics
        return dtrajstats

    def estimate(self, dtrajs, **parms):
        """
        Parameters
        ----------
        dtrajs : list containing ndarrays(dtype=int) or ndarray(n, dtype=int)
            or :class:`pyemma.msm.util.dtraj_states.DiscreteTrajectoryStats`
            discrete trajectories, stored as integer ndarrays (arbitrary size)
            or a single ndarray for only one trajectory.
        **params :
            Other keyword parameters if different from the settings when this estimator was constructed

        Returns
        -------
        MSM : :class:`pyemma.msm.MaximumlikelihoodMSM`

        """
        dtrajs = ensure_dtraj_list(dtrajs)  # ensure format
        return super(_MSMEstimator, self).estimate(dtrajs, **parms)

    def _check_is_estimated(self):
        assert self._is_estimated, 'You tried to access model parameters before estimating it - run estimate first!'

    def score(self, dtrajs, score_method=None, score_k=None):
        """ Scores the MSM using the dtrajs using the variational approach for Markov processes [1]_ [2]_

        Currently only implemented using dense matrices - will be slow for large state spaces.

        Parameters
        ----------
        dtrajs : list of arrays
            test data (discrete trajectories).
        score_method : str
            Overwrite scoring method if desired. If `None`, the estimators scoring
            method will be used. See __init__ for documention.
        score_k : str
            Overwrite scoring rank if desired. If `None`, the estimators scoring
            rank will be used. See __init__ for documention.
        score_method : str, optional, default='VAMP2'
            Overwrite scoring method to be used if desired. If `None`, the estimators scoring
            method will be used.
            Available scores are based on the variational approach for Markov processes [1]_ [2]_ :

            *  'VAMP1'  Sum of singular values of the symmetrized transition matrix [2]_ .
                        If the MSM is reversible, this is equal to the sum of transition
                        matrix eigenvalues, also called Rayleigh quotient [1]_ [3]_ .
            *  'VAMP2'  Sum of squared singular values of the symmetrized transition matrix [2]_ .
                        If the MSM is reversible, this is equal to the kinetic variance [4]_ .

        score_k : int or None
            The maximum number of eigenvalues or singular values used in the
            score. If set to None, all available eigenvalues will be used.

        References
        ----------
        .. [1] Noe, F. and F. Nueske: A variational approach to modeling slow processes
            in stochastic dynamical systems. SIAM Multiscale Model. Simul. 11, 635-655 (2013).
        .. [2] Wu, H and F. Noe: Variational approach for learning Markov processes
            from time series data (in preparation)
        .. [3] McGibbon, R and V. S. Pande: Variational cross-validation of slow
            dynamical modes in molecular kinetics, J. Chem. Phys. 142, 124105 (2015)
        .. [4] Noe, F. and C. Clementi: Kinetic distance and kinetic maps from molecular
            dynamics simulation. J. Chem. Theory Comput. 11, 5002-5011 (2015)

        """
        dtrajs = ensure_dtraj_list(dtrajs)  # ensure format

        # reset estimator data if needed
        if score_method is not None:
            self.score_method = score_method
        if self.score_k is not None:
            self.score_k = score_k

        # determine actual scoring rank
        if self.score_k is None:
            self.score_k = self.nstates
        if self.score_k > self.nstates:
            self.logger.warning('Requested scoring rank ' + str(self.score_k) +
                                'exceeds number of MSM states. Reduced to score_k = ' + str(self.nstates))
            self.score_k = self.nstates  # limit to nstates

        # training data
        K = self.transition_matrix  # model
        C0t_train = self.count_matrix_active
        from scipy.sparse import issparse
        if issparse(K):  # can't deal with sparse right now.
            K = K.toarray()
        if issparse(C0t_train):  # can't deal with sparse right now.
            C0t_train = C0t_train.toarray()
        C00_train = _np.diag(C0t_train.sum(axis=1))  # empirical cov
        Ctt_train = _np.diag(C0t_train.sum(axis=0))  # empirical cov

        # test data
        C0t_test_raw = msmest.count_matrix(dtrajs, self.lag, sparse_return=False)
        # map to present active set
        map_from = self.active_set[_np.where(self.active_set < C0t_test_raw.shape[0])[0]]
        map_to = _np.arange(len(map_from))
        C0t_test = _np.zeros((self.nstates, self.nstates))
        C0t_test[_np.ix_(map_to, map_to)] = C0t_test_raw[_np.ix_(map_from, map_from)]
        C00_test = _np.diag(C0t_test.sum(axis=1))
        Ctt_test = _np.diag(C0t_test.sum(axis=0))

        # score
        from pyemma.util.metrics import vamp_score
        return vamp_score(K, C00_train, C0t_train, Ctt_train, C00_test, C0t_test, Ctt_test,
                          k=self.score_k, score=self.score_method)

    def _blocksplit_dtrajs(self, dtrajs, sliding):
        from pyemma.msm.estimators._dtraj_stats import blocksplit_dtrajs
        return blocksplit_dtrajs(dtrajs, lag=self.lag, sliding=sliding)

    def score_cv(self, dtrajs, n=10, score_method=None, score_k=None):
        """ Scores the MSM using the variational approach for Markov processes [1]_ [2]_ and crossvalidation [3]_ .

        Divides the data into training and test data, fits a MSM using the training
        data using the parameters of this estimator, and scores is using the test
        data.
        Currently only one way of splitting is implemented, where for each n,
        the data is randomly divided into two approximately equally large sets of
        discrete trajectory fragments with lengths of at least the lagtime.

        Currently only implemented using dense matrices - will be slow for large state spaces.

        Parameters
        ----------
        dtrajs : list of arrays
            Test data (discrete trajectories).
        n : number of samples
            Number of repetitions of the cross-validation. Use large n to get solid
            means of the score.
        score_method : str, optional, default='VAMP2'
            Overwrite scoring method to be used if desired. If `None`, the estimators scoring
            method will be used.
            Available scores are based on the variational approach for Markov processes [1]_ [2]_ :

            *  'VAMP1'  Sum of singular values of the symmetrized transition matrix [2]_ .
                        If the MSM is reversible, this is equal to the sum of transition
                        matrix eigenvalues, also called Rayleigh quotient [1]_ [3]_ .
            *  'VAMP2'  Sum of squared singular values of the symmetrized transition matrix [2]_ .
                        If the MSM is reversible, this is equal to the kinetic variance [4]_ .

        score_k : int or None
            The maximum number of eigenvalues or singular values used in the
            score. If set to None, all available eigenvalues will be used.

        References
        ----------
        .. [1] Noe, F. and F. Nueske: A variational approach to modeling slow processes
            in stochastic dynamical systems. SIAM Multiscale Model. Simul. 11, 635-655 (2013).
        .. [2] Wu, H and F. Noe: Variational approach for learning Markov processes
            from time series data (in preparation).
        .. [3] McGibbon, R and V. S. Pande: Variational cross-validation of slow
            dynamical modes in molecular kinetics, J. Chem. Phys. 142, 124105 (2015).
        .. [4] Noe, F. and C. Clementi: Kinetic distance and kinetic maps from molecular
            dynamics simulation. J. Chem. Theory Comput. 11, 5002-5011 (2015).

        """
        dtrajs = ensure_dtraj_list(dtrajs)  # ensure format

        from pyemma.msm.estimators._dtraj_stats import cvsplit_dtrajs
        if self.count_mode not in ('sliding', 'sample'):
            raise ValueError('score_cv currently only supports count modes "sliding" and "sample"')
        sliding = self.count_mode == 'sliding'
        scores = []
        for i in range(n):
            dtrajs_split = self._blocksplit_dtrajs(dtrajs, sliding)
            dtrajs_train, dtrajs_test = cvsplit_dtrajs(dtrajs_split)
            self.fit(dtrajs_train)
            s = self.score(dtrajs_test, score_method=score_method, score_k=score_k)
            scores.append(s)
        return _np.array(scores)

    ################################################################################
    # Basic attributes
    ################################################################################

    @property
    def lagtime(self):
        """
        The lag time at which the Markov model was estimated

        """
        return self.lag

    @property
    def nstates_full(self):
        r""" Number of states in discrete trajectories """
        self._check_is_estimated()
        return self._nstates_full

    @property
    def active_set(self):
        """
        The active set of states on which all computations and estimations will be done

        """
        self._check_is_estimated()
        return self._active_set

    @active_set.setter
    def active_set(self, value):
        self._active_set = value

    @property
    def connectivity(self):
        """Returns the connectivity mode of the MSM """
        return self._connectivity

    @connectivity.setter
    def connectivity(self, value):
        self._connectivity = value

    @property
    def largest_connected_set(self):
        """
        The largest reversible connected set of states

        """
        self._check_is_estimated()
        return self._connected_sets[0]

    @property
    def connected_sets(self):
        """
        The reversible connected sets of states, sorted by size (descending)

        """
        self._check_is_estimated()
        return self._connected_sets

    @property
    @alias('dtrajs_full')
    def discrete_trajectories_full(self):
        """
        A list of integer arrays with the original (unmapped) discrete trajectories:

        """
        self._check_is_estimated()
        return self._dtrajs_full

    @property
    @alias('dtrajs_active')
    def discrete_trajectories_active(self):
        """
        A list of integer arrays with the discrete trajectories mapped to the connectivity mode used.
        For example, for connectivity='largest', the indexes will be given within the connected set.
        Frames that are not in the connected set will be -1.

        """
        self._check_is_estimated()
        # compute connected dtrajs
        self._dtrajs_active = []
        for dtraj in self._dtrajs_full:
            self._dtrajs_active.append(self._full2active[dtraj])

        return self._dtrajs_active

    @property
    def count_matrix_active(self):
        """The count matrix on the active set given the connectivity mode used.

        For example, for connectivity='largest', the count matrix is given only on the largest reversibly connected set.
        Attention: This count matrix has been obtained by sliding a window of length tau across the data. It contains
        a factor of tau more counts than are statistically uncorrelated. It's fine to use this matrix for maximum
        likelihood estimated, but it will give far too small errors if you use it for uncertainty calculations. In order
        to do uncertainty calculations, use the effective count matrix, see:
        :attr:`effective_count_matrix`

        See Also
        --------
        effective_count_matrix
            For a count matrix with effective (statistically uncorrelated) counts.

        """
        self._check_is_estimated()
        return self._C_active

    @property
    def count_matrix_full(self):
        """
        The count matrix on full set of discrete states, irrespective as to whether they are connected or not.
        Attention: This count matrix has been obtained by sliding a window of length tau across the data. It contains
        a factor of tau more counts than are statistically uncorrelated. It's fine to use this matrix for maximum
        likelihood estimated, but it will give far too small errors if you use it for uncertainty calculations. In order
        to do uncertainty calculations, use the effective count matrix, see: :attr:`effective_count_matrix`
        (only implemented on the active set), or divide this count matrix by tau.

        See Also
        --------
        effective_count_matrix
            For a active-set count matrix with effective (statistically uncorrelated) counts.

        """
        self._check_is_estimated()
        return self._C_full

    @property
    def active_state_fraction(self):
        """The fraction of states in the largest connected set.

        """
        self._check_is_estimated()
        return float(self._nstates) / float(self._nstates_full)

    @property
    def active_count_fraction(self):
        """The fraction of counts in the largest connected set.

        """
        self._check_is_estimated()
        from pyemma.util.discrete_trajectories import count_states

        hist = count_states(self._dtrajs_full)
        hist_active = hist[self.active_set]
        return float(_np.sum(hist_active)) / float(_np.sum(hist))

    ################################################################################
    # Generation of trajectories and samples
    ################################################################################

    @property
    def active_state_indexes(self):
        """
        Ensures that the connected states are indexed and returns the indices
        """
        self._check_is_estimated()
        try:  # if we have this attribute, return it
            return self._active_state_indexes
        except:  # didn't exist? then create it.
            import pyemma.util.discrete_trajectories as dt

            self._active_state_indexes = dt.index_states(self.discrete_trajectories_full, subset=self.active_set)
            return self._active_state_indexes

    def generate_traj(self, N, start=None, stop=None, stride=1):
        """Generates a synthetic discrete trajectory of length N and simulation time stride * lag time * N

        This information can be used
        in order to generate a synthetic molecular dynamics trajectory - see
        :func:`pyemma.coordinates.save_traj`

        Note that the time different between two samples is the Markov model lag time tau. When comparing
        quantities computing from this synthetic trajectory and from the input trajectories, the time points of this
        trajectory must be scaled by the lag time in order to have them on the same time scale.

        Parameters
        ----------
        N : int
            Number of time steps in the output trajectory. The total simulation time is stride * lag time * N
        start : int, optional, default = None
            starting state. If not given, will sample from the stationary distribution of P
        stop : int or int-array-like, optional, default = None
            stopping set. If given, the trajectory will be stopped before N steps
            once a state of the stop set is reached
        stride : int, optional, default = 1
            Multiple of lag time used as a time step. By default, the time step is equal to the lag time

        Returns
        -------
        indexes : ndarray( (N, 2) )
            trajectory and time indexes of the simulated trajectory. Each row consist of a tuple (i, t), where i is
            the index of the trajectory and t is the time index within the trajectory.
            Note that the time different between two samples is the Markov model lag time tau

        See also
        --------
        pyemma.coordinates.save_traj
            in order to save this synthetic trajectory as a trajectory file with molecular structures

        """
        # TODO: this is the only function left which does something time-related in a multiple of tau rather than dt.
        # TODO: we could generate dt-strided trajectories by sampling tau times from the current state, but that would
        # TODO: probably lead to a weird-looking trajectory. Maybe we could use a HMM to generate intermediate 'hidden'
        # TODO: frames. Anyway, this is a nontrivial issue.
        self._check_is_estimated()
        # generate synthetic states
        from msmtools.generation import generate_traj as _generate_traj

        syntraj = _generate_traj(self.transition_matrix, N, start=start, stop=stop, dt=stride)
        # result
        from pyemma.util.discrete_trajectories import sample_indexes_by_sequence

        return sample_indexes_by_sequence(self.active_state_indexes, syntraj)

    def sample_by_state(self, nsample, subset=None, replace=True):
        """Generates samples of the connected states.

        For each state in the active set of states, generates nsample samples with trajectory/time indexes.
        This information can be used in order to generate a trajectory of length nsample * nconnected using
        :func:`pyemma.coordinates.save_traj` or nconnected trajectories of length nsample each using
        :func:`pyemma.coordinates.save_traj`

        Parameters
        ----------
        nsample : int
            Number of samples per state. If replace = False, the number of returned samples per state could be smaller
            if less than nsample indexes are available for a state.
        subset : ndarray((n)), optional, default = None
            array of states to be indexed. By default all states in the connected set will be used
        replace : boolean, optional
            Whether the sample is with or without replacement

        Returns
        -------
        indexes : list of ndarray( (N, 2) )
            list of trajectory/time index arrays with an array for each state.
            Within each index array, each row consist of a tuple (i, t), where i is
            the index of the trajectory and t is the time index within the trajectory.

        See also
        --------
        pyemma.coordinates.save_traj
            in order to save the sampled frames sequentially in a trajectory file with molecular structures
        pyemma.coordinates.save_trajs
            in order to save the sampled frames in nconnected trajectory files with molecular structures

        """
        self._check_is_estimated()
        # generate connected state indexes
        import pyemma.util.discrete_trajectories as dt

        return dt.sample_indexes_by_state(self.active_state_indexes, nsample, subset=subset, replace=replace)

    # TODO: add sample_metastable() for sampling from metastable (pcca or hmm) states.
    def sample_by_distributions(self, distributions, nsample):
        """Generates samples according to given probability distributions

        Parameters
        ----------
        distributions : list or array of ndarray ( (n) )
            m distributions over states. Each distribution must be of length n and must sum up to 1.0
        nsample : int
            Number of samples per distribution. If replace = False, the number of returned samples per state could be
            smaller if less than nsample indexes are available for a state.

        Returns
        -------
        indexes : length m list of ndarray( (nsample, 2) )
            List of the sampled indices by distribution.
            Each element is an index array with a number of rows equal to nsample, with rows consisting of a
            tuple (i, t), where i is the index of the trajectory and t is the time index within the trajectory.

        """
        self._check_is_estimated()
        # generate connected state indexes
        import pyemma.util.discrete_trajectories as dt

        return dt.sample_indexes_by_distribution(self.active_state_indexes, distributions, nsample)

    ################################################################################
    # For general statistics
    ################################################################################

    def trajectory_weights(self):
        r"""Uses the MSM to assign a probability weight to each trajectory frame.

        This is a powerful function for the calculation of arbitrary observables in the trajectories one has
        started the analysis with. The stationary probability of the MSM will be used to reweigh all states.
        Returns a list of weight arrays, one for each trajectory, and with a number of elements equal to
        trajectory frames. Given :math:`N` trajectories of lengths :math:`T_1` to :math:`T_N`, this function
        returns corresponding weights:

        .. math::

            (w_{1,1}, ..., w_{1,T_1}), (w_{N,1}, ..., w_{N,T_N})

        that are normalized to one:

        .. math::

            \sum_{i=1}^N \sum_{t=1}^{T_i} w_{i,t} = 1

        Suppose you are interested in computing the expectation value of a function :math:`a(x)`, where :math:`x`
        are your input configurations. Use this function to compute the weights of all input configurations and
        obtain the estimated expectation by:

        .. math::

            \langle a \rangle = \sum_{i=1}^N \sum_{t=1}^{T_i} w_{i,t} a(x_{i,t})

        Or if you are interested in computing the time-lagged correlation between functions :math:`a(x)` and
        :math:`b(x)` you could do:

        .. math::

            \langle a(t) b(t+\tau) \rangle_t = \sum_{i=1}^N \sum_{t=1}^{T_i} w_{i,t} a(x_{i,t}) a(x_{i,t+\tau})


        Returns
        -------
        weights : list of ndarray
            The normalized trajectory weights. Given :math:`N` trajectories of lengths :math:`T_1` to :math:`T_N`,
            returns the corresponding weights:

            .. math::

                (w_{1,1}, ..., w_{1,T_1}), (w_{N,1}, ..., w_{N,T_N})

        """
        self._check_is_estimated()
        # compute stationary distribution, expanded to full set
        statdist_full = _np.zeros([self._nstates_full])
        statdist_full[self.active_set] = self.stationary_distribution
        # histogram observed states
        import msmtools.dtraj as msmtraj
        hist = 1.0 * msmtraj.count_states(self.discrete_trajectories_full)
        # simply read off stationary distribution and accumulate total weight
        W = []
        wtot = 0.0
        for dtraj in self.discrete_trajectories_full:
            w = statdist_full[dtraj] / hist[dtraj]
            W.append(w)
            wtot += _np.sum(w)
        # normalize
        for w in W:
            w /= wtot
        # done
        return W

    ################################################################################
    # HMM-based coarse graining
    ################################################################################

    def hmm(self, nhidden):
        """Estimates a hidden Markov state model as described in [1]_

        Parameters
        ----------
        nhidden : int
            number of hidden (metastable) states

        Returns
        -------
        hmsm : :class:`MaximumLikelihoodHMSM`

        References
        ----------
        .. [1] F. Noe, H. Wu, J.-H. Prinz and N. Plattner:
            Projected and hidden Markov models for calculating kinetics and metastable states of complex molecules
            J. Chem. Phys. 139, 184114 (2013)

        """
        self._check_is_estimated()
        # check if the time-scale separation is OK
        # if hmm.nstates = msm.nstates there is no problem. Otherwise, check spectral gap
        if self.nstates > nhidden:
            timescale_ratios = self.timescales()[:-1] / self.timescales()[1:]
            if timescale_ratios[nhidden-2] < 1.5:
                self.logger.warning('Requested coarse-grained model with ' + str(nhidden) + ' metastable states at ' +
                                    'lag=' + str(self.lag) + '.' + 'The ratio of relaxation timescales between ' +
                                    str(nhidden) + ' and ' + str(nhidden+1) + ' states is only ' +
                                    str(timescale_ratios[nhidden-2]) + ' while we recommend at least 1.5. ' +
                                    'It is possible that the resulting HMM is inaccurate. Handle with caution.')
        # run HMM estimate
        from pyemma.msm.estimators.maximum_likelihood_hmsm import MaximumLikelihoodHMSM
        estimator = MaximumLikelihoodHMSM(lag=self.lagtime, nstates=nhidden, msm_init=self,
                                          reversible=self.is_reversible, dt_traj=self.dt_traj)
        estimator.estimate(self.discrete_trajectories_full)
        return estimator.model

    def coarse_grain(self, ncoarse, method='hmm'):
        r"""Returns a coarse-grained Markov model.

        Currently only the HMM method described in [1]_ is available for coarse-graining MSMs.

        Parameters
        ----------
        ncoarse : int
            number of coarse states

        Returns
        -------
        hmsm : :class:`MaximumLikelihoodHMSM`

        References
        ----------
        .. [1] F. Noe, H. Wu, J.-H. Prinz and N. Plattner:
            Projected and hidden Markov models for calculating kinetics and metastable states of complex molecules
            J. Chem. Phys. 139, 184114 (2013)

        """
        self._check_is_estimated()
        # check input
        assert _types.is_int(self.nstates) and 1 < ncoarse <= self.nstates, \
            'nstates must be an int in [2,msmobj.nstates]'

        return self.hmm(ncoarse)

    ################################################################################
    # MODEL VALIDATION
    ################################################################################

    def cktest(self, nsets, memberships=None, mlags=10, conf=0.95, err_est=False,
               n_jobs=1, show_progress=True):
        """ Conducts a Chapman-Kolmogorow test.

        Parameters
        ----------
        nsets : int
            number of sets to test on
        memberships : ndarray(nstates, nsets), optional
            optional state memberships. By default (None) will conduct a cktest
            on PCCA (metastable) sets.
        mlags : int or int-array, optional
            multiples of lag times for testing the Model, e.g. range(10).
            A single int will trigger a range, i.e. mlags=10 maps to
            mlags=range(10). The setting None will choose mlags automatically
            according to the longest available trajectory
        conf : float, optional
            confidence interval
        err_est : bool, optional
            compute errors also for all estimations (computationally expensive)
            If False, only the prediction will get error bars, which is often
            sufficient to validate a model.
        n_jobs : int, default=1
            how many jobs to use during calculation
        show_progress : bool, optional
            Show progress bars for calculation?

        Returns
        -------
        cktest : :class:`ChapmanKolmogorovValidator <pyemma.msm.ChapmanKolmogorovValidator>`


        References
        ----------
        This test was suggested in [1]_ and described in detail in [2]_.

        .. [1] F. Noe, Ch. Schuette, E. Vanden-Eijnden, L. Reich and
            T. Weikl: Constructing the Full Ensemble of Folding Pathways
            from Short Off-Equilibrium Simulations.
            Proc. Natl. Acad. Sci. USA, 106, 19011-19016 (2009)
        .. [2] Prinz, J H, H Wu, M Sarich, B Keller, M Senne, M Held, J D
            Chodera, C Schuette and F Noe. 2011. Markov models of
            molecular kinetics: Generation and validation. J Chem Phys
            134: 174105

        """
        from pyemma.msm.estimators import ChapmanKolmogorovValidator
        if memberships is None:
            self.pcca(nsets)
            memberships = self.metastable_memberships
        ck = ChapmanKolmogorovValidator(self, self, memberships, mlags=mlags, conf=conf,
                                        n_jobs=n_jobs, err_est=err_est, show_progress=show_progress)
        ck.estimate(self._dtrajs_full)
        return ck


@fix_docs
@aliased
class MaximumLikelihoodMSM(_MSMEstimator):
    r"""Maximum likelihood estimator for MSMs given discrete trajectory statistics"""

    def __init__(self, lag=1, reversible=True, statdist_constraint=None,
                 count_mode='sliding', sparse=False,
                 connectivity='largest', dt_traj='1 step', maxiter=1000000,
                 maxerr=1e-8, score_method='VAMP2', score_k=10):
        r"""Maximum likelihood estimator for MSMs given discrete trajectory statistics

        Parameters
        ----------
        lag : int
            lag time at which transitions are counted and the transition matrix is
            estimated.

        reversible : bool, optional, default = True
            If true compute reversible MSM, else non-reversible MSM

        statdist : (M,) ndarray, optional
            Stationary vector on the full set of states. Estimation will be
            made such the the resulting transition matrix has this distribution
            as an equilibrium distribution. Set probabilities to zero if these
            states should be excluded from the analysis.

        count_mode : str, optional, default='sliding'
            mode to obtain count matrices from discrete trajectories. Should be
            one of:

            * 'sliding' : A trajectory of length T will have :math:`T-tau` counts
              at time indexes

              .. math::

                 (0 \rightarrow \tau), (1 \rightarrow \tau+1), ..., (T-\tau-1 \rightarrow T-1)

            * 'effective' : Uses an estimate of the transition counts that are
              statistically uncorrelated. Recommended when used with a
              Bayesian MSM.
            * 'sample' : A trajectory of length T will have :math:`T/tau` counts
              at time indexes

              .. math::

                    (0 \rightarrow \tau), (\tau \rightarrow 2 \tau), ..., (((T/tau)-1) \tau \rightarrow T)

        sparse : bool, optional, default = False
            If true compute count matrix, transition matrix and all derived
            quantities using sparse matrix algebra. In this case python sparse
            matrices will be returned by the corresponding functions instead of
            numpy arrays. This behavior is suggested for very large numbers of
            states (e.g. > 4000) because it is likely to be much more efficient.
        connectivity : str, optional, default = 'largest'
            Connectivity mode. Three methods are intended (currently only 'largest'
            is implemented)

            * 'largest' : The active set is the largest reversibly connected set.
              All estimation will be done on this subset and all quantities
              (transition matrix, stationary distribution, etc) are only defined
              on this subset and are correspondingly smaller than the full set
              of states
            * 'all' : The active set is the full set of states. Estimation will be
              conducted on each reversibly connected set separately. That means
              the transition matrix will decompose into disconnected submatrices,
              the stationary vector is only defined within subsets, etc.
              Currently not implemented.
            * 'none' : The active set is the full set of states. Estimation will
              be conducted on the full set of
              states without ensuring connectivity. This only permits
              nonreversible estimation. Currently not implemented.

        dt_traj : str, optional, default='1 step'
            Description of the physical time of the input trajectories. May be used
            by analysis algorithms such as plotting tools to pretty-print the axes.
            By default '1 step', i.e. there is no physical time unit. Specify by a
            number, whitespace and unit. Permitted units are (* is an arbitrary
            string):

            |  'fs',  'femtosecond*'
            |  'ps',  'picosecond*'
            |  'ns',  'nanosecond*'
            |  'us',  'microsecond*'
            |  'ms',  'millisecond*'
            |  's',   'second*'

        maxiter: int, optioanl, default = 1000000
            Optional parameter with reversible = True. maximum number of iterations
            before the transition matrix estimation method exits
        maxerr : float, optional, default = 1e-8
            Optional parameter with reversible = True.
            convergence tolerance for transition matrix estimation.
            This specifies the maximum change of the Euclidean norm of relative
            stationary probabilities (:math:`x_i = \sum_k x_{ik}`). The relative
            stationary probability changes
            :math:`e_i = (x_i^{(1)} - x_i^{(2)})/(x_i^{(1)} + x_i^{(2)})` are used
            in order to track changes in small probabilities. The Euclidean norm
            of the change vector, :math:`|e_i|_2`, is compared to maxerr.

        score_method : str, optional, default='VAMP2'
            Score to be used with score function. Available are:

            |  'VAMP1'  [1]_
            |  'VAMP2'  [1]_
            |  'VAMPE'  [1]_

        score_k : int or None
            The maximum number of eigenvalues or singular values used in the
            score. If set to None, all available eigenvalues will be used.

        References
        ----------
        .. [1] H. Wu and F. Noe: Variational approach for learning Markov processes from time series data
            (in preparation)

        """
        super(MaximumLikelihoodMSM, self).__init__(lag=lag, reversible=reversible, count_mode=count_mode,
                                                   sparse=sparse, connectivity=connectivity, dt_traj=dt_traj,
                                                   score_method=score_method, score_k=score_k)
        
        self.statdist_constraint = _types.ensure_ndarray_or_None(statdist_constraint, ndim=None, kind='numeric')
        if self.statdist_constraint is not None:  # renormalize
            self.statdist_constraint /= self.statdist_constraint.sum()

        # convergence parameters
        self.maxiter = maxiter
        self.maxerr = maxerr

    def _prepare_input_revpi(self, C, pi):
        """Max. state index visited by trajectories"""
        nC = C.shape[0]
        # Max. state index of the stationary vector array
        npi = pi.shape[0]
        # pi has to be defined on all states visited by the trajectories
        if nC > npi:
            errstr = """There are visited states for which no stationary
            probability is given"""
            raise ValueError(errstr)
        # Reduce pi to the visited set
        pi_visited = pi[0:nC]
        # Find visited states with positive stationary probabilities"""
        pos = _np.where(pi_visited > 0.0)[0]
        # Reduce C to positive probability states"""
        C_pos = msmest.connected_cmatrix(C, lcc=pos)
        if C_pos.sum() == 0.0:
            errstr = """The set of states with positive stationary
            probabilities is not visited by the trajectories. A MSM
            reversible with respect to the given stationary vector can
            not be estimated"""
            raise ValueError(errstr)
        # Compute largest connected set of C_pos, undirected connectivity"""
        lcc = msmest.largest_connected_set(C_pos, directed=False)
        return pos[lcc]

    def _estimate(self, dtrajs):
        """ Estimates the MSM """
        # get trajectory counts. This sets _C_full and _nstates_full
        dtrajstats = self._get_dtraj_stats(dtrajs)
        self._C_full = dtrajstats.count_matrix()  # full count matrix
        self._nstates_full = self._C_full.shape[0]  # number of states

        # set active set. This is at the same time a mapping from active to full
        if self.connectivity == 'largest':
            if self.statdist_constraint is None:
                # statdist not given - full connectivity on all states
                self.active_set = dtrajstats.largest_connected_set
            else:
                active_set = self._prepare_input_revpi(self._C_full,
                                                       self.statdist_constraint)
                self.active_set = active_set
        else:
            # for 'None' and 'all' all visited states are active
            self.active_set = dtrajstats.visited_set

        # FIXME: setting is_estimated before so that we can start using the parameters just set, but this is not clean!
        # is estimated
        self._is_estimated = True

        # if active set is empty, we can't do anything.
        if _np.size(self.active_set) == 0:
            raise RuntimeError('Active set is empty. Cannot estimate MSM.')

        # active count matrix and number of states
        self._C_active = dtrajstats.count_matrix(subset=self.active_set)
        self._nstates = self._C_active.shape[0]

        # computed derived quantities
        # back-mapping from full to lcs
        self._full2active = -1 * _np.ones(dtrajstats.nstates, dtype=int)
        self._full2active[self.active_set] = _np.arange(len(self.active_set))

        # restrict stationary distribution to active set
        if self.statdist_constraint is None:
            statdist_active = None
        else:
            statdist_active = self.statdist_constraint[self.active_set]
            statdist_active /= statdist_active.sum()  # renormalize

        # Estimate transition matrix
        if self.connectivity == 'largest':
            P = msmest.transition_matrix(self._C_active, reversible=self.reversible,
                                         mu=statdist_active, maxiter=self.maxiter,
                                         maxerr=self.maxerr)
        elif self.connectivity == 'none':
            # reversible mode only possible if active set is connected
            # - in this case all visited states are connected and thus
            # this mode is identical to 'largest'
            if self.reversible and not msmest.is_connected(self._C_active):
                raise ValueError('Reversible MSM estimation is not possible with connectivity mode "none", '
                                 'because the set of all visited states is not reversibly connected')
            P = msmest.transition_matrix(self._C_active, reversible=self.reversible,
                                         mu=statdist_active,
                                         maxiter=self.maxiter, maxerr=self.maxerr)
        else:
            raise NotImplementedError(
                'MSM estimation with connectivity=%s is currently not implemented.' % self.connectivity)

        # continue sparse or dense?
        if not self.sparse:
            # converting count matrices to arrays. As a result the
            # transition matrix and all subsequent properties will be
            # computed using dense arrays and dense matrix algebra.
            self._C_full = self._C_full.toarray()
            self._C_active = self._C_active.toarray()
            P = P.toarray()

        # Done. We set our own model parameters, so this estimator is
        # equal to the estimated model.
        self._dtrajs_full = dtrajs
        self._connected_sets = msmest.connected_sets(self._C_full)
        self.set_model_params(P=P, pi=statdist_active, reversible=self.reversible,
                              dt_model=self.timestep_traj.get_scaled(self.lag))

        return self

    # TODO: change to statistically effective count matrix!
    @property
    def effective_count_matrix(self):
        """Statistically uncorrelated transition counts within the active set of states

        You can use this count matrix for Bayesian estimation or error perturbation.

        References
        ----------
        [1] Noe, F. (2015) Statistical inefficiency of Markov model count matrices
            http://publications.mi.fu-berlin.de/1699/1/autocorrelation_counts.pdf

        """
        self._check_is_estimated()
        Ceff_full = msmest.effective_count_matrix(self._dtrajs_full, self.lag)
        from pyemma.util.linalg import submatrix
        Ceff = submatrix(Ceff_full, self.active_set)
        return Ceff
        # return self._C_active / float(self.lag)


@fix_docs
@aliased
class OOMReweightedMSM(_MSMEstimator):
    r"""OOM based estimator for MSMs given discrete trajectory statistics"""

    def __init__(self, lag=1, reversible=True, count_mode='sliding', sparse=False, connectivity='largest',
                 dt_traj='1 step', nbs=10000, rank_Ct='bootstrap_counts', tol_rank=10.0,
                 score_method='VAMP2', score_k=10):
        r"""Maximum likelihood estimator for MSMs given discrete trajectory statistics

        Parameters
        ----------
        lag : int
            lag time at which transitions are counted and the transition matrix is
            estimated.

        reversible : bool, optional, default = True
            If true compute reversible MSM, else non-reversible MSM

        count_mode : str, optional, default='sliding'
            mode to obtain count matrices from discrete trajectories. Should be
            one of:

            * 'sliding' : A trajectory of length T will have :math:`T-tau` counts
              at time indexes

              .. math::

                 (0 \rightarrow \tau), (1 \rightarrow \tau+1), ..., (T-\tau-1 \rightarrow T-1)
            * 'sample' : A trajectory of length T will have :math:`T/tau` counts
              at time indexes

              .. math::

                    (0 \rightarrow \tau), (\tau \rightarrow 2 \tau), ..., (((T/tau)-1) \tau \rightarrow T)

        sparse : bool, optional, default = False
            If true compute count matrix, transition matrix and all derived
            quantities using sparse matrix algebra. In this case python sparse
            matrices will be returned by the corresponding functions instead of
            numpy arrays. This behavior is suggested for very large numbers of
            states (e.g. > 4000) because it is likely to be much more efficient.
        connectivity : str, optional, default = 'largest'
            Connectivity mode. Three methods are intended (currently only 'largest'
            is implemented)

            * 'largest' : The active set is the largest reversibly connected set.
              All estimation will be done on this subset and all quantities
              (transition matrix, stationary distribution, etc) are only defined
              on this subset and are correspondingly smaller than the full set
              of states
            * 'all' : The active set is the full set of states. Estimation will be
              conducted on each reversibly connected set separately. That means
              the transition matrix will decompose into disconnected submatrices,
              the stationary vector is only defined within subsets, etc.
              Currently not implemented.
            * 'none' : The active set is the full set of states. Estimation will
              be conducted on the full set of
              states without ensuring connectivity. This only permits
              nonreversible estimation. Currently not implemented.

        dt_traj : str, optional, default='1 step'
            Description of the physical time of the input trajectories. May be used
            by analysis algorithms such as plotting tools to pretty-print the axes.
            By default '1 step', i.e. there is no physical time unit. Specify by a
            number, whitespace and unit. Permitted units are (* is an arbitrary
            string):

            |  'fs',  'femtosecond*'
            |  'ps',  'picosecond*'
            |  'ns',  'nanosecond*'
            |  'us',  'microsecond*'
            |  'ms',  'millisecond*'
            |  's',   'second*'

        nbs : int, optional, default=10000
            number of re-samplings for rank decision in OOM estimation.

        rank_Ct : str, optional
            Re-sampling method for model rank selection. Can be
            * 'bootstrap_counts': Directly re-sample transitions based on effective count matrix.

            * 'bootstrap_trajs': Re-draw complete trajectories with replacement.

        tol_rank: float, optional, default = 10.0
            signal-to-noise threshold for rank decision.

        score_method : str, optional, default='VAMP2'
            Score to be used with score function. Available are:

            |  'VAMP1'  [1]_
            |  'VAMP2'  [1]_
            |  'VAMPE'  [1]_

        score_k : int or None
            The maximum number of eigenvalues or singular values used in the
            score. If set to None, all available eigenvalues will be used.

        References
        ----------
        .. [1] H. Wu and F. Noe: Variational approach for learning Markov processes from time series data
            (in preparation)

        """
        # Check count mode:
        self.count_mode = str(count_mode).lower()
        if self.count_mode not in ('sliding', 'sample'):
            raise ValueError('count mode ' + count_mode + ' is unknown. Only \'sliding\' and \'sample\' are allowed.')
        if rank_Ct not in ('bootstrap_counts', 'bootstrap_trajs'):
            raise ValueError('rank_Ct must be either \'bootstrap_counts\' or \'bootstrap_trajs\'')

        super(OOMReweightedMSM, self).__init__(lag=lag, reversible=reversible, count_mode=count_mode, sparse=sparse,
                                               connectivity=connectivity, dt_traj=dt_traj,
                                               score_method=score_method, score_k=score_k)
        self.nbs = nbs
        self.tol_rank = tol_rank
        self.rank_Ct = rank_Ct

    def _estimate(self, dtrajs):
        """ Estimate MSM """
        # remove last lag steps from dtrajs:
        dtrajs_lag = [traj[:-self.lag] for traj in dtrajs]

        # get trajectory counts. This sets _C_full and _nstates_full
        dtrajstats = self._get_dtraj_stats(dtrajs_lag)
        self._C_full = dtrajstats.count_matrix()  # full count matrix
        self._nstates_full = self._C_full.shape[0]  # number of states

        # set active set. This is at the same time a mapping from active to full
        if self.connectivity == 'largest':
            self.active_set = dtrajstats.largest_connected_set
        else:
            raise NotImplementedError('OOM based MSM estimation is only implemented for connectivity=\'largest\'.')

        # FIXME: setting is_estimated before so that we can start using the parameters just set, but this is not clean!
        # is estimated
        self._is_estimated = True

        # if active set is empty, we can't do anything.
        if _np.size(self.active_set) == 0:
            raise RuntimeError('Active set is empty. Cannot estimate MSM.')

        # active count matrix and number of states
        self._C_active = dtrajstats.count_matrix(subset=self.active_set)
        self._nstates = self._C_active.shape[0]

        # computed derived quantities
        # back-mapping from full to lcs
        self._full2active = -1 * _np.ones(dtrajstats.nstates, dtype=int)
        self._full2active[self.active_set] = _np.arange(len(self.active_set))

        # Estimate transition matrix
        if self.connectivity == 'largest':
            # Re-sampling:
            if self.rank_Ct == 'bootstrap_counts':
                Ceff_full = msmest.effective_count_matrix(dtrajs_lag, self.lag)
                from pyemma.util.linalg import submatrix
                Ceff = submatrix(Ceff_full, self.active_set)
                smean, sdev = bootstrapping_count_matrix(Ceff, nbs=self.nbs)
            else:
                smean, sdev = bootstrapping_dtrajs(dtrajs_lag, self.lag, self._nstates_full, nbs=self.nbs,
                                                   active_set=self._active_set)
            # Estimate two step count matrices:
            C2t = twostep_count_matrix(dtrajs, self.lag, self._nstates_full)
            # Rank decision:
            rank_ind = rank_decision(smean, sdev, tol=self.tol_rank)
            # Estimate OOM components:
            Xi, omega, sigma, l = oom_components(self._C_full.toarray(), C2t, rank_ind=rank_ind,
                                                 lcc=self.active_set)
            # Compute transition matrix:
            P, lcc_new = equilibrium_transition_matrix(Xi, omega, sigma, reversible=self.reversible)
        else:
            raise NotImplementedError('OOM based MSM estimation is only implemented for connectivity=\'largest\'.')

        # Update active set and derived quantities:
        if lcc_new.size < self._nstates:
            self._active_set = self._active_set[lcc_new]
            self._C_active = dtrajstats.count_matrix(subset=self.active_set)
            self._nstates = self._C_active.shape[0]
            self._full2active = -1 * _np.ones(dtrajstats.nstates, dtype=int)
            self._full2active[self.active_set] = _np.arange(len(self.active_set))
            warnings.warn("Caution: Re-estimation of count matrix resulted in reduction of the active set.")

        # continue sparse or dense?
        if not self.sparse:
            # converting count matrices to arrays. As a result the
            # transition matrix and all subsequent properties will be
            # computed using dense arrays and dense matrix algebra.
            self._C_full = self._C_full.toarray()
            self._C_active = self._C_active.toarray()

        # Done. We set our own model parameters, so this estimator is
        # equal to the estimated model.
        self._dtrajs_full = dtrajs
        self._connected_sets = msmest.connected_sets(self._C_full)
        self._Xi = Xi
        self._omega = omega
        self._sigma = sigma
        self._eigenvalues_OOM = l
        self._rank_ind = rank_ind
        self._oom_rank = self._sigma.size
        self._C2t = C2t
        self.set_model_params(P=P, pi=None, reversible=self.reversible,
                              dt_model=self.timestep_traj.get_scaled(self.lag))

        return self

    def _blocksplit_dtrajs(self, dtrajs, sliding):
        """ Override splitting method of base class.

        For OOM estimators we currently need a clean trajectory splitting, i.e. we don't do block splitting at all.

        """
        if len(dtrajs) < 2:
            raise NotImplementedError('Current cross-validation implementation for OOMReweightedMSM requires' +
                                      'multiple trajectories. You can split the trajectory yourself into training' +
                                      'and test set and use the score method after fitting the training set.')
        return dtrajs

    @property
    def eigenvalues_OOM(self):
        """
            System eigenvalues estimated by OOM.

        """
        self._check_is_estimated()
        return self._eigenvalues_OOM

    @property
    def timescales_OOM(self):
        """
            System timescales estimated by OOM.

        """
        self._check_is_estimated()
        return -self.lag / _np.log(_np.abs(self._eigenvalues_OOM[1:]))

    @property
    def OOM_rank(self):
        """
            Return OOM model rank.

        """
        self._check_is_estimated()
        return self._oom_rank

    @property
    def OOM_components(self):
        """
            Return OOM components.

        """
        self._check_is_estimated()
        return self._Xi

    @property
    def OOM_omega(self):
        """
            Return OOM initial state vector.

        """
        self._check_is_estimated()
        return self._omega

    @property
    def OOM_sigma(self):
        """
            Return OOM evaluator vector.

        """
        self._check_is_estimated()
        return self._sigma
