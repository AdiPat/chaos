"""
Chaos: A minimal, AI-based entropy analyzer for Python developers.
Provides tools for analyzing text data entropy and gaining entropy-based insights.
"""

from .version import Version
from .chaos_encoder import ChaosEncoder, EncodingModel
from .algorithms import Algorithms
from .models import EntropyResult, EntropyResponse, AlgorithmType
from typing import List, Union, Optional
import numpy as np


class Order:
    def __init__(self) -> None:
        """Initialize the Order instance."""
        self.encoder = ChaosEncoder()
        self.algorithms = Algorithms()
        # Store valid algorithm types for validation
        self._valid_algorithms = {
            AlgorithmType.SHANNON,
            AlgorithmType.APPROXIMATE,
            AlgorithmType.SAMPLE,
            AlgorithmType.PERMUTATION,
        }

    def _get_algorithm_function(self, algorithm: AlgorithmType):
        """Get the corresponding algorithm function with parameters.

        Args:
            algorithm: Algorithm type to get the function for

        Returns:
            Callable: Algorithm function with parameters set
        """
        algorithm_map = {
            AlgorithmType.SHANNON: self.algorithms.shannon_entropy,
            AlgorithmType.APPROXIMATE: lambda x: self.algorithms.approximate_entropy(
                x, m=2, r=0.2 * float(x.std())
            ),
            AlgorithmType.SAMPLE: lambda x: self.algorithms.sample_entropy(
                x, m=2, r=0.2 * float(x.std())
            ),
            AlgorithmType.PERMUTATION: self.algorithms.permutation_entropy,
        }
        return algorithm_map.get(algorithm)

    def _calculate_entropy(
        self, data: np.ndarray, encoding: str, algorithm: AlgorithmType
    ) -> EntropyResult:
        """Calculate entropy for given data using specified encoding and algorithm.

        Args:
            data: Encoded data
            encoding: Name of the encoding used
            algorithm: Algorithm to calculate entropy

        Returns:
            EntropyResult: Result containing encoding, algorithm and entropy value
        """
        algo_func = self._get_algorithm_function(algorithm)
        if algo_func is None:
            raise ValueError(f"Unsupported algorithm type: {algorithm}")

        try:
            entropy = algo_func(data)
            if not np.isfinite(entropy):
                raise ValueError("Calculated entropy is not finite")

            return EntropyResult(
                encoding=encoding, algorithm=algorithm.value, entropy=float(entropy)
            )
        except Exception as e:
            raise ValueError(f"Error calculating entropy with {algorithm}: {str(e)}")

    def get_stats(
        self,
        data: str,
        encodings: Optional[List[EncodingModel]] = None,
        algorithms: Optional[List[AlgorithmType]] = None,
        json_response: bool = False,
    ) -> Union[EntropyResponse, List[EntropyResult]]:
        """Get entropy analysis report for the given text data.

        Args:
            data: Input text data to analyze
            encodings: List of encoding models to use (default: all)
            algorithms: List of algorithms to use (default: all)
            json_response: Whether to return response as JSON

        Returns:
            Union[EntropyResponse, List[EntropyResult]]: Entropy analysis results
        """
        # Input validation
        if not data or not isinstance(data, str):
            raise ValueError("Input data must be a non-empty string")

        if encodings is None:
            encodings = [EncodingModel.FREQUENCY]
        else:
            # Check for duplicates
            encoding_set = set(encodings)
            if len(encoding_set) != len(encodings):
                raise ValueError("Duplicate encoding models detected")
            # Validate encoding models
            invalid_encodings = [
                e for e in encodings if not isinstance(e, EncodingModel)
            ]
            if invalid_encodings:
                raise ValueError(f"Invalid encoding models: {invalid_encodings}")

        if algorithms is None:
            algorithms = list(self._valid_algorithms)
        else:
            # Check for duplicates
            algo_set = set(algorithms)
            if len(algo_set) != len(algorithms):
                raise ValueError("Duplicate algorithms detected")
            # Validate algorithms
            invalid_algos = [a for a in algorithms if a not in self._valid_algorithms]
            if invalid_algos:
                raise ValueError(f"Unsupported algorithm types: {invalid_algos}")

        results = []
        for encoding_model in encodings:
            try:
                encoded_data = self.encoder.encode(data, encoding_model)
                if encoded_data is None or len(encoded_data) == 0:
                    raise ValueError(f"Encoding failed for model {encoding_model}")

                for algorithm in algorithms:
                    result = self._calculate_entropy(
                        encoded_data, encoding_model.value, algorithm
                    )
                    results.append(result)
            except Exception as e:
                raise ValueError(
                    f"Error processing encoding {encoding_model}: {str(e)}"
                )

        if not results:
            raise ValueError("No entropy results were calculated")

        response = EntropyResponse(results=results)
        if json_response:
            return {
                "results": [
                    {
                        "encoding": r.encoding,
                        "algorithm": r.algorithm,
                        "entropy": r.entropy,
                    }
                    for r in response.results
                ]
            }
        return response.results

    def version(self) -> str:
        """Get the current version of Chaos.

        Returns:
            str: Current version string of the Chaos package
        """
        return Version.CURRENT_VERSION
