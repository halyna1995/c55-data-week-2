"""Pure transform functions over a list of dicts.

Tasks (see chapter Task 3):
  Build at least these four pure, composable transforms. Each MUST:
    - take a list of dicts and return a NEW list (never mutate the input)
    - be free of I/O (no file reads, no prints)
    - be testable with hand-rolled data (see tests/test_transforms.py)

Each function must return a new list of new dicts, not mutate the input
rows in place. The chapter (Functional Composition) shows the canonical
pattern; the auto-grader checks that you used it inside the function
bodies, not just in prose.
"""


def remove_invalid(rows: list[dict]) -> list[dict]:
    """Remove rows with empty product_name OR negative price.

    Empty here means missing, "", or whitespace-only.
    """
    
    result = []
    for row in rows:
        product_name = str(row.get("product_name") or "").strip()
        price = float(row.get("price", 0))

        if product_name == "" or price < 0:
            continue

        result.append({**row})

    return result

def clean_fields(rows: list[dict]) -> list[dict]:
    """Clean string fields:

    - product_name: strip + title-case
    - customer_email: strip + lowercase
    - category: default to "Unknown" if missing or empty

    Return a new list. Do not mutate the input rows.
    """
    
    result = []
    for row in rows:
        product_name = str(row.get("product_name") or "").strip().title()
        customer_email = str(row.get("customer_email") or "").strip().lower()
        raw_category = str(row.get("category") or "").strip()
        category = raw_category if raw_category else "Unknown"

        result.append(
            {
                **row,
                "product_name": product_name,
                "customer_email": customer_email,
                "category": category,
            }
        )

    return result

def calculate_revenue(rows: list[dict], vat_rate: float = 0.21) -> list[dict]:
    """Add 'revenue' (price * quantity) and 'vat' (revenue * vat_rate) fields.

    Round both to 2 decimal places. Coerce price/quantity from string if needed.
    """
    
    result = []
    for row in rows:
        price = float(row["price"])
        quantity = int(row["quantity"])
        revenue = round(price * quantity, 2)
        vat = round(revenue * vat_rate, 2)

        result.append(
            {
                **row,
                "price": price,
                "quantity": quantity,
                "revenue": revenue,
                "vat": vat,
            }
        )

    return result


def filter_zero_quantity(rows: list[dict]) -> list[dict]:
    """Remove rows where quantity is 0."""
    
    result = []
    for row in rows:
        if int(row.get("quantity", 0)) == 0:
            continue

        result.append({**row})

    return result