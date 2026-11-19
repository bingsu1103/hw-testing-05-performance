## Environment

- SUT commit: `85af3ba875c88283615e22cb108f13e2fccaf0e9`
- Backend: Node.js/Express + SQLite on macOS, Apple M2, 8 GB RAM
- Flow: Register → Login → Search → Product detail → Add to cart → Apply coupon
- Reproduced: 2026-11-19 ICT

## Observed behavior

Applying the seeded `SAVE10` coupon to an order total of `30,000,000` returns a negative discount and increases the final amount to `300,000,000`.

```text
Coupon seed: SAVE10, type=percent, discount_value=10
Original total: 30000000
Expected 10% discount: 3000000
Expected final amount: 27000000
Actual discount_amount: -270000000
Actual final_amount: 300000000
```

## Expected behavior

`SAVE10` should reduce the order total by 10%, producing a discount of `3,000,000` and final amount of `27,000,000`.

## Reproduction

1. Register a new user and log in.
2. Search for `iPhone`, open product ID 1, and add it to the cart.
3. Call `POST /api/apply-coupon` with `code=SAVE10`, `total_amount=30000000`, and the registered user ID.
4. Inspect `discount_amount` and `final_amount` in the response.

## Probable cause

The seeded percentage is stored as integer `10`, while the calculation treats it as fraction `0.10` and evaluates `total_amount * (1 - discount_value)`.

## Impact

Customers using a valid percentage coupon see a dramatically inflated checkout total. This is a functional regression in the assigned search-and-coupon workflow and can also corrupt performance-test transactions if `SAVE10` is used as load data.

## Data-safety check

- [x] No email, password, JWT, address, serial number, or UUID is attached.
- [x] The behavior was reproduced from a clean database with a newly registered test user.
