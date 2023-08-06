import scipy as sp
import scipy.fftpack as fftp
import scipy.linalg as la
from scipy import pi, sin, cos
from scipy.optimize import newton_krylov, anderson, broyden1, broyden2,\
                           excitingmixing, linearmixing, diagbroyden
# import matplotlib.pyplot as plt

"""__all__ = ["hb_so",
           "harmonic_deriv",
           "solmf",
           "duff_osc"]
"""
# print('kwargs not being sent to optimizer')


def hb_so(sdfunc, x0, omega=1, method='newton_krylov', num_harmonics=1,
          params={}, **kwargs):
    r"""Harmonic balance solver for second order ODEs.

    Obtains the solution of a second order differential equation under the
    presumption that the solution is harmonic.

    Returns t (time), x (displacement), v (velocity), and a (acceleration)
    response of a second order linear ordinary differential
    equation defined by
    :math:`\ddot{\mathbf{x}}=f(\mathbf{x},\mathbf{v},\omega)`.

    Parameters
    ----------
    sdfunc: function
        Name of function that returns **column vector** second derivative
        given omega and \*\*kwargs. This is NOT a string.

        :math:`\ddot{\mathbf{x}}=f(\mathbf{x},\mathbf{v},\omega)`
    omega:  float
        assumed fundamental response frequency in radians per second.
    num_harmonics: int
        number of harmonics to presume. omega = 0 constant term is always
        presumed to exist. Minimum (and default) is 1.
    x0: array_like
        n x m array where n is the number of equations and m is the number of
        values representing the repeating solution.
        It is required that :math:`m = 1 + 2 num_{harmonics}`. (we will
        generalize allowable default values later.)
    method: str
        Name of optimization method to be used.
    params: dict
        Dictionary of parameters needed by sdfunc.
    other: any
        Other keyword arguments available to nonlinear solvers in
        `scipy.optimize.nonlin
        <https://docs.scipy.org/doc/scipy/reference/optimize.nonlin.html>`_.
        See Notes.

    Returns
    -------
    t, x, e, amps, phases: array_like
        time, displacement history (time steps along columns), errors,
    amps : float array
        amplitudes of displacement (primary harmonic) in column vector format.
    phases : float array
        amplitudes of displacement (primary harmonic) in column vector format.

    Examples
    --------
    >>> import mousai as ms
    >>> t, x, e, amps, phases = ms.hb_so(ms.duff_osc, sp.array([[0,1,-1]]), .7)

    Notes
    ------
    Calls a linear algebra function from
    `scipy.optimize.nonlin
    <https://docs.scipy.org/doc/scipy/reference/optimize.nonlin.html>`_ with
    ``newton_krylov`` as the default.

    Needs quasi-linear estimator for starting point.

    Should gently "walk" solution up to get to nonlinearities.

    Algorithm:
        1. calls `hb_so_err` with x as the variable to solve for.
        2. `hb_so_err` uses a Fourier representation of x to obtain velocities
           (after an inverse fft) then calls `sdfunc` to determine
           accelerations.
        3. Accelerations are also obtained using a Fourier representation of x
        4. Error in the accelerations are the functional error used by the
           nonlinear algebraic solver (default ``newton_krylov``) to be
           minimized by the solver.

    Options to the nonlinear solvers can be passed in by \*\*kwargs.
    """

    if isinstance(sdfunc, str):
        sdfunc = globals()[sdfunc]
        print("`sdfunc` is expected to be a function name, not a string")
    params['function'] = sdfunc  # function that returns SO derivative
    time = sp.linspace(0, 2*pi/omega, num=2*num_harmonics+1, endpoint=False)
    params['time'] = time
    params['omega'] = omega
    params['n_har'] = num_harmonics

    def hb_so_err(x):
        """Array (vector) of hamonic balance second order algebraic errors.

        Given a set of second order equations
        :math:`\ddot{x} = f(x, \dot{x}, \omega, t)`
        calculate the error :math:`E = \ddot{x} - f(x, \dot{x}, \omega, t)`
        presuming that :math:`x` can be represented as a Fourier series, and
        thus :math:`\dot{x}` and :math:`\ddot{x}` can be obtained from the
        Fourier series representation of :math:`x`.

        Parameters
        ----------
        x : array_like
            x is an :math:`n \\times m` by 1 array of presumed displacements.
            It must be a "list" array (not a linear algebra vector). Here
            :math:`n` is the number of displacements and :math:`m` is the
            number of times per cycle at which the displacement is guessed
            (minimum of 3)

        **kwargs : string, float, variable
            **kwargs is a packed set of keyword arguments with 3 required
            arguments.
                1. `function`: a string name of the function which returned
                the numerically calculated acceleration.

                2. `omega`: which is the defined fundamental harmonic
                at which the is desired.

                3. `n_har`: an integer representing the number of harmonics.
                Note that `m` above is equal to 1 + 2 * `n_har`.

        Returns
        -------
        e : array_like
            2d array of numerical error of presumed solution(s) `x`.

        Notes
        -----
        `function` and `omega` are not separately defined arguments so as to
        enable algebraic solver functions to call `hb_so_err` cleanly.

        The algorithm is as follows:
            1. The velocity and accelerations are calculated in the same shape
               as `x` as `vel` and `accel`.
            3. Each column of `x` and `v` are sent with `t`, `omega`, and other
               `**kwargs** to `function` one at a time with the results
               agregated into the columns of `accel_num`.
            4. The difference between `accel_num` and `accel` is reshaped to be
               :math:`n \\times m` by 1 and returned as the vector error used
               by the numerical algebraic equation solver.
        """
        nonlocal params  # Will stay out of global/conflicts
        n_har = params['n_har']
        omega = params['omega']
        # function = params['function']
        time = params['time']
        m = 1 + 2 * n_har
        # print(x)
        vel = harmonic_deriv(omega, x)
        # print(vel)

        accel = harmonic_deriv(omega, vel)
        accel_from_deriv = sp.zeros_like(accel)

        # Should subtract in place below to save memory for large problems
        for i in sp.arange(m):
            t = time[i]  # This should enable t to be used for current time in
            params['cur_time'] = time[i]  # loops
            # Note that everything in params can be accessed within `function`.
#            accel_from_deriv[:, i] = globals()[function](x[:, i], vel[:, i],
#                                                         params)"""
            # print(params['function'])
            accel_from_deriv[:, i] = params['function'](x[:, i], vel[:, i],
                                                        params)

        e = accel_from_deriv - accel
        return e
    try:
        x = globals()[method](hb_so_err, x0, **kwargs)
    except:
        raise
    # v = harmonic_deriv(omega, x)
    # a = harmonic_deriv(omega, v)
    xhar = fftp.fft(x)*2/len(time)
    amps = sp.absolute(xhar[:, 1])
    phases = sp.angle(xhar[:, 1])
    e = hb_so_err(x)

    '''
    a) define a function that returns errors in time domain as vector
    b) define function to obtain velocity and accelerations from displacement
    and frequencies.
    c)
    '''
    return time, x, e, amps, phases


def harmonic_deriv(omega, r):
    """Derivative of a harmonic function using frequency methods.

    Returns the derivatives of a harmonic function

    Parameters
    ----------
    omega: float
        Fundamendal frequency, in rad/sec, of repeating signal
    r: array_like
        | Array of rows of time histories to take the derivative of.
        | The 1 axis (each row) corresponds to a time history.
        | The length of the time histories *must be an odd integer*.

    Returns
    -------
    s: array_like
        Function derivatives.
        The 1 axis (each row) corresponds to a time history.

    Notes
    -----
    At this time, the length of the time histories *must be an odd integer*.

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> from mousai import *
    >>> import scipy as sp
    >>> from scipy import pi,sin,cos
    >>> f = 2
    >>> omega = 2.*pi * f
    >>> numsteps = 11
    >>> t = sp.arange(0,1/omega*2*pi,1/omega*2*pi/numsteps)
    >>> x = sp.array([sin(omega*t)])
    >>> v = sp.array([omega*cos(omega*t)])
    >>> states = sp.append(x,v,axis = 0)
    >>> state_derives = harmonic_deriv(omega,states)
    >>> plt.plot(t,states.T,t,state_derives.T,'x')
    [<matplotlib.line...]
    """
    # print(r)
    n = r.shape[1]
    omega_half = -sp.arange((n-1)/2+1) * omega * 2j/(n-2)
    omega_whole = sp.append(sp.conj(omega_half[-1:0:-1]), omega_half)
    r_freq = fftp.fft(r)
    s_freq = r_freq * omega_whole
    s = fftp.ifft(s_freq)
    return sp.real(s)


def solmf(x, v, M, C, K, F):
    """Acceleration of second order linear matrix system.

    Parameters
    ----------
    x, v, F : array_like
        :math:`n\\times 1` arrays of current displacement, velocity, and Force.
    M, C, K : array_like
        Mass, damping, and stiffness matrices.

    Returns
    -------
    a : array_like
        :math:`n\\times 1` acceleration vector

    Examples
    --------
    >>> import scipy as sp
    >>> M = sp.array([[2,0],[0,1]])
    >>> K = sp.array([[2,-1],[-1,3]])
    >>> C = 0.01 * M + 0.01 * K
    >>> x = sp.array([[1],[0]])
    >>> v = sp.array([[0],[10]])
    >>> F = v * 0.1
    >>> a = solmf(x, v, M, C, K, F)
    >>> print(a)
        [[-0.95]
         [ 1.6 ]]
    """

    return -la.solve(M, C @ v + K @ x - F)


def duff_osc(x, v, params):
    # print('duff osc')
    # print(reduced_kwargs)
    omega = params['omega']
    t = params['cur_time']
    '''print('t=',t)
    print('x = ', x)
    print('v = ', v)'''
    return -x-.1*x**3-.2*v+sin(omega*t)

'''
if __name__ == "__main__":
    """Run doctests.

    python (name of this file)  -v
    will test all of the examples in the help.

    Leaving off -v will run the tests without any output. Success will return
    nothing.

    See the doctest section of the python manual.
    https://docs.python.org/3.5/library/doctest.html
    """

    # import mousai as ms

    # doctest.run_docstring_examples(frfest,globals(),optionflags=doctest.ELLIPSIS)
    # doctest.run_docstring_examples(asd,globals(),optionflags=doctest.ELLIPSIS)
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS |
                    doctest.NORMALIZE_WHITESPACE)
'''
