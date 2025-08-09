from typing import Dict, Any
import math

def attribute_sample_size(population: int, expected_exception_rate=0.05, precision=0.05, confidence=0.95) -> int:
    """
    Simple attribute sampling size using normal approximation for planning.
    Not a substitute for firm standards; tune parameters per policy.
    """
    # z for 95%
    z = 1.96 if abs(confidence - 0.95) < 1e-6 else 1.96
    p = expected_exception_rate
    q = 1 - p
    n0 = (z**2 * p * q) / (precision**2)
    # finite population correction
    n = (n0 / (1 + (n0 - 1)/max(population, 1)))
    return max(5, int(math.ceil(n)))

def stratify_by_thresholds(items, thresholds):
    """
    thresholds: list of (label, min_amount, max_amount)
    Returns dict label -> list(items)
    Each item should be dict-like with 'amount' field.
    """
    buckets = {label: [] for (label, *_rest) in thresholds}
    for it in items:
        amt = float(it.get("amount", 0))
        for label, lo, hi in thresholds:
            if (lo is None or amt >= lo) and (hi is None or amt < hi):
                buckets[label].append(it)
                break
    return buckets
