import numpy as np
import numpy.typing as npt
import matplotlib.pyplot as plt
from typing import Callable, List


def f(x: npt.NDArray[np.floating], u: npt.NDArray[np.floating]) -> npt.NDArray[np.floating]:
    """
    A numerical evaluation of the plant with n number of states and o number of inputs.

    Parameters
    ----------
    x: npt.NDArray[np.floating]
    The current state vector of shape nx1

    u: npt.NDArray[np.floating]
    The current input vector of shape ox1

    Returns
    -------
    x_next: npt.NDArray[np.floating]
    Returning a state vector with the derivatives, to be used by an integrator.
    """

    x_dot = [x[1], u[0]]

    return np.array(x_dot)

class Simulator:
    def __init__(self, model: Callable, nx: int, nu: int, nsim: int, dt: float):
        self.model = model
        self.nx = nx
        self.nu = nu
        self.nsim = nsim
        self.dt = dt


    def evolve(self, pid_gains: List[float], x0: List[float], y_idx: int, ref: float):
        kp, ki, kd = pid_gains

        X = np.full([int(self.nsim / self.dt), self.nx], np.nan)
        X[0] = x0
        U = np.full([int(self.nsim / self.dt)-1, self.nu], np.nan)
        e = np.full([int(self.nsim / self.dt)-1, 1], np.nan)

        for k in range(int(self.nsim / self.dt)-1):
            e[k] = ref - X[k, y_idx]

            if k >= 2:
                a0 = kp + ki*self.dt + kd/self.dt
                a1 = -kp - 2 * (kd/self.dt)
                a2 = kd / self.dt

                U[k] = U[k-1] + a0 * e[k] + a1 * e[k-1] + a2 * e[k-2]
            else:
                U[k] = np.array([0.0])

            X[k+1] = self.RK4_step(X[k], U[k])

        return X, U, float(np.sum(e**2) / len(e)) + 10*float(np.sum(U**2) / len(U)) + 40 * np.max(U)

    def RK4_step(self, x: npt.NDArray[np.floating], u: npt.NDArray[np.floating]) -> npt.NDArray[np.floating]:
        k1 = self.model(x, u)
        k2 = self.model(x + k1 * self.dt / 2, u)
        k3 = self.model(x + k2 * self.dt / 2, u)
        k4 = self.model(x + k3 * self.dt,     u)

        return x + self.dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6
