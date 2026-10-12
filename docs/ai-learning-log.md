# AI Learning Log

## Fellow: <Alexander Ogwu>

### Interaction #1: Raising errors vs printing (check_title)

**Problem:** My `check_title` printed a message and returned nothing for a blank title.
**My initial understanding:** I thought printing the message was enough to reject blank input.
**Prompt to AI:** "How did I do?" (shared my `check_title` function).
**Useful AI guidance:** A function should either return a valid value or raise an error. Printing and returning `None` would let a ticket with no title be stored, and tests cannot easily check printed text.
**My independent experiment/test:** [e.g. called `check_title("   ")` before and after the fix and wrote down what happened]
**Verification source or result:** [FILL IN: test output, e.g. `assertRaises(ValueError)` passing for `""` and `"   "`]
**Decision:** Accepted. Changed `print` + `return` to `raise ValueError("Title cannot be blank")`.
**Related file/commit:** `campusflow/tickets.py`, `tests/test_tickets.py`, commit [FILL IN SHA]
**What I can now explain without AI:** [FILL IN: in your own words, why raising is safer than printing]

---

### Interaction #2: Logic bug with `or` and `!=` (check_urgency)

**Problem:** `check_urgency` rejected every input, including valid ones like "low".
**My initial understanding:** I wrote `if cleaned != "low" or cleaned != "medium" or cleaned != "high"` thinking it meant "not one of these three".
**Prompt to AI:** "How did I do with the third function?" (shared the code).
**Useful AI guidance:** With `or`, at least two of the three `!=` checks are always true, so the error always fires. It needs `and`, or a cleaner `not in` check against a list.
**My independent experiment/test:** [FILL IN: e.g. predicted the result for `"low"`, ran the old version, then the fixed version, and noted the difference]
**Verification source or result:** [FILL IN: test results for "low", "MEDIUM", "  High ", "urgent"]
**Decision:** Accepted and improved. Fixed with `and` (or `not in` an allowed list).
**Related file/commit:** `campusflow/tickets.py`, `tests/test_tickets.py`, commit [FILL IN SHA]
**What I can now explain without AI:** [FILL IN: in your own words, why "not A or not B or not C" is always true]

---

### Interaction #3: What `int()` accepts (check_affected_users)

**Problem:** Menu input arrives as text, so I needed to convert it safely to a whole number and reject bad values.
**My initial understanding:** I expected `int()` to reject anything that is not plain digits, and I did not know `True` counts as the number 1.
**Prompt to AI:** "Will this work for the fourth function?" (shared the code).
**Useful AI guidance:** Check `bool` before `int`, because `True` is an `int` in Python. `int("5.5")` and `int("abc")` raise `ValueError`. `int()` also accepts forms like `"+5"` and `"1_000"`.
**My independent experiment/test:** [FILL IN: run these in a Python shell, predict first: `int("5.5")`, `int("  7  ")`, `int("+5")`, `int("1_000")`, `isinstance(True, int)`]
**Verification source or result:** [FILL IN: what the shell printed, and/or Python docs link]
**Decision:** [FILL IN: accepted / improved. If you changed or rejected any AI advice after checking it, say exactly what and why. This is where your required "critical evaluation" entry goes.]
**Related file/commit:** `campusflow/tickets.py`, commit [FILL IN SHA]
**What I can now explain without AI:** [FILL IN: why the bool check must come before the int check]

---

### Interaction #4 (optional extra): Storage safety

**Problem:** [FILL IN: e.g. understanding `try/except` with `json.JSONDecodeError`, or why writing to a temp file then replacing it is safer]
**My initial understanding:** [FILL IN]
**Prompt to AI:** [FILL IN: your actual prompt]
**Useful AI guidance:** [FILL IN]
**My independent experiment/test:** [FILL IN]
**Verification source or result:** [FILL IN]
**Decision:** [FILL IN]
**Related file/commit:** `campusflow/storage.py`, `tests/test_storage.py`
**What I can now explain without AI:** [FILL IN]

---

## Fellow: <partner's name>

(Your partner completes their own section with at least three interactions, including one corrected, improved or rejected AI suggestion.)