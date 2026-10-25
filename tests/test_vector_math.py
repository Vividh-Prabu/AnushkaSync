
from src.vector_math import (
    dot_product,
    vector_norm,
    cosine_similarity,
    angle_between,
    are_orthogonal,
)


def test_dot_product():
    assert dot_product([1, 2], [3, 4]) == 11


def test_vector_norm():
    assert vector_norm([3, 4]) == 5


def test_cosine_similarity():
    assert abs(cosine_similarity([1, 0], [1, 0]) - 1.0) < 1e-9


def test_angle_between():
    assert abs(angle_between([1, 0], [0, 1]) - 90.0) < 1e-9


def test_are_orthogonal():
    assert are_orthogonal([1, 0], [0, 1])
