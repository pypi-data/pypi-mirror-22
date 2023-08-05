from __future__ import division, unicode_literals, print_function

import numpy as np
cimport numpy as np

ctypedef fused ntype:
    np.uint8_t
    np.uint16_t
    np.uint32_t
    np.uint64_t
    np.int8_t
    np.int16_t
    np.int32_t
    np.int64_t
    np.float32_t
    np.float64_t

cpdef relative_extrema(np.ndarray[ntype, ndim=1] data, int order, int cmp):
    cdef Py_ssize_t width = data.shape[0], x = 0, i = 0
    cdef int lower, upper
    cdef ntype curex = 0, value = 0

    cpdef np.ndarray[np.int_t, ndim=1] result = np.empty(width, dtype=np.int)

    cdef Py_ssize_t result_len = 0
    cdef int changed = 0

    for x in range(width):
        curex = data[x]
        lower = < int > x - order
        if lower < 0:
            lower = 0

        upper = < int > x + order
        if upper > width:
            upper = width

        changed = 0

        for i in range(lower, upper):
            value = data[i]

            if value != curex:
                changed = 1
                if (cmp == -1 and curex > value) or (cmp == 1 and curex < value):
                    curex = value
                    break

        if curex == data[x] and changed == 1:
            result[result_len] = x
            result_len += 1

    return result[:result_len]


#def relative_maxima(data, order=1):
#    return relative_extrema(data, order=order, cmp=1)

#def relative_minima(data, order=1):
#    return relative_extrema(data, order=order, cmp=-1)