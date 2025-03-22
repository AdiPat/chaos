"""
A sophisticated text encoding module that provides various encoding algorithms for text data.
This module implements different encoding strategies optimized for entropy analysis.
"""

from enum import Enum
import numpy as np
from .models import EncodingModel


class ChaosEncoder:
    """A sophisticated text encoding class with various encoding strategies."""

    def __init__(self) -> None:
        """Initialize the ChaosEncoder."""
        pass

    def encode(self, text: str, model: EncodingModel) -> np.ndarray:
        """Encode text using the specified encoding model.

        Args:
            text: Input text to encode
            model: Encoding model to use from EncodingModel enum

        Returns:
            np.ndarray: Encoded text as a 1D numpy array

        Raises:
            ValueError: If an invalid encoding model is specified
        """
        encoding_methods = {
            EncodingModel.ORDINAL: self._ordinal_encode,
            EncodingModel.ONE_HOT: self._one_hot_encode,
            EncodingModel.FREQUENCY: self._frequency_encode,
            EncodingModel.BINARY: self._binary_encode,
        }

        if model not in encoding_methods:
            raise ValueError(f"Unsupported encoding model: {model}")

        return encoding_methods[model](text)

    def _ordinal_encode(self, text: str) -> np.ndarray:
        """Encode text using ordinal encoding (character to number mapping).

        Args:
            text: Input text to encode

        Returns:
            np.ndarray: Ordinal encoded array
        """
        return np.array([ord(c) for c in text], dtype=np.int32)

    def _one_hot_encode(self, text: str) -> np.ndarray:
        """Encode text using one-hot encoding.

        Args:
            text: Input text to encode

        Returns:
            np.ndarray: Flattened one-hot encoded array
        """
        unique_chars = sorted(list(set(text)))
        char_to_idx = {c: i for i, c in enumerate(unique_chars)}

        encoded = np.zeros((len(text), len(unique_chars)))
        for i, char in enumerate(text):
            encoded[i, char_to_idx[char]] = 1

        return encoded.flatten()

    def _frequency_encode(self, text: str) -> np.ndarray:
        """Encode text using frequency-based encoding.

        Args:
            text: Input text to encode

        Returns:
            np.ndarray: Frequency encoded array
        """
        char_freq = {}
        for char in text:
            char_freq[char] = char_freq.get(char, 0) + 1

        total_chars = len(text)
        return np.array([char_freq[c] / total_chars for c in text])

    def _binary_encode(self, text: str) -> np.ndarray:
        """Encode text using binary encoding (ASCII to binary).

        Args:
            text: Input text to encode

        Returns:
            np.ndarray: Binary encoded array
        """
        binary_list = []
        for char in text:
            binary = format(ord(char), "08b")
            binary_list.extend([int(b) for b in binary])
        return np.array(binary_list, dtype=np.int8)
