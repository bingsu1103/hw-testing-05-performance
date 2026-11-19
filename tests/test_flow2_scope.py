import csv
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLANS = sorted((ROOT / "test-plans").glob("23120205_*_20261117.jmx"))

EXPECTED_CSV_HEADER = [
    "name_prefix",
    "password",
    "search",
    "product_id",
    "product_name",
    "product_price",
    "quantity",
    "total_amount",
    "coupon_code",
    "expected_final_amount",
    "shipping_address",
]

EXPECTED_FLOW = [
    ("01 Auth - Register", "/api/register"),
    ("02 Auth - Login", "/api/login"),
    ("03 Read - Search Products", "/api/products"),
    ("04 Read - Product Detail", "/api/products/${product_id}"),
    ("05 Transaction - Add to Cart", "/api/cart"),
    ("06 Transaction - Apply Coupon", "/api/apply-coupon"),
    ("07 Transaction - Checkout", "/api/checkout"),
    ("08 Transaction - Record Coupon Usage", "/api/coupon-usage"),
]


def sampler_flow(plan: Path):
    root = ET.parse(plan).getroot()
    flow = []
    for sampler in root.iter("HTTPSamplerProxy"):
        path = sampler.find("./stringProp[@name='HTTPSampler.path']")
        flow.append((sampler.attrib["testname"], path.text if path is not None else None))
    return flow


class Flow2ScopeTests(unittest.TestCase):
    def test_csv_schema_matches_flow2_inputs(self):
        with (ROOT / "data" / "users.csv").open(newline="", encoding="utf-8") as handle:
            header = next(csv.reader(handle))
        self.assertEqual(header, EXPECTED_CSV_HEADER)

    def test_all_four_plans_use_exact_flow2_sequence(self):
        self.assertEqual(len(PLANS), 4)
        for plan in PLANS:
            with self.subTest(plan=plan.name):
                self.assertEqual(sampler_flow(plan), EXPECTED_FLOW)

    def test_plans_extract_and_reuse_flow2_state(self):
        for plan in PLANS:
            text = plan.read_text(encoding="utf-8")
            with self.subTest(plan=plan.name):
                for value in (
                    "flow_email",
                    "user_id",
                    "auth_token",
                    "coupon_id",
                    "final_amount",
                    "order_id",
                    "${final_amount}",
                ):
                    self.assertIn(value, text)


if __name__ == "__main__":
    unittest.main()
