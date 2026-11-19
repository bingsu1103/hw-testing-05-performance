# Flow 2 Scope Correction Design

## Intent

Correct HW05 so every measured JMeter scenario represents the assigned Flow 2, “Tìm kiếm + Mã giảm giá”, instead of the earlier generic purchase example.

## Binding workflow

`Register → Login → Search Products → Product Detail → Add to Cart → Apply Coupon → Checkout`

The web client also records coupon usage after checkout. That call is treated as part of the Checkout step because it is issued by the same user action and is required to preserve coupon state.

## Goals

- Use the same Flow 2 sequence in Load, Stress, Spike, and Soak plans.
- Generate a unique registered account for every virtual-user iteration so registration remains repeatable.
- Use CSV data for password, product, coupon, expected discounted total, and shipping address.
- Apply the valid fixed-value `BIGBUY` coupon during measured runs and assert its returned final amount.
- Re-run all measured evidence and rebuild the report from Flow 2 raw JTL files only.
- Preserve the supplied flow-assignment screenshot as coordination evidence.
- Reproduce and report any genuine coupon defect separately from the measured workload.

## Non-goals

- Do not modify the SUT to make its behavior pass.
- Do not produce or alter AI prompts, AI analysis, AI Critique, or AI Audit Report.
- Do not claim the assignment table itself contains the student's name; the supplied screenshot shows the available flows but its “Người chọn” cells are blank.
- Do not reuse Flow 1 JTL metrics as Flow 2 evidence.

## Constraints

- Required plan names remain `23120205_{Load,Stress,Spike}_20261117.jmx`; the Soak plan remains supporting evidence.
- Load, Stress, and Spike retain distinct JMeter listener types.
- Real JTL, HTML report, and resource evidence must be regenerated from a clean tracked SUT database.
- Previous public issues remain in GitHub history, but the main Flow 2 report references only defects reproduced in the selected flow.

## Approaches considered

1. Patch the existing login-first plans by inserting registration and coupon requests. Rejected because the old CSV identity and assertions would leave hidden Flow 1 assumptions.
2. Rebuild the workflow contract and update all four plans against it. Selected because one explicit sequence can be validated automatically and prevents future scope drift.
3. Modify the SUT to merge coupon application into checkout. Rejected because homework tests must observe, not repair, the assigned SUT.

## Data and assertions

CSV columns: `name_prefix,password,search,product_id,product_name,product_price,quantity,total_amount,coupon_code,expected_final_amount,shipping_address`.

JMeter creates `flow_email` from a run identifier, thread number, and loop iteration. Registration extracts `user_id`; login extracts `auth_token`; coupon application extracts `coupon_id` and `final_amount`. Assertions require HTTP success, a JWT, coupon success, the expected discounted total, and an order ID.

## Evidence replacement

Tracked Flow 1 JTLs, HTML reports, analyses, rendered summaries, and run metadata will be removed from the primary evidence paths before Flow 2 execution. They remain recoverable from Git history. The final report and package must contain only the newly measured Flow 2 evidence.
