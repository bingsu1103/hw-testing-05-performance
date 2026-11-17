import importlib.util
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "analyze_jtl.py"
SPEC = importlib.util.spec_from_file_location("analyze_jtl", MODULE_PATH)
assert SPEC and SPEC.loader
analyze_jtl = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(analyze_jtl)


class AnalyzeJtlTests(unittest.TestCase):
    def write_jtl(self, rows: list[str]) -> Path:
        directory = Path(tempfile.mkdtemp())
        path = directory / "result.jtl"
        path.write_text(
            "timeStamp,elapsed,label,responseCode,success\n" + "\n".join(rows) + "\n",
            encoding="utf-8",
        )
        return path

    def test_percentile_uses_nearest_rank(self):
        self.assertEqual(analyze_jtl.percentile(list(range(1, 101)), 95), 95)

    def test_calculates_metrics_and_groups(self):
        path = self.write_jtl(
            [
                "1000,100,Login,200,true",
                "1100,200,Login,500,false",
                "1200,300,Products,200,true",
                "1300,400,Products,200,true",
            ]
        )
        overall, labels = analyze_jtl.analyze(path)
        self.assertEqual(overall.samples, 4)
        self.assertEqual(overall.errors, 1)
        self.assertEqual(overall.error_rate_pct, 25.0)
        self.assertEqual(overall.p95_ms, 400)
        self.assertEqual(set(labels), {"Login", "Products"})

    def test_rejects_missing_columns(self):
        directory = Path(tempfile.mkdtemp())
        path = directory / "invalid.jtl"
        path.write_text("elapsed,label\n10,Login\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Missing JTL columns"):
            analyze_jtl.analyze(path)

    def test_gate_returns_failure(self):
        path = self.write_jtl(["1000,900,Login,200,true"])
        self.assertEqual(analyze_jtl.main([str(path), "--max-p95-ms", "500"]), 1)


if __name__ == "__main__":
    unittest.main()

