"""
A comprehensive toolkit for entropy analysis in Python, implementing different entropy estimation methods.
This module provides various algorithms for calculating different types of entropy measures.
"""

import numpy as np
from math import log2
from typing import Any, Sequence


class Algorithms:
    """A comprehensive toolkit for entropy analysis in Python."""

    def __init__(self) -> None:
        """Initialize the entropy analysis toolkit."""
        pass

    def shannon_entropy(self, data: Sequence[Any], base: int = 2) -> float:
        """Calculate Shannon entropy of input data.

        Args:
            data: Input sequence data to analyze
            base: Base for logarithm calculation, defaults to 2

        Returns:
            float: Calculated Shannon entropy value
        """
        _, counts = np.unique(data, return_counts=True)
        probabilities = counts / len(data)

        if base == 2:
            entropy = -sum(p * log2(p) for p in probabilities)
        else:
            entropy = -sum(p * np.log(p) / np.log(base) for p in probabilities)

        return entropy

    def approximate_entropy(self, time_series: np.ndarray, m: int, r: float) -> float:
        """Calculate Approximate Entropy (ApEn) for a time series.

        Args:
            time_series: Input time series data
            m: Embedding dimension
            r: Tolerance value (typically 0.2 * std of the time series)

        Returns:
            float: Calculated ApEn value
        """
        N = len(time_series)

        def _phi(m_val: int) -> float:
            """Calculate phi value for given m.

            Args:
                m_val: Embedding dimension value

            Returns:
                float: Calculated phi value
            """
            count = np.zeros(N - m_val + 1)

            for i in range(N - m_val + 1):
                template = time_series[i : i + m_val]
                for j in range(N - m_val + 1):
                    if max(abs(template - time_series[j : j + m_val])) < r:
                        count[i] += 1
            return np.sum(np.log(count / (N - m_val + 1))) / (N - m_val + 1)

        return abs(_phi(m) - _phi(m + 1))

    def sample_entropy(self, time_series: np.ndarray, m: int, r: float) -> float:
        """Calculate Sample Entropy (SampEn) for a time series.

        Args:
            time_series: Input time series data
            m: Embedding dimension
            r: Tolerance value (typically 0.2 * std of the time series)

        Returns:
            float: Calculated SampEn value
        """
        N = len(time_series)

        A = 0
        B = 0

        def create_vectors(dim: int) -> np.ndarray:
            """Create embedding vectors for given dimension.

            Args:
                dim: Embedding dimension

            Returns:
                np.ndarray: Array of embedding vectors
            """
            vectors = []
            for i in range(N - dim + 1):
                vectors.append(time_series[i : i + dim])
            return np.array(vectors)

        xm = create_vectors(m)
        xm1 = create_vectors(m + 1)

        for i in range(N - m):
            distances = np.max(np.abs(xm[i] - xm), axis=1)
            B += np.sum((distances < r) & (np.arange(len(distances)) != i))

        for i in range(N - m - 1):
            distances = np.max(np.abs(xm1[i] - xm1), axis=1)
            A += np.sum((distances < r) & (np.arange(len(distances)) != i))

        return -np.log(A / B) if B > 0 and A > 0 else np.inf

    def permutation_entropy(
        self, time_series: np.ndarray, order: int = 3, delay: int = 1
    ) -> float:
        """Calculate Permutation Entropy for a time series.

        Args:
            time_series: Input time series data
            order: Permutation order, defaults to 3
            delay: Time delay, defaults to 1

        Returns:
            float: Calculated permutation entropy value
        """
        n = len(time_series)
        permutation_counts = {}

        for i in range(n - delay * (order - 1)):
            pattern = time_series[i : i + delay * order : delay]
            sorted_idx = np.argsort(pattern)
            pattern_key = tuple(sorted_idx)

            if pattern_key in permutation_counts:
                permutation_counts[pattern_key] += 1
            else:
                permutation_counts[pattern_key] = 1

        total = sum(permutation_counts.values())
        probabilities = [count / total for count in permutation_counts.values()]

        return -sum(p * log2(p) for p in probabilities)

    def multiscale_entropy(
        self, time_series: np.ndarray, scale_range: int = 10, m: int = 2, r: float = 0.2
    ) -> np.ndarray:
        """Calculate Multiscale Entropy for a time series.

        Args:
            time_series: Input time series data
            scale_range: Maximum scale factor, defaults to 10
            m: Embedding dimension, defaults to 2
            r: Tolerance value, defaults to 0.2

        Returns:
            np.ndarray: Array of multiscale entropy values for each scale factor
        """
        r = r * np.std(time_series, ddof=1)
        mse = np.zeros(scale_range)

        for scale in range(1, scale_range + 1):
            coarse_grained = self._coarse_grain(time_series, scale)
            mse[scale - 1] = self.sample_entropy(coarse_grained, m, r)

        return mse

    def _coarse_grain(self, time_series: np.ndarray, scale: int) -> np.ndarray:
        """Perform coarse-graining on a time series.

        Args:
            time_series: Input time series data
            scale: Scale factor for coarse-graining

        Returns:
            np.ndarray: Coarse-grained time series
        """
        N = len(time_series)
        result = np.zeros(int(N / scale))

        for i in range(0, int(N / scale)):
            result[i] = np.mean(time_series[i * scale : (i + 1) * scale])

        return result
