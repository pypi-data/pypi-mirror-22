import logging
import numpy as np
import scipy as sp

import matplotlib
import matplotlib.pyplot as plt

from elfi.bo.utils import stochastic_optimization

logger = logging.getLogger(__name__)


class BolfiPosterior(object):
    """
    Container for the approximate posterior in the BOLFI framework, where the likelihood
    is defined as

    L \propto F((h - \mu) / \sigma)

    where F is the cdf of N(0,1), h is a threshold, and \mu and \sigma are the mean and (noisy)
    standard deviation of the Gaussian process.

    Note that when using a log discrepancy, h should become log(h).

    References
    ----------
    Gutmann M U, Corander J (2016). Bayesian Optimization for Likelihood-Free Inference
    of Simulator-Based Statistical Models. JMLR 17(125):1−47, 2016.
    http://jmlr.org/papers/v17/15-017.html

    Parameters
    ----------
    model : object
        Instance of the surrogate model, e.g. elfi.bo.gpy_regression.GPyRegression.
    threshold : float, optional
        The threshold value used in the calculation of the posterior, see the BOLFI paper for details.
        By default, the minimum value of discrepancy estimate mean is used.
    priors : list of elfi.Priors, optional
        By default uniform distribution within model bounds.
    max_opt_iters : int, optional
        Maximum number of iterations performed in internal optimization.
    """

    def __init__(self, model, threshold=None, priors=None, max_opt_iters=10000):
        super(BolfiPosterior, self).__init__()
        self.threshold = threshold
        self.model = model
        if self.threshold is None:
            minloc, minval = stochastic_optimization(self.model.predict_mean, self.model.bounds, max_opt_iters)
            self.threshold = minval
            logger.info("Using minimum value of discrepancy estimate mean (%.4f) as threshold" % (self.threshold))
        self.priors = priors or [None] * model.input_dim
        self.max_opt_iters = max_opt_iters

    @property
    def ML(self):
        """
        Maximum likelihood (ML) approximation.

        Returns
        -------
        tuple
            Maximum likelihood parameter values and the corresponding value of neg_unnormalized_loglikelihood.
        """
        x, lh_x = stochastic_optimization(self._neg_unnormalized_loglikelihood,
                                          self.model.bounds, self.max_opt_iters)
        return x, lh_x

    @property
    def MAP(self):
        """
        Maximum a posteriori (MAP) approximation.

        Returns
        -------
        tuple
            Maximum a posteriori parameter values and the corresponding value of neg_unnormalized_logposterior.
        """
        x, post_x = stochastic_optimization(self._neg_unnormalized_logposterior,
                                            self.model.bounds, self.max_opt_iters)
        return x, post_x

    def logpdf(self, x):
        """
        Returns the unnormalized log-posterior pdf at x.

        Parameters
        ----------
        x : np.array

        Returns
        -------
        float
        """
        if not self._within_bounds(x):
            return -np.inf
        return self._unnormalized_loglikelihood(x) + self._logprior_density(x)

    def pdf(self, x):
        """
        Returns the unnormalized posterior pdf at x.

        Parameters
        ----------
        x : np.array

        Returns
        -------
        float
        """
        return np.exp(self.logpdf(x))

    def grad_logpdf(self, x):
        """
        Returns the gradient of the unnormalized log-posterior pdf at x.

        Parameters
        ----------
        x : np.array

        Returns
        -------
        np.array
        """
        grad = self._grad_unnormalized_loglikelihood(x) + self._grad_logprior_density(x)
        return grad[0]

    def __getitem__(self, idx):
        return tuple([[v]*len(idx) for v in self.MAP])

    def _unnormalized_loglikelihood(self, x):
        mean, var = self.model.predict(x)
        if mean is None or var is None:
            raise ValueError("Unable to evaluate model at %s" % (x))
        return sp.stats.norm.logcdf(self.threshold, mean, np.sqrt(var))

    def _grad_unnormalized_loglikelihood(self, x):
        mean, var = self.model.predict(x)
        if mean is None or var is None:
            raise ValueError("Unable to evaluate model at %s" % (x))
        std = np.sqrt(var)

        grad_mean, grad_var = self.model.predictive_gradients(x)
        grad_mean = grad_mean[:, :, 0]  # assume 1D output

        factor = -grad_mean * std - (self.threshold - mean) * 0.5 * grad_var / std
        factor = factor / var
        term = (self.threshold - mean) / std
        pdf = sp.stats.norm.pdf(term)
        cdf = sp.stats.norm.cdf(term)

        return factor * pdf / cdf

    def _unnormalized_likelihood(self, x):
        return np.exp(self._unnormalized_loglikelihood(x))

    def _neg_unnormalized_loglikelihood(self, x):
        return -1 * self._unnormalized_loglikelihood(x)

    def _neg_unnormalized_logposterior(self, x):
        return -1 * self.logpdf(x)

    def _logprior_density(self, x):
        logprior_density = 0.0
        for xv, prior in zip(x, self.priors):
            if prior is not None:
                logprior_density += prior.logpdf(xv)
        return logprior_density

    def _within_bounds(self, x):
        x = x.reshape((-1, self.model.input_dim))
        for ii in range(self.model.input_dim):
            if np.any(x[:, ii] < self.model.bounds[ii][0]) or np.any(x[:, ii] > self.model.bounds[ii][1]):
                return False
        return True

    def _grad_logprior_density(self, x):
        grad_logprior_density = np.zeros(x.shape)
        for ii, prior in enumerate(self.priors):
            if prior is not None:
                grad_logprior_density[ii] = prior.grad_logpdf(x[ii])
        return grad_logprior_density

    def _prior_density(self, x):
        return np.exp(self._logprior_density(x))

    def _neg_logprior_density(self, x):
        return -1 * self._logprior_density(x)

    def plot(self):
        if len(self.model.bounds) == 1:
            mn = self.model.bounds[0][0]
            mx = self.model.bounds[0][1]
            dx = (mx - mn) / 200.0
            x = np.arange(mn, mx, dx)
            pd = np.zeros(len(x))
            for i in range(len(x)):
                pd[i] = self.pdf([x[i]])
            plt.figure()
            plt.plot(x, pd)
            plt.xlim(mn, mx)
            plt.ylim(0.0, max(pd)*1.05)
            plt.show()

        elif len(self.model.bounds) == 2:
            x, y = np.meshgrid(np.linspace(*self.model.bounds[0]), np.linspace(*self.model.bounds[1]))
            z = (np.vectorize(lambda a,b: self.pdf(np.array([a, b]))))(x, y)
            plt.contour(x, y, z)
            plt.show()

        else:
            raise NotImplementedError("Currently not supported for dim > 2")
