"""Tests for the pure transform functions (chapter Task 5).

Write at least 4 tests:
  - test_remove_invalid_drops_empty_names
  - test_clean_fields_normalizes_names
  - test_calculate_revenue_adds_fields
  - test_no_mutation
"""
from copy import deepcopy

from src.transforms import (
    calculate_revenue,
    clean_fields,
    filter_zero_quantity,
    remove_invalid,
)

 
def test_no_mutation():
    """Run all transforms and assert the original list is unchanged."""
    original = [
        {
            "transaction_id": "1",
            "product_name": "  laptop  ",
            "category": "",
            "price": "100",
            "quantity": "2",
            "customer_email": "  Halyna@gmail.COM  ",
            "date": "2025-01-15",
        },
        {
            "transaction_id": "2",
            "product_name": "Mouse",
            "category": "Accessories",
            "price": "25",
            "quantity": "0",
            "customer_email": "test@example.com",
            "date": "2025-01-16",
        },
    ]

    transforms = [
        remove_invalid,
        clean_fields,
        filter_zero_quantity,
        calculate_revenue,
    ]

    for transform in transforms:
        rows = deepcopy(original)
        expected = deepcopy(rows)

        transform(rows)

        assert rows == expected
