import numpy as np

from tick.base import actual_kwargs
from tick.inference.base import LearnerHawkesParametric
from tick.optim.model import ModelHawkesFixedSumExpKernLeastSq
from tick.optim.prox import ProxElasticNet, ProxL1, ProxL2Sq, ProxPositive
from tick.simulation.hawkes_sumexp_kernels import SimuHawkesSumExpKernels


class HawkesSumExpKern(LearnerHawkesParametric):
    """Hawkes process learner for sum-exponential kernels with fixed and given
    decays, with many choices of penalization and solvers.

    Hawkes processes are point processes defined by the intensity:

    .. math::
        \\forall i \\in [1 \\dots D], \\quad
        \\lambda_i(t) = \\mu_i + \\sum_{j=1}^D
        \\sum_{t_k^j < t} \\phi_{ij}(t - t_k^j)

    where

    * :math:`D` is the number of nodes
    * :math:`\mu_i` are the baseline intensities
    * :math:`\phi_{ij}` are the kernels
    * :math:`t_k^j` are the timestamps of all events of node :math:`j`

    and with an sum-exponential parametrisation of the kernels

    .. math::
        \phi_{ij}(t) = \sum_{u=1}^{U} \\alpha^u_{ij} \\beta^u
                       \exp (- \\beta^u t) 1_{t > 0}

    In our implementation we denote:

    * Integer :math:`D` by the attribute `n_nodes`
    * Integer :math:`U` by the attribute `n_decays`
    * Vector :math:`\mu \in \mathbb{R}^{D}` by the attribute
      `baseline`
    * Matrix :math:`A = (\\alpha^u_{ij})_{ij} \in \mathbb{R}^{D \\times D
      \\times U}` by the attribute `adjacency`
    * Vector :math:`\\beta \in \mathbb{R}^{U}` by the
      parameter `decays`. This parameter is given to the model

    Parameters
    ----------
    decays : `np.ndarray`, shape=(n_decays, )
        The decays used in the exponential kernels.
    
    C : `float`, default=1e3
        Level of penalization

    penalty : {'l1', 'l2', 'elasticnet', 'none'} default='l2'
        The penalization to use. Default is ridge penalization.

    solver : {'gd', 'agd', 'bfgs', 'svrg'}, default='agd'
        The name of the solver to use

    step : `float`, default=None
        Initial step size used for learning. Used in 'gd', 'agd', 'sgd'
        and 'svrg' solvers

    tol : `float`, default=1e-5
        The tolerance of the solver (iterations stop when the stopping
        criterion is below it). If not reached the solver does ``max_iter``
        iterations

    max_iter : `int`, default=100
        Maximum number of iterations of the solver

    verbose : `bool`, default=False
        If `True`, we verbose things, otherwise the solver does not
        print anything (but records information in history anyway)

    print_every : `int`, default=10
        Print history information when ``n_iter`` (iteration number) is
        a multiple of ``print_every``

    record_every : `int`, default=10
        Record history information when ``n_iter`` (iteration number) is
        a multiple of ``record_every``

    elastic_net_ratio : `float`, default=0.95
        Ratio of elastic net mixing parameter with 0 <= ratio <= 1.

        * For ratio = 0 this is ridge (L2 squared) regularization.
        * For ratio = 1 this is lasso (L1) regularization.
        * For 0 < ratio < 1, the regularization is a linear combination
          of L1 and L2.

        Used in 'elasticnet' penalty

    random_state : int seed, or None (default)
        The seed that will be used by stochastic solvers. If `None`, a random
        seed will be used (based on timestamp and other physical metrics).
        Used in 'sgd', and 'svrg' solvers

    Attributes
    ----------
    n_nodes : `int`
        Number of nodes / components in the Hawkes model

    baseline : `np.array`, shape=(n_nodes,)
        Inferred baseline of each component's intensity

    adjacency : `np.ndarray`, shape=(n_nodes, n_nodes, n_decays)
        Inferred adjacency matrix

    coeffs : `np.array`, shape=(n_nodes + n_nodes * n_nodes * n_decays, )
        Raw coefficients of the model. Row stack of `self.baseline` and
        `self.adjacency`
    """

    _attrinfos = {
        "n_decays": {"writable": False},
        "decays": {"writable": False},
    }

    _penalties = {
        "none": ProxPositive,
        "l1": ProxL1,
        "l2": ProxL2Sq,
        "elasticnet": ProxElasticNet,
    }

    @actual_kwargs
    def __init__(self, decays, penalty="l2", C=1e3,
                 solver="agd", step=None, tol=1e-5, max_iter=100,
                 verbose=False, print_every=10, record_every=10,
                 elastic_net_ratio=0.95, random_state=None):

        self._actual_kwargs = \
            HawkesSumExpKern.__init__.actual_kwargs

        self.decays = decays

        LearnerHawkesParametric.__init__(self, penalty=penalty, C=C,
                                         solver=solver, step=step, tol=tol,
                                         max_iter=max_iter, verbose=verbose,
                                         print_every=print_every,
                                         record_every=record_every,
                                         elastic_net_ratio=elastic_net_ratio,
                                         random_state=random_state)

    def _construct_model_obj(self):
        model = ModelHawkesFixedSumExpKernLeastSq(self.decays)
        return model

    @property
    def n_decays(self):
        return self._model_obj.n_decays

    @property
    def adjacency(self):
        if not self._fitted:
            raise ValueError('You must fit data before getting estimated '
                             'adjacency')
        else:
            return self.coeffs[self.n_nodes:].reshape((self.n_nodes,
                                                       self.n_nodes,
                                                       self.n_decays))

    def _corresponding_simu(self):
        return SimuHawkesSumExpKernels(adjacency=self.adjacency,
                                       decays=self.decays,
                                       baseline=self.baseline)
