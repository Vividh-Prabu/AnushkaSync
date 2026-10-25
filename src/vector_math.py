
import numpy as np


def dot_product(a, b):
    """Calculate the dot product of two vectors."""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)

    if a.shape != b.shape:
        raise ValueError("Vectors must have the same dimensions.")

    return float(np.dot(a, b))


def vector_norm(a):
    """Calculate the length of a vector."""
    return float(np.linalg.norm(a))


def cosine_similarity(a, b):
    """Calculate cosine similarity between two vectors."""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)

    if a.shape != b.shape:
        raise ValueError("Vectors must have the same dimensions.")

    norm_a = vector_norm(a)
    norm_b = vector_norm(b)

    if norm_a == 0 or norm_b == 0:
        raise ValueError("Cannot compare a zero vector.")

    score = dot_product(a, b) / (norm_a * norm_b)
    return float(np.clip(score, -1.0, 1.0))


def angle_between(a, b):
    """Calculate the angle between vectors in degrees."""
    score = cosine_similarity(a, b)
    return float(np.degrees(np.arccos(score)))


def are_orthogonal(a, b):
    """Check whether the dot product is zero."""
    return bool(np.isclose(dot_product(a, b), 0.0, atol=1e-10))
