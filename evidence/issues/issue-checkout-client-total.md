## Environment

- SUT commit: `85af3ba875c88283615e22cb108f13e2fccaf0e9`
- Backend: Node.js/Express + SQLite on macOS 26.6, Apple M2, 8 GB RAM
- Reproduced: 2026-11-17 15:47 ICT

## Observed behavior

The authenticated checkout endpoint persists the client-provided `total_amount` without recalculating the order total from the server-side cart.

## Expected behavior

FR-08 states that the backend must recalculate the total and must not trust `total_amount` supplied by the client.

## Reproduction

1. Start from the tracked clean `database.sqlite`.
2. Log in as the default test user.
3. Add product 1 to the cart with price `25,000,000` and quantity `1`.
4. Call `POST /api/checkout` with `total_amount: 1`.
5. Read the created order with `GET /api/orders/1`.

## Evidence

```text
Cart item price sent: 25000000
Checkout total_amount sent: 1
Checkout response: {"message":"Checkout successful","orderId":1}
Persisted order: {"id":1,"user_id":2,"total_amount":1,"status":"pending",...}
```

The request succeeds and the order is persisted with `total_amount=1`.

## Impact

A client can create an order with an arbitrary total that does not match the cart, breaking order integrity and potentially causing financial loss.

## Data-safety check

- [x] No password, JWT, personal address, serial number, or UUID is attached.
- [x] The behavior was reproduced from a clean database.

