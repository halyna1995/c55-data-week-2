"""Tests for the pure transform functions (chapter Task 5).

Write at least 4 tests:
  - test_remove_invalid_drops_empty_names
  - test_clean_fields_normalizes_names
  - test_calculate_revenue_adds_fields
  - test_no_mutation
"""

from src.transforms import (
    calculate_revenue,
    clean_fields,
    filter_zero_quantity,
    remove_invalid,
)


def test_remove_invalid_drops_empty_names():
    """Feed in rows with empty product_name; assert they're dropped."""
    data = [
        {"product_name": "Laptop", "price": 999.99},
        {"product_name": "", "price": 50.0},
        {"product_name": "  ", "price": 25.0},
    ]
    result = remove_invalid(data)
    assert len(result) == 1
    assert result[0]['product_name'] == 'Laptop'


def test_clean_fields_normalizes_names():
    """Feed a row with messy product_name and uppercase email; assert
    the output has stripped + title-cased name and lowercase email.
    """
    data = [
        {
            "product_name": "  laptop ",
            "customer_email": "  Halyna@gmail.COM  ",
            "category": "",
        }
    ]
    result = clean_fields(data)
    assert result[0]["product_name"] == "Laptop"
    assert result[0]["customer_email"] == "halyna@gmail.com"
    assert result[0]["category"] == "Unknown"


def test_calculate_revenue_adds_fields():
    """Feed a row with price=100, quantity=3; assert output has
    revenue=300.0 and vat=63.0 (default VAT rate is 0.21).
    """
    data = [
        {"product_name": "Laptop", "price": 100, "quantity": 3}
    ]
    result = calculate_revenue(data)
    assert result[0]['revenue'] == 300.0
    assert result[0]['vat'] == 63.0


def test_no_mutation():
    """Feed in a list, run any transform on it, assert the original
    list is unchanged. This is the most important test in the file.
    """
    original = [
        {
            "product_name": "  laptop",
            "customer_email": "  Halyna@gmail.COM  ",
            "category": "",
        }
    ]
    expected = original.copy()
    remove_invalid(original)
    assert original == expected

def test_filter_zero_quantity():
    """Feed in rows with zero quantity; assert they're dropped."""
    data = [
        {"product_name": "Laptop", "quantity": 2},
        {"product_name": "Mouse", "quantity": 0},
    ]

    result = filter_zero_quantity(data)

    assert len(result) == 1
    assert result[0]["product_name"] == "Laptop"