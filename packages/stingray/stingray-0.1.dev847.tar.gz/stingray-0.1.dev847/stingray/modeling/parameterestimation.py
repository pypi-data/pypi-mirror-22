
__all__ = ["OptimizationResults", "ParameterEstimation", "PSDParEst",
           "SamplingResults"]


# check whether matplotlib is installed for easy plotting
try:
    import matplotlib.pyplot as plt
    from matplotlib.ticker import MaxNLocator
    can_plot = True
except ImportError:
    can_plot = False


# check whether emcee is installed for sampling
try:
    import emcee
    can_sample = True
except ImportError:
    can_sample = False

try:
    import corner
    use_corner = True
except ImportError:
    use_corner = False

import numpy as np
import scipy
import scipy.optimize
import scipy.stats
import scipy.signal
import copy

try:
    from statsmodels.tools.numdiff import approx_hess
    comp_hessian = True
except ImportError:
    comp_hessian = False

from stingray.modeling.posterior import Posterior, PSDPosterior, LogLikelihood
from astropy.modeling.fitting import _fitter_to_model_params


class OptimizationResults(object):

    def __init__(self, lpost, res, neg=True):
        """
        Helper class that will contain the results of the regression.
        Less fiddly than a dictionary.

        Parameters
        ----------
        lpost: instance of Posterior or one of its subclasses
            The object containing the function that is being optimized
            in the regression


        res: instance of scipy's OptimizeResult class
            The object containing the results from a optimization run

        """
        self.neg = neg
        self.result = res.fun
        self.p_opt = res.x
        self.model = lpost.model

        self._compute_covariance(lpost, res)
        self._compute_model(lpost)
        self._compute_criteria(lpost)
        self._compute_statistics(lpost)

    def _compute_covariance(self, lpost, res):

        if hasattr(res, "hess_inv"):
            if not isinstance(res.hess_inv, np.ndarray):
                self.cov = np.asarray(res.hess_inv.todense())
            else:
                self.cov = res.hess_inv

            self.err = np.sqrt(np.diag(self.cov))
        else:
            if comp_hessian:
                # calculate Hessian approximating with finite differences
                print("Approximating Hessian with finite differences ...")

                phess = approx_hess(self.p_opt, lpost)

                self.cov = np.linalg.inv(phess)
                self.err = np.sqrt(np.diag(np.abs(self.cov)))

            else:
                self.cov = None
                self.err = None

    def _compute_model(self, lpost):

        _fitter_to_model_params(lpost.model, self.p_opt)

        self.mfit = lpost.model(lpost.x)

    def _compute_criteria(self, lpost):

        if isinstance(lpost, Posterior):
            self.deviance = -2.0*lpost.loglikelihood(self.p_opt, neg=False)
        elif isinstance(lpost, LogLikelihood):
            self.deviance = 2.0*self.result

        # Akaike Information Criterion
        self.aic = self.result+2.0*self.p_opt.shape[0]

        # Bayesian Information Criterion
        self.bic = self.result + self.p_opt.shape[0]*np.log(lpost.x.shape[0])

        # Deviance Information Criterion
        # TODO: Add Deviance Information Criterion

    def _compute_statistics(self, lpost):
        try:
            self.mfit
        except AttributeError:
            self._compute_model(lpost)

        self.merit = np.sum(((lpost.y-self.mfit)/self.mfit)**2.0)
        self.dof = lpost.y.shape[0] - float(self.p_opt.shape[0])
        self.sexp = 2.0*len(lpost.x)*len(self.p_opt)
        self.ssd = np.sqrt(2.0*self.sexp)
        self.sobs = np.sum(lpost.y-self.mfit)

    def print_summary(self, lpost):

        print("The best-fit model parameters plus errors are:")

        fixed = [lpost.model.fixed[n] for n in lpost.model.param_names]
        parnames = [n for n, f in zip(lpost.model.param_names, fixed) \
                    if f is False]

        for i, (x, y, p) in enumerate(zip(self.p_opt, self.err, parnames)):
            print("%i) Parameter %s: %f.5 +/- %f.5f"%(i, p, x, y))

        print("\n")

        print("Fitting statistics: ")
        print(" -- number of data points: %i"%(len(lpost.x)))

        try:
            self.deviance
        except AttributeError:
            self._compute_criteria(lpost)

        print(" -- Deviance [-2 log L] D = %f.3"%self.deviance)
        print(" -- The Akaike Information Criterion of the model is: " +
              str(self.aic) + ".")

        print(" -- The Bayesian Information Criterion of the model is: " +
              str(self.bic) + ".")

        try:
            self.merit
        except AttributeError:
            self._compute_statistics(lpost)

        print(" -- The figure-of-merit function for this model " +
              " is: %f.5f"%self.merit +
              " and the fit for %i dof is %f.3f"%(self.dof,
                                                  self.merit/self.dof))

        print(" -- Summed Residuals S = %f.5f"%self.sobs)
        print(" -- Expected S ~ %f.5 +/- %f.5"%(self.sexp, self.ssd))
        print(" -- merit function (SSE) M = %f.5f \n\n"%self.merit)

        return


class ParameterEstimation(object):

    def __init__(self, fitmethod='BFGS', max_post=True):
        """
        Parameter estimation of two-dimensional data, either via
        optimization or MCMC.
        Note: optimization with bounds is not supported. If something like
        this is required, define (uniform) priors in the ParametricModel
        instances to be used below.

        Parameters:
        -----------
        fitmethod: string, optional, default "L-BFGS-B"
            Any of the strings allowed in scipy.optimize.minimize in
            the method keyword. Sets the fit method to be used.

        max_post: bool, optional, default True
            If True, then compute the Maximum-A-Posteriori estimate. If False,
            compute a Maximum Likelihood estimate.
        """

        self.fitmethod = fitmethod

        self.max_post = max_post

    def fit(self, lpost, t0, neg=True, scipy_optimize_options=None):
        """
        Do either a Maximum A Posteriori or Maximum Likelihood
        fit to the data.

        Parameters:
        -----------
        lpost: Posterior (or subclass) instance
            and instance of class Posterior or one of its subclasses
            that defines the function to be minized (either in loglikelihood
            or logposterior)

        t0 : {list | numpy.ndarray}
            List/array with set of initial parameters

        neg : bool, optional, default True
            Boolean to be passed to `lpost`, setting whether to use the
            *negative* posterior or the *negative* log-likelihood. Since
            `Posterior` and `LogLikelihood` objects are generally defined in

        scipy_optimize_options : dict, optional, default None
            A dictionary with options for `scipy.optimize.minimize`,
            directly passed on as keyword arguments.

        Returns:
        --------
        fitparams: dict
            A dictionary with the fit results
            TODO: Add description of keywords in the class!
        """

        if not isinstance(lpost, Posterior) and not isinstance(lpost,
                                                               LogLikelihood):
            raise TypeError("lpost must be a subclass of "
                            "Posterior or LogLikelihoood.")

        if not len(t0) == lpost.npar:
            raise ValueError("Parameter set t0 must be of right "
                             "length for model in lpost.")

        if scipy.__version__ < "0.10.0":
            args = [neg]
        else:
            args = (neg,)

        if not scipy_optimize_options:
            scipy_optimize_options = {}

        # different commands for different fitting methods,
        # at least until scipy 0.11 is out
        funcval = 100.0
        i = 0
        while funcval == 100 or funcval == 200 or \
                funcval == 0.0 or not np.isfinite(funcval):

            if i > 20:
                raise Exception("Fitting unsuccessful!")
            # perturb parameters slightly
            t0_p = np.random.multivariate_normal(t0, np.diag(np.abs(t0)/100.))

            # if max_post is True, do the Maximum-A-Posteriori Fit
            if self.max_post:
                opt = scipy.optimize.minimize(lpost, t0_p,
                                              method=self.fitmethod,
                                              args=args, tol=1.e-10,
                                              **scipy_optimize_options)

            # if max_post is False, then do a Maximum Likelihood Fit
            else:
                if isinstance(lpost, Posterior):
                    # This could be a `Posterior` object
                    opt = scipy.optimize.minimize(lpost.loglikelihood, t0_p,
                                                  method=self.fitmethod,
                                                  args=args, tol=1.e-10,
                                                 **scipy_optimize_options)

                elif isinstance(lpost, LogLikelihood):
                    # Except this could be a `LogLikelihood object
                    # In which case, use the evaluate function
                    # if it's not either, give up and break!
                    opt = scipy.optimize.minimize(lpost.evaluate, t0_p,
                                                  method=self.fitmethod,
                                                  args=args, tol=1.e-10,
                                                  **scipy_optimize_options)
                else:
                    raise TypeError("lpost must be a Posterior or LogLikelihood"
                                    " object.")

            funcval = opt.fun
            i += 1

        res = OptimizationResults(lpost, opt, neg=neg)

        return res

    def compute_lrt(self, lpost1, t1, lpost2, t2, neg=True, max_post=False):
        """
        This function computes the Likelihood Ratio Test between two
        nested models.

        Parameters
        ----------
        lpost1 : object of a subclass of Posterior
            The posterior object for model 1

        t1 : iterable
            The starting parameters for model 1

        lpost2 : object of a subclass of Posterior
            The posterior object for model 2

        t2 : iterable
            The starting parameters for model 2

        neg : bool, optional, default True
            Boolean flag to decide whether to use the negative log-likelihood
            or log-posterior

        max_post: bool, optional, default False
            If True, set the internal state to do the optimization with the
            log-likelihood rather than the log-posterior.

        """

        self.max_post = max_post

        # fit data with both models
        res1 = self.fit(lpost1, t1, neg=neg)
        res2 = self.fit(lpost2, t2, neg=neg)

        # compute log likelihood ratio as difference between the deviances
        lrt = res1.deviance - res2.deviance

        return lrt

    def sample(self, lpost, t0, cov=None,
               nwalkers=500, niter=100, burnin=100, threads=1,
               print_results=True, plot=False, namestr="test"):
        """
        Sample the posterior distribution defined in `lpost` using MCMC.
        Here we use the `emcee` package, but other implementations could
        in principle be used.

        Parameters
        ----------
        t0 : iterable
            list or array containing the starting parameters. Its length
            must match `lpost.model.npar`.


        nwalkers : int
            The number of walkers (chains) to use during the MCMC procedure.
            The more walkers are used, the slower the estimation will be, but
            the better the final distribution is likely to be.

        niter : int
            The number of iterations to run the MCMC chains for. The larger this
            number, the longer the estimation will take, but the higher the
            chance that the walkers have actually converged on the true
            posterior distribution.

        burnin : int
            The number of iterations to run the walkers before convergence is
            assumed to have occurred. This part of the chain will be discarded
            before sampling from what is then assumed to be the posterior
            distribution desired.

        threads : int
            The number of threads for parallelization.
            Default is 1, i.e. no parallelization

        print_results : bool
            Boolean flag setting whether the results of the MCMC run should
            be printed to standard output. Default: True

        plot : bool
            Boolean flag setting whether summary plots of the MCMC chains
            should be produced. Default: False

        namestr : str
            Optional string for output file names for the plotting.

        Returns
        -------

        res : SamplingResults object

        """
        if not can_sample:
            raise ImportError("emcee not installed! Can't sample!")

        ndim = len(t0)

        if cov is None:
            # do a MAP fitting step to find good starting positions for
            # the sampler
            res = self.fit(lpost, t0, neg=True)
            cov = res.cov
        # sample random starting positions for each walker from
        # a multivariate Gaussian
        p0 = np.array([np.random.multivariate_normal(t0, cov) for
                       i in range(nwalkers)])

        # initialize the sampler
        sampler = emcee.EnsembleSampler(nwalkers, ndim, lpost, args=[False],
                                        threads=threads)

        # run the burn-in
        pos, prob, state = sampler.run_mcmc(p0, burnin)

        sampler.reset()

        # do the actual MCMC run
        _, _, _ = sampler.run_mcmc(pos, niter, rstate0=state)

        res = SamplingResults(sampler)

        if print_results:
            res.print_results()

        if plot:
            res.plot_results(namestr + "_corner.pdf")

        return res


class SamplingResults(object):

    def __init__(self, sampler, ci_min=0.05, ci_max=0.95):
        """
        Helper class that will contain the results of the sampling
        in a handly format.
        Less fiddly than a dictionary.

        Parameters
        ----------
        sampler: emcee.EnsembleSampler object
            The object containing the sampler that's done all the work.

        ci_min: float out of [0,1]
            The lower bound percentile for printing confidence intervals
            on the parameters

        ci_max: float out of [0,1]
            The upper bound percentile for printing confidence intervals
            on the parameters

        """

        # store all the samples
        self.samples = sampler.flatchain

        self.nwalkers = np.float(sampler.chain.shape[0])
        self.niter = np.float(sampler.iterations)

        # store number of dimensions
        self.ndim = sampler.dim

        # compute and store acceptance fraction
        self.acceptance = np.nanmean(sampler.acceptance_fraction)
        self.L = self.acceptance*self.samples.shape[0]

        self._check_convergence(sampler)
        self._infer(ci_min, ci_max)

    def _check_convergence(self, sampler):

        # compute and store autocorrelation time
        try:
            self.acor = sampler.acor
        except emcee.autocorr.AutocorrError:
            print("Chains too short to compute autocorrelation lengths.")

        self.rhat = self._compute_rhat(sampler)

    def _compute_rhat(self, sampler):

        # between-sequence variance
        mean_samples_iter = np.nanmean(sampler.chain, axis=1)

        # mean over the means over iterations: (self.ndim)
        mean_samples = np.nanmean(sampler.chain, axis=(0,1))

        # now compute between-sequence variance
        bb = (self.niter / (self.nwalkers - 1)) * np.sum((mean_samples_iter -
                                                          mean_samples)**2.,
                                                         axis=0)

        # compute variance of each chain
        var_samples = np.nanvar(sampler.chain, axis=1)

        # compute mean of variance
        ww = np.nanmean(var_samples, axis=0)

        # compute weighted average of ww and bb:
        rhat = ((self.niter - 1) / self.niter) * ww + (1 / self.niter) * bb

        return rhat

    def _infer(self, ci_min=0.05, ci_max=0.95):
        self.mean = np.mean(self.samples, axis=0)
        self.std = np.std(self.samples, axis=0)
        self.ci = np.percentile(self.samples, [ci_min, ci_max], axis=0)

    def print_results(self):
        """
        Print results of the MCMC run.

        """

        print("-- The acceptance fraction is: %f.5"%self.acceptance)
        try:
            print("-- The autocorrelation time is: %f.5"%self.acor)
        except AttributeError:
            pass
        print("R_hat for the parameters is: " + str(self.rhat))

        print("-- Posterior Summary of Parameters: \n")
        print("parameter \t mean \t\t sd \t\t 5% \t\t 95% \n")
        print("---------------------------------------------\n")
        for i in range(self.ndim):
            print("theta[" + str(i) + "] \t " +
                  str(self.mean[i]) + "\t" + str(self.std[i]) + "\t" +
                  str(self.ci[0, i]) + "\t" + str(self.ci[1, i]) + "\n")

    def plot_results(self, filename, nsamples=1000):
        """
        Plot some results in a triangle plot.
        If installed, will use `corner` for the plotting
        (available here https://github.com/dfm/corner.py or
        through pip), if not, uses its own code to make a triangle
        plot.

        Parameters
        ----------

        filename: str
            Name of the output file with the figure
        nsamples: int
            The maximum number of samples used for plotting.

        """
        assert can_plot, "Need to have matplotlib installed for plotting"
        if use_corner:
            corner.corner(self.samples, labels=None,
                          quantiles=[0.16, 0.5, 0.84],
                          show_titles=True, title_args={"fontsize": 12})

        else:
            fig = plt.figure(figsize=(15, 15))
            plt.subplots_adjust(top=0.925, bottom=0.025,
                                left=0.025, right=0.975,
                                wspace=0.2, hspace=0.2)

            ind_all = np.random.choice(np.arange(self.samples.shape[0]),
                                       size=nsamples)
            samples = self.samples[ind_all]
            for i in range(self.ndim):
                for j in range(self.ndim):
                    xmin, xmax = samples[:, j].min(), samples[:, j].max()
                    ymin, ymax = samples[:, i].min(), samples[:, i].max()
                    ax = fig.add_subplot(self.ndim, self.ndim, i*self.ndim+j+1)

                    ax.xaxis.set_major_locator(MaxNLocator(5))
                    ax.ticklabel_format(style="sci", scilimits=(-2, 2))

                    if i == j:
                        ntemp, binstemp, patchestemp = \
                            ax.hist(samples[:, i], 30, normed=True,
                                    histtype='stepfilled')
                        ax.axis([ymin, ymax, 0, max(ntemp)*1.2])

                    else:

                        ax.axis([xmin, xmax, ymin, ymax])

                        # make a scatter plot first
                        ax.scatter(samples[:, j], samples[:, i], s=7)
                        # then add contours
                        xmin, xmax = samples[:, j].min(), samples[:, j].max()
                        ymin, ymax = samples[:, i].min(), samples[:, i].max()

                        # Perform Kernel density estimate on data
                        try:
                            xx, yy = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
                            positions = np.vstack([xx.ravel(), yy.ravel()])
                            values = np.vstack([samples[:, j], samples[:, i]])
                            kernel = scipy.stats.gaussian_kde(values)
                            zz = np.reshape(kernel(positions).T, xx.shape)

                            ax.contour(xx, yy, zz, 7)
                        except ValueError:
                            print("Not making contours.")

        plt.savefig(filename, format='pdf')
        plt.close()
        return


class PSDParEst(ParameterEstimation):

    def __init__(self, ps, fitmethod='BFGS', max_post=True):

        self.ps = ps
        ParameterEstimation.__init__(self, fitmethod=fitmethod,
                                     max_post=max_post)

    def fit(self, lpost, t0, neg=True):

        self.lpost = lpost

        res = ParameterEstimation.fit(self, self.lpost, t0, neg=neg)

        res.maxpow, res.maxfreq, res.maxind = \
            self._compute_highest_outlier(self.lpost, res)

        return res

    def sample(self, lpost, t0, cov=None,
               nwalkers=500, niter=100, burnin=100, threads=1,
               print_results=True, plot=False, namestr="test"):

        self.lpost = lpost

        fit_res = ParameterEstimation.fit(self, self.lpost, t0, neg=True)

        res = ParameterEstimation.sample(self, self.lpost, fit_res.p_opt,
                                         cov=fit_res.cov,
                                         nwalkers=nwalkers,
                                         niter=niter, burnin=burnin,
                                         threads=threads,
                                         print_results=print_results, plot=plot,
                                         namestr=namestr)

        return res

    def _compute_highest_outlier(self, lpost, res, nmax=1):

        residuals = 2.0 * lpost.y/ res.mfit

        ratio_sort = copy.copy(residuals)
        ratio_sort.sort()
        max_y = ratio_sort[-nmax:]

        max_x = np.zeros(max_y.shape[0])
        max_ind = np.zeros(max_y.shape[0])

        for i, my in enumerate(max_y):
            max_x[i], max_ind[i] = self._find_outlier(lpost.x, residuals, my)

        return max_y, max_x, max_ind

    @staticmethod
    def _find_outlier(xdata, ratio, max_y):
        max_ind = np.where(ratio == max_y)[0][0]+1
        max_x = xdata[max_ind]

        return max_x, max_ind

    def plotfits(self, res1, res2=None, save_plot=False,
                 namestr='test', log=False):

        if not can_plot:
            print("No matplotlib imported. Can't plot!")
        else:
            # make a figure
            f = plt.figure(figsize=(12, 10))
            # adjust subplots such that the space between the top and bottom
            # of each are zero
            plt.subplots_adjust(hspace=0.0, wspace=0.4)

            # first subplot of the grid, twice as high as the other two
            # This is the periodogram with the two fitted models overplotted
            s1 = plt.subplot2grid((4, 1), (0, 0), rowspan=2)

            if log:
                logx = np.log10(self.ps.freq)
                logy = np.log10(self.ps.power)
                logpar1 = np.log10(res1.mfit)

                p1, = s1.plot(logx, logy, color='black', linestyle='steps-mid')
                p2, = s1.plot(logx, logpar1, color='blue', lw=2)
                s1.set_xlim([min(logx), max(logx)])
                s1.set_ylim([min(logy)-1.0, max(logy)+1])
                if self.ps.norm == "leahy":
                    s1.set_ylabel('log(Leahy-Normalized Power)', fontsize=18)
                elif self.ps.norm == "rms":
                    s1.set_ylabel('log(RMS-Normalized Power)', fontsize=18)
                else:
                    s1.set_ylabel("log(Power)", fontsize=18)

            else:
                p1, = s1.plot(self.ps.freq, self.ps.power,
                              color='black', linestyle='steps-mid')
                p2, = s1.plot(self.ps.freq, res1.mfit,
                              color='blue', lw=2)

                s1.set_xscale("log")
                s1.set_yscale("log")

                s1.set_xlim([min(self.ps.freq), max(self.ps.freq)])
                s1.set_ylim([min(self.ps.freq)/10.0,
                             max(self.ps.power)*10.0])

                if self.ps.norm == "leahy":
                    s1.set_ylabel('Leahy-Normalized Power', fontsize=18)
                elif self.ps.norm == "rms":
                    s1.set_ylabel('RMS-Normalized Power', fontsize=18)
                else:
                    s1.set_ylabel("Power", fontsize=18)

            if res2 is not None:
                if log:
                    logpar2 = np.log10(res2.mfit)
                    p3, = s1.plot(logx, logpar2, color='red', lw=2)
                else:
                    p3, = s1.plot(self.ps.freq, res2.mfit,
                                  color='red', lw=2)
                s1.legend([p1, p2, p3], ["data", "model 1 fit", "model 2 fit"])
            else:
                s1.legend([p1, p2], ["data", "model fit"])

            s1.set_title("Periodogram and fits for data set " + namestr,
                         fontsize=18)

            # second subplot: power/model for Power law and straight line
            s2 = plt.subplot2grid((4, 1), (2, 0), rowspan=1)
            pldif = self.ps.power / res1.mfit

            s2.set_ylabel("Residuals, \n first model",
                          fontsize=18)

            if log:
                s2.plot(logx, pldif, color='black', linestyle='steps-mid')
                s2.plot(logx, np.ones(self.ps.freq.shape[0]),
                        color='blue', lw=2)
                s2.set_xlim([min(logx), max(logx)])
                s2.set_ylim([min(pldif), max(pldif)])

            else:
                s2.plot(self.ps.freq, pldif, color='black',
                        linestyle='steps-mid')
                s2.plot(self.ps.power, np.ones(self.ps.power.shape[0]),
                        color='blue', lw=2)

                s2.set_xscale("log")
                s2.set_yscale("log")
                s2.set_xlim([min(self.ps.freq), max(self.ps.freq)])
                s2.set_ylim([min(pldif), max(pldif)])

            if res2 is not None:
                bpldif = self.ps.power/res2.mfit

            # third subplot: power/model for bent power law and straight line
                s3 = plt.subplot2grid((4, 1), (3, 0), rowspan=1)

                if log:
                    s3.plot(logx, bpldif, color='black', linestyle='steps-mid')
                    s3.plot(logx, np.ones(len(self.ps.freq)),
                            color='red', lw=2)
                    s3.axis([min(logx), max(logx), min(bpldif), max(bpldif)])
                    s3.set_xlabel("log(Frequency) [Hz]", fontsize=18)

                else:
                    s3.plot(self.ps.freq, bpldif,
                            color='black', linestyle='steps-mid')
                    s3.plot(self.ps.freq, np.ones(len(self.ps.freq)),
                            color='red', lw=2)
                    s3.set_xscale("log")
                    s3.set_yscale("log")
                    s3.set_xlim([min(self.ps.freq), max(self.ps.freq)])
                    s3.set_ylim([min(bpldif), max(bpldif)])
                    s3.set_xlabel("Frequency [Hz]", fontsize=18)

                s3.set_ylabel("Residuals, \n second model",
                              fontsize=18)

            else:
                if log:
                    s2.set_xlabel("log(Frequency) [Hz]", fontsize=18)
                else:
                    s2.set_xlabel("Frequency [Hz]", fontsize=18)

            ax = plt.gca()

            for label in ax.get_xticklabels() + ax.get_yticklabels():
                label.set_fontsize(14)

            # make sure xticks are taken from first plots, but don't
            # appear there
            plt.setp(s1.get_xticklabels(), visible=False)

            if save_plot:
                # save figure in png file and close plot device
                plt.savefig(namestr + '_ps_fit.png', format='png')

        return
