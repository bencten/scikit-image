import numpy as np

from ..._shared.testing import assert_equal, assert_almost_equal
from ..profile import profile_line


image = np.arange(100).reshape((10, 10)).astype(np.float)


def test_horizontal_rightward():
    prof = profile_line(image, (0, 2), (0, 8), order=0)
    expected_prof = np.arange(2, 9)
    assert_equal(prof, expected_prof)


def test_horizontal_leftward():
    prof = profile_line(image, (0, 8), (0, 2), order=0)
    expected_prof = np.arange(8, 1, -1)
    assert_equal(prof, expected_prof)


def test_vertical_downward():
    prof = profile_line(image, (2, 5), (8, 5), order=0)
    expected_prof = np.arange(25, 95, 10)
    assert_equal(prof, expected_prof)


def test_vertical_upward():
    prof = profile_line(image, (8, 5), (2, 5), order=0)
    expected_prof = np.arange(85, 15, -10)
    assert_equal(prof, expected_prof)


def test_45deg_right_downward():
    prof = profile_line(image, (2, 2), (8, 8), order=0)
    expected_prof = np.array([22, 33, 33, 44, 55, 55, 66, 77, 77, 88])
    # repeats are due to aliasing using nearest neighbor interpolation.
    # to see this, imagine a diagonal line with markers every unit of
    # length traversing a checkerboard pattern of squares also of unit
    # length. Because the line is diagonal, sometimes more than one
    # marker will fall on the same checkerboard box.
    assert_almost_equal(prof, expected_prof)


def test_45deg_right_downward_interpolated():
    prof = profile_line(image, (2, 2), (8, 8), order=1)
    expected_prof = np.linspace(22, 88, 10)
    assert_almost_equal(prof, expected_prof)


def test_45deg_right_upward():
    prof = profile_line(image, (8, 2), (2, 8), order=1)
    expected_prof = np.arange(82, 27, -6)
    assert_almost_equal(prof, expected_prof)


def test_45deg_left_upward():
    prof = profile_line(image, (8, 8), (2, 2), order=1)
    expected_prof = np.arange(88, 21, -22. / 3)
    assert_almost_equal(prof, expected_prof)


def test_45deg_left_downward():
    prof = profile_line(image, (2, 8), (8, 2), order=1)
    expected_prof = np.arange(28, 83, 6)
    assert_almost_equal(prof, expected_prof)


def test_pythagorean_triangle_right_downward():
    prof = profile_line(image, (1, 1), (7, 9), order=0)
    expected_prof = np.array([11, 22, 23, 33, 34, 45, 56, 57, 67, 68, 79])
    assert_equal(prof, expected_prof)


def test_pythagorean_triangle_right_downward_interpolated():
    prof = profile_line(image, (1, 1), (7, 9), order=1)
    expected_prof = np.linspace(11, 79, 11)
    assert_almost_equal(prof, expected_prof)


pyth_image = np.zeros((6, 7), np.float)
line = ((1, 2, 2, 3, 3, 4), (1, 2, 3, 3, 4, 5))
below = ((2, 2, 3, 4, 4, 5), (0, 1, 2, 3, 4, 4))
above = ((0, 1, 1, 2, 3, 3), (2, 2, 3, 4, 5, 6))
pyth_image[line] = 1.8
pyth_image[below] = 0.6
pyth_image[above] = 0.6


def test_pythagorean_triangle_right_downward_linewidth():
    prof = profile_line(pyth_image, (1, 1), (4, 5), linewidth=3, order=0)
    expected_prof = np.ones(6)
    assert_almost_equal(prof, expected_prof)


def test_pythagorean_triangle_right_upward_linewidth():
    prof = profile_line(pyth_image[::-1, :], (4, 1), (1, 5),
                        linewidth=3, order=0)
    expected_prof = np.ones(6)
    assert_almost_equal(prof, expected_prof)


def test_pythagorean_triangle_transpose_left_down_linewidth():
    prof = profile_line(pyth_image.T[:, ::-1], (1, 4), (5, 1),
                        linewidth=3, order=0)
    expected_prof = np.ones(6)
    assert_almost_equal(prof, expected_prof)


def test_reduce_func_mean():
    prof = profile_line(pyth_image, (0, 1), (3, 1), linewidth=3, order=0,
                        reduce_func=np.mean)
    expected_prof = np.array([0, 0.8, 1, 0.2])
    assert_almost_equal(prof, expected_prof)


def test_reduce_func_max():
    prof = profile_line(pyth_image, (0, 1), (3, 1), linewidth=3, order=0,
                        reduce_func=np.max)
    expected_prof = np.array([0, 1.8, 1.8, 0.6])
    assert_almost_equal(prof, expected_prof)


def test_reduce_func_sum():
    prof = profile_line(pyth_image, (0, 1), (3, 1), linewidth=3, order=0,
                        reduce_func=np.sum)
    expected_prof = np.array([0, 2.4, 3, 0.6])
    assert_almost_equal(prof, expected_prof)


def test_reduce_func_mean_linewidth_1():
    prof = profile_line(pyth_image, (0, 1), (3, 1), linewidth=1, order=0,
                        reduce_func=np.mean)
    expected_prof = np.array([0, 1.8, 0.6, 0.])
    assert_almost_equal(prof, expected_prof)


def test_reduce_func_None_linewidth_1():
    prof = profile_line(pyth_image, (1, 2), (4, 2),
                        linewidth=1, order=0, reduce_func=None)
    expected_prof = np.array([[0.6], [1.8], [0.6], [0.]])
    assert_almost_equal(prof, expected_prof)


def test_reduce_func_None_linewidth_3():
    prof = profile_line(pyth_image, (1, 2), (4, 2),
                        linewidth=3, order=0, reduce_func=None)
    expected_prof = np.array([[1.8, 0.6, 0.6],
                              [0.6, 1.8, 1.8],
                              [0., 0.6, 1.8],
                              [0., 0., 0.6]])
    assert_almost_equal(prof, expected_prof)


def test_reduce_func_lambda_linewidth_3():
    prof = profile_line(pyth_image, (1, 2), (4, 2), linewidth=3, order=0,
                        reduce_func=lambda x: x + x**2)
    expected_prof = np.array([[5.04, 0.96, 0.96],
                              [0.96, 5.04, 5.04],
                              [0., 0.96, 5.04],
                              [0., 0., 0.96]])
    # The lambda function acts on each pixel value individually.
    assert_almost_equal(prof, expected_prof)


def test_reduce_func_sqrt_linewidth_3():
    prof = profile_line(pyth_image, (1, 2), (4, 2),
                        linewidth=3, order=0, reduce_func=lambda x: x**0.5)
    expected_prof = np.array([[1.34164079, 0.77459667, 0.77459667],
                              [0.77459667, 1.34164079, 1.34164079],
                              [0., 0.77459667, 1.34164079],
                              [0., 0., 0.77459667]])
    assert_almost_equal(prof, expected_prof)


def test_reduce_func_sumofsqrt_linewidth_3():
    prof = profile_line(pyth_image, (1, 2), (4, 2), linewidth=3, order=0,
                        reduce_func=lambda x: np.sum(x**0.5))
    expected_prof = np.array([2.89083412, 3.45787824, 2.11623746, 0.77459667])
    assert_almost_equal(prof, expected_prof)


def test_bool_array_input():

    shape = (200, 200)
    center_x, center_y = (140, 150)
    radius = 20
    x, y = np.meshgrid(range(shape[1]), range(shape[0]))
    mask = (y - center_y) ** 2 + (x - center_x) ** 2 < radius ** 2
    src = (center_y, center_x)
    phi = 4 * np.pi / 9.
    dy = 31 * np.cos(phi)
    dx = 31 * np.sin(phi)
    dst = (center_y + dy, center_x + dx)

    profile_u8 = profile_line(mask.astype(np.uint8), src, dst)
    assert all(profile_u8[:radius] == 1)

    profile_b = profile_line(mask, src, dst)
    assert all(profile_b[:radius] == 1)

    assert all(profile_b == profile_u8)
