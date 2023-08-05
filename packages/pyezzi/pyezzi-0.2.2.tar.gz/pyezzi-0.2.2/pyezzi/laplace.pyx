import numpy as np
cimport numpy as np
cimport cython

DTYPE = np.float64
ctypedef np.float64_t DTYPE_FLOAT
ctypedef np.int_t DTYPE_INT

# dirty fix to get rid of annoying warnings
np.seterr(divide='ignore', invalid='ignore')

@cython.boundscheck(False)
@cython.wraparound(False)
def solve_3D(np.ndarray wall,
             np.ndarray[DTYPE_FLOAT, ndim=3] init,
             float tolerance=0.0,
             int max_iterations=100,
             np.ndarray[DTYPE_FLOAT, ndim=1] spacing=np.array([1.0, 1.0, 1.0])):
    """
    Solve Laplacian in 3 dimensions

    :param wall:
    :param init:
    :param tolerance:
    :param max_iterations:
    :param spacing:
    :return:
    """
    cdef np.ndarray[DTYPE_FLOAT, ndim=3] laplace_grid = np.copy(init)
    cdef np.ndarray[DTYPE_FLOAT, ndim=3] prev_laplace_grid = np.copy(
        laplace_grid)
    cdef int iteration = 0
    cdef DTYPE_FLOAT max_error = 1.0
    cdef np.ndarray[DTYPE_INT, ndim=2] wall_idx = np.argwhere(wall)
    cdef np.ndarray[DTYPE_INT, ndim=1] wall_idx_i = wall_idx[:, 0]
    cdef np.ndarray[DTYPE_INT, ndim=1] wall_idx_j = wall_idx[:, 1]
    cdef np.ndarray[DTYPE_INT, ndim=1] wall_idx_k = wall_idx[:, 2]
    cdef int n_points = len(wall_idx)
    cdef DTYPE_INT i, j, k, n
    cdef DTYPE_FLOAT error
    cdef DTYPE_FLOAT value
    cdef DTYPE_FLOAT hi, hj, hk, hi2, hj2, hk2, factor

    hi, hj, hk = spacing
    hi2, hj2, hk2 = spacing ** 2

    factor = (hi2 * hj2 * hk2) / (2 * (hi2 * hj2 + hi2 * hk2 + hj2 * hk2))

    while max_error > tolerance and iteration < max_iterations:
        iteration += 1
        prev_laplace_grid = np.copy(laplace_grid)
        for n in range(n_points):
            i = wall_idx_i[n]
            j = wall_idx_j[n]
            k = wall_idx_k[n]
            value = \
                (
                    (laplace_grid[i + 1, j, k] +
                     laplace_grid[i - 1, j, k]) / hi2 +
                    (laplace_grid[i, j + 1, k] +
                     laplace_grid[i, j - 1, k]) / hj2 +
                    (laplace_grid[i, j, k - 1] +
                     laplace_grid[i, j, k + 1]) / hk2
                ) * factor
            laplace_grid[i, j, k] = value
        max_error = np.nanmax(
            np.abs(
                (prev_laplace_grid[wall_idx_i, wall_idx_j, wall_idx_k] -
                 laplace_grid[wall_idx_i, wall_idx_j, wall_idx_k]) /
                prev_laplace_grid[wall_idx_i, wall_idx_j, wall_idx_k]))
    return laplace_grid, iteration, max_error
