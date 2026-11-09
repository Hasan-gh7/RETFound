"""Compatibility imports. Inference belongs exclusively to the RETFound API.

The former ONNX and synthetic prediction engines are no longer used.
"""
from .retfound_client import Connection, RETFoundClient, ServiceError, adapt_prediction

__all__ = ["Connection", "RETFoundClient", "ServiceError", "adapt_prediction"]
