# AI Debug Report — Task 2

While building Task 1 (the Cleaner Pipeline), you will encounter at least one bug. (If not, introduce one intentionally — pick the most surprising thing about Python you noticed this week and break it.)

Use an LLM (ChatGPT, Claude, etc.) to help you debug it, then fill in the four sections below. The goal is not "the AI fixed it"; the goal is showing you understood what was broken, what the AI suggested, and whether you accepted or pushed back.

Aim for 100-200 words per section. Bullet points are fine.

## The Error

What went wrong? Paste the traceback or the wrong-output sample. Include the file and the line you were running when it broke.

While implementing the transform functions for Task 1, I ran the test suite with:

```bash
pytest tests/

Several tests failed. The first problem was in remove_invalid():

AttributeError: 'float' object has no attribute 'strip'

The failing line was:

price_str = row.get("price", "").strip()

The test passed price as a number:

{"product_name": "Laptop", "price": 999.99}

but my function expected price to be a string, like it is when read from a CSV file.

A similar error happened in calculate_revenue():

AttributeError: 'int' object has no attribute 'strip'

The failing line was:

price = float(calculated_row.get("price", "0").strip())

Here the test passed price as an integer:

{"product_name": "Laptop", "price": 100, "quantity": 3}

but my code again assumed that every value was a string.

One more test failed for filter_zero_quantity():

AssertionError: assert 2 == 1
 +  where 2 = len([{'product_name': 'Product A', 'quantity': '2', 'transaction_id': '1'}, {'product_name': 'Product C', 'quantity': '-1', 'transaction_id': '3'}])

My function removed rows where quantity == 0, but the test also expected rows with negative quantity, for example quantity == -1, to be removed.

## The Prompt

What did you ask the AI? Paste the actual prompt verbatim. (Include the code or stack trace you pasted alongside it; do NOT include any real `.env` values, API keys, or PII — replace those with `<REDACTED>`.)

I asked AI to help debug the failing pytest output. I pasted the error messages and the relevant parts of my transform functions.

My prompt was approximately:

pytest tests/ fails with these errors:

AttributeError: 'float' object has no attribute 'strip'
in remove_invalid()

AttributeError: 'int' object has no attribute 'strip'
in calculate_revenue()

Also test_filter_zero_quantity expects only one row, but my function returns two rows.

Here is my code:

def remove_invalid(rows):
    result = []
    for row in rows:
        product_name = row.get("product_name", "").strip()
        price_str = row.get("price", "").strip()
        price = float(price_str)

        if product_name == "":
            continue

        if price < 0:
            continue

        result.append(row.copy())

    return result


def calculate_revenue(rows, vat_rate=0.21):
    result = []
    for row in rows:
        calculated_row = row.copy()

        price = float(calculated_row.get("price", "0").strip())
        quantity = int(calculated_row.get("quantity", "0").strip())

        revenue = price * quantity
        vat = revenue * vat_rate

        calculated_row["revenue"] = round(revenue, 2)
        calculated_row["vat"] = round(vat, 2)

        result.append(calculated_row)

    return result


def filter_zero_quantity(rows):
    result = []
    for row in rows:
        quantity = int(row.get("quantity", "0"))

        if quantity == 0:
            continue

        result.append(row.copy())

    return result

How should I fix this while keeping the transform functions pure?

## The Solution

What did the AI suggest? Did it work on the first try? Did you have to follow up? Paste the final code change (a small diff is best).

The AI explained that values coming from csv.DictReader are strings, but values in unit tests may already be int or float. Therefore, calling .strip() directly on a value is unsafe unless the value is definitely a string.

The fix was to convert values to strings before calling .strip():

price = float(str(row.get("price", "0")).strip())
quantity = int(str(row.get("quantity", "0")).strip())

So instead of this:

row.get("price", "").strip()

I changed the code to this:

str(row.get("price", "0")).strip()

I also updated filter_zero_quantity() to remove rows where quantity is zero or negative:

if quantity <= 0:
    continue

This made the behavior stricter and matched the test expectation.

After applying these fixes, I ran:

pytest tests/

and the transform tests passed.

## Reflection

Did you understand *why* the original code was broken before the AI told you? If not, what was the gap in your mental model? If you understood it before asking, why did you still ask the AI — speed, second opinion, or something else?

I understood the bug.

The main issue was an incorrect assumption about input types. In the real pipeline, CSV data is read with csv.DictReader, so all values initially arrive as strings. But unit tests often use Python-native values such as int and float. A pure transform function should be robust enough to handle both cases.

The .strip() method belongs to strings only. Therefore, this is unsafe:

value.strip()

if value might be an int or float.

This is safer:

str(value).strip()

because it normalizes the value before parsing it.

 The assignment explicitly mentioned removing zero quantity, but the provided test also expected negative quantity to be removed. That makes sense because a sales transaction should not have a negative quantity. So I changed the logic from checking only quantity == 0 to checking quantity <= 0.
