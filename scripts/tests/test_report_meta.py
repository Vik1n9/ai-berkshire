#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""report_meta 的單元測試。

全部用內嵌字串 fixture，不依賴 reports/ 下的任何真實檔案——
所以報告清空後仍然跑得起來。

表頭格式取自清空前實際存在於倉庫中的五種寫法。
"""
from __future__ import annotations

import os
import sys
import tempfile
import unittest
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import report_meta as rm  # noqa: E402

# ---- 五種真實表頭格式（取自清空前的倉庫） -----------------------------------

H_BLOCKQUOTE = """# Meta Platforms (META) 投資研究 — 最終報告

> 四維度綜合分析 | 2026年5月
> 市值：15930億美元 | 股價：約601美元 | PE(TTM)：22倍

## 一、公司概況
"""

H_VALUATION_TRIPLE = """# 費埃哲(FICO) 晨星深度低估研究

> 晨星公允價值: $2,020 | 當前價: $1,181.82 | 潛在漲幅: +70.9%
> 護城河評級: 寬護城河 | 行業: Software - Application
> 研究日期: 2026-05-19

## 一、公司概況
"""

H_BOLD_KV = """# 納斯達克100指數（NDX / QQQ）投資研究報告

**研究日期：2026年6月25日**
**資料截至：2026年6月24日**

## 資訊豐富度評級：A級
"""

H_MULTILINE_BOLD = """# 英偉達（NVDA）"判斷錯誤時的安全墊"深度分析

**報告日期**：2026年4月26日
**分析基準價**：$200 / 市值 $4.88萬億
**總股本**：24.43B（拆股後）
"""

H_HYBRID = """# 邁威爾科技（NASDAQ: MRVL）投資研究報告

> 四大師綜合分析框架：巴菲特 · 芒格 · 段永平 · 李錄
> 研究日期：2026年6月24日 | 股價：$281 | 市值：$2,470億
"""


class TestFrontmatter(unittest.TestCase):
    def test_no_frontmatter(self):
        fm, body = rm.split_frontmatter(H_BOLD_KV)
        self.assertEqual(fm, {})
        self.assertEqual(body, H_BOLD_KV)

    def test_parses_scalars_and_list(self):
        text = ("---\n"
                "company: 輝達\n"
                "ticker: NVDA\n"
                "conviction: 4\n"
                "tags: [AI算力, 半導體]\n"
                "---\n"
                "# 標題\n")
        fm, body = rm.split_frontmatter(text)
        self.assertEqual(fm["company"], "輝達")
        self.assertEqual(fm["ticker"], "NVDA")
        self.assertEqual(fm["conviction"], "4")
        self.assertEqual(fm["tags"], ["AI算力", "半導體"])
        self.assertTrue(body.startswith("# 標題"))

    def test_strips_quotes_and_empty_value(self):
        fm, _ = rm.split_frontmatter('---\na: "x"\nb: \nc: [] \n---\n')
        self.assertEqual(fm["a"], "x")
        self.assertIsNone(fm["b"])
        self.assertEqual(fm["c"], [])

    def test_unterminated_frontmatter_is_not_frontmatter(self):
        """沒有收尾 --- 的檔案不該被吃掉正文。"""
        text = "---\ncompany: X\n# 其實是分隔線開頭的正文\n"
        fm, body = rm.split_frontmatter(text)
        self.assertEqual(fm, {})
        self.assertEqual(body, text)

    def test_horizontal_rule_after_h1_is_not_frontmatter(self):
        """報告內文常有 ---，但不在第一行，不該誤判。"""
        fm, body = rm.split_frontmatter(H_VALUATION_TRIPLE)
        self.assertEqual(fm, {})

    def test_dump_skips_none_and_empty_list(self):
        out = rm.dump_frontmatter(
            {"company": "輝達", "conviction": None, "tags": [], "ticker": "NVDA"},
            rm.FRONTMATTER_ORDER)
        self.assertIn("company: 輝達", out)
        self.assertIn("ticker: NVDA", out)
        self.assertNotIn("conviction", out)
        self.assertNotIn("tags", out)
        self.assertTrue(out.startswith("---\n") and out.endswith("---\n"))

    def test_roundtrip(self):
        meta = {"company": "輝達", "ticker": "NVDA", "date": "2026-08-22",
                "tags": ["AI算力", "半導體"]}
        fm, _ = rm.split_frontmatter(
            rm.dump_frontmatter(meta, rm.FRONTMATTER_ORDER) + "# 標題\n")
        self.assertEqual(fm["company"], "輝達")
        self.assertEqual(fm["tags"], ["AI算力", "半導體"])


class TestHeaderDate(unittest.TestCase):
    def test_five_real_header_formats(self):
        cases = [
            (H_BLOCKQUOTE, "2026-05-01"),        # 只有年月 → 補 01
            (H_VALUATION_TRIPLE, "2026-05-19"),
            (H_BOLD_KV, "2026-06-25"),
            (H_MULTILINE_BOLD, "2026-04-26"),
            (H_HYBRID, "2026-06-24"),
        ]
        for header, expected in cases:
            with self.subTest(expected=expected):
                self.assertEqual(rm.parse_header_date(header), expected)

    def test_ignores_prices_and_market_cap(self):
        """$2,020 / 24.43B / 15930億 這類數字不該被當成日期。"""
        self.assertIsNone(rm.parse_header_date(
            "> 公允價值: $2,020 | 當前價: $1,181.82 | 總股本 24.43B"))

    def test_rejects_impossible_date(self):
        self.assertIsNone(rm.parse_header_date("2026年13月45日"))

    def test_no_date(self):
        self.assertIsNone(rm.parse_header_date("# 標題\n\n沒有任何日期"))


class TestMasters(unittest.TestCase):
    def test_simplified_and_traditional_both_match(self):
        self.assertEqual(rm.derive_masters("", "巴菲特 · 芒格 · 段永平 · 李錄"),
                         ["巴菲特", "蒙格", "段永平", "李錄"])
        self.assertEqual(rm.derive_masters("", "巴菲特 芒格 李录"),
                         ["巴菲特", "蒙格", "李錄"])

    def test_normalises_to_traditional(self):
        """簡體輸入要正規化成繁體輸出（CLAUDE.md 的台灣正體規範）。"""
        self.assertEqual(rm.derive_masters("03-行业竞争分析-芒格视角", ""), ["蒙格"])
        self.assertEqual(rm.derive_masters("04-风险管理层评估-李录视角", ""), ["李錄"])

    def test_none(self):
        self.assertEqual(rm.derive_masters("random", "no masters here"), [])


class TestTypeAndCompany(unittest.TestCase):
    def test_series_detected_from_path(self):
        p = "reports/Adobe/公众号/《看懂Adobe》/02-商业模式-订阅制印钞机.md"
        self.assertEqual(rm.derive_type(p), "series")

    def test_type_from_filename(self):
        self.assertEqual(
            rm.derive_type("reports/Marvell/投研报告/20260624-投研报告-Marvell-investment-research.md"),
            "research")
        self.assertEqual(
            rm.derive_type("reports/騰訊/騰訊-earnings-2025Q4.md"), "earnings")

    def test_company_is_first_dir_under_root(self):
        self.assertEqual(
            rm.derive_company("reports/英伟达/专题/20260426-安全垫分析.md"), "英伟达")

    def test_file_directly_under_root_has_no_company(self):
        self.assertIsNone(rm.derive_company("reports/nasdaq-100-research.md"))


class TestReviewAndStatus(unittest.TestCase):
    def test_review_by_uses_type_period(self):
        self.assertEqual(rm.derive_review_by("2026-01-01", "earnings"), "2026-04-11")
        self.assertEqual(rm.derive_review_by("2026-01-01", "research"), "2026-06-30")
        self.assertEqual(rm.derive_review_by("2026-01-01", "industry"), "2027-01-01")

    def test_series_has_no_review_date(self):
        self.assertIsNone(rm.derive_review_by("2026-01-01", "series"))

    def test_status_transitions(self):
        today = date(2026, 8, 22)
        # 尚未到期
        self.assertEqual(rm.compute_status("2026-09-01", "research", today), "fresh")
        # 逾期但未超過一個週期(180天)
        self.assertEqual(rm.compute_status("2026-08-01", "research", today), "review_due")
        # 逾期超過一個週期
        self.assertEqual(rm.compute_status("2025-01-01", "research", today), "stale")

    def test_series_always_archived(self):
        self.assertEqual(rm.compute_status(None, "series", date(2026, 8, 22)), "archived")


class TestSlug(unittest.TestCase):
    def test_ascii_safe_and_stable(self):
        p = "reports/晨星深度低估/FICO-宽护城河-低估71%/研究报告.md"
        s1 = rm.make_slug(p, "FICO", "2026-05-19")
        s2 = rm.make_slug(p, "FICO", "2026-05-19")
        self.assertEqual(s1, s2, "同一份報告必須得到同一個 slug")
        self.assertTrue(all(c.isalnum() or c == "-" for c in s1),
                        f"slug 必須是 ASCII-safe，實際為 {s1}")
        self.assertIn("fico", s1)
        self.assertIn("20260519", s1)

    def test_distinct_paths_distinct_slugs(self):
        a = rm.make_slug("reports/A/x.md", None, "2026-01-01")
        b = rm.make_slug("reports/B/x.md", None, "2026-01-01")
        self.assertNotEqual(a, b)

    def test_pure_chinese_path_still_ascii(self):
        s = rm.make_slug("reports/英伟达/专题/安全垫分析.md", None, "2026-04-26")
        self.assertTrue(all(c.isalnum() or c == "-" for c in s), s)

    def test_ticker_dot_normalised(self):
        self.assertIn("2449-tw", rm.make_slug("reports/京元電子/x.md", "2449.TW", None))


class TestDeriveEndToEnd(unittest.TestCase):
    """derive() 的整合測試——寫真實暫存檔，涵蓋路徑地雷。"""

    def _write(self, relpath: str, content: str) -> str:
        full = os.path.join(self.tmp, relpath)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as f:
            f.write(content)
        return full

    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.tmp = self._tmpdir.name
        self._orig_root = rm.ROOT
        rm.ROOT = self.tmp

    def tearDown(self):
        rm.ROOT = self._orig_root
        self._tmpdir.cleanup()

    def test_header_date_and_ticker(self):
        p = self._write("reports/Marvell/投研报告/20260624-投研报告-Marvell-investment-research.md",
                        H_HYBRID)
        m = rm.derive(p, use_git=False)
        self.assertEqual(m["company"], "Marvell")
        self.assertEqual(m["date"], "2026-06-24")   # 檔名日期優先
        self.assertEqual(m["type"], "research")
        self.assertEqual(m["_masters"], ["巴菲特", "蒙格", "段永平", "李錄"])
        self.assertEqual(m["_missing"], [])

    def test_date_falls_back_to_header_when_filename_has_none(self):
        p = self._write("reports/晨星深度低估/FICO-宽护城河-低估71%/研究报告.md",
                        H_VALUATION_TRIPLE)
        m = rm.derive(p, use_git=False)
        self.assertEqual(m["date"], "2026-05-19")
        self.assertEqual(m["ticker"], "FICO")

    def test_path_with_space(self):
        p = self._write("reports/GE Vernova/投研报告/20260623-GEV.md", H_BOLD_KV)
        m = rm.derive(p, use_git=False)
        self.assertEqual(m["company"], "GE Vernova")
        self.assertEqual(m["date"], "2026-06-23")

    def test_series_inherits_sibling_date(self):
        base = "reports/Adobe/公众号/《看懂Adobe》"
        self._write(f"{base}/00-系列说明.md", H_BOLD_KV)          # 帶 2026-06-25
        p = self._write(f"{base}/02-商业模式-订阅制印钞机.md",
                        "# 商業模式\n\n沒有日期的系列文\n")
        m = rm.derive(p, use_git=False)
        self.assertEqual(m["type"], "series")
        self.assertEqual(m["date"], "2026-06-25", "應從同目錄兄弟檔繼承日期")
        self.assertEqual(m["status"], "archived")
        self.assertIsNone(m["review_by"])

    def test_existing_frontmatter_wins(self):
        p = self._write("reports/輝達/x-20260101-research.md",
                        "---\ncompany: 輝達\nticker: NVDA\ndate: 2026-08-22\n"
                        "conviction: 5\n---\n" + H_MULTILINE_BOLD)
        m = rm.derive(p, use_git=False)
        self.assertEqual(m["date"], "2026-08-22", "frontmatter 應蓋過檔名與表頭")
        self.assertEqual(m["ticker"], "NVDA")
        self.assertEqual(m["conviction"], "5")

    def test_missing_fields_are_reported_not_guessed(self):
        p = self._write("reports/無日期報告.md", "# 只有標題\n\n沒有公司也沒有日期\n")
        m = rm.derive(p, use_git=False)
        self.assertIsNone(m["company"])
        self.assertIsNone(m["date"])
        self.assertEqual(sorted(m["_missing"]), ["company", "date"])
        self.assertIsNone(m["conviction"], "人工判斷欄位不該被猜測")
        self.assertIsNone(m["priority"])


# ---- 端對端演練實測抓到的四個缺陷，以下為迴歸測試 ------------------------

H_SERIES_WITH_PROSE_DATE = """# 社交廣告帝國的關鍵資料

> 《看懂Meta》系列 · 第 01 篇 · 開篇
> 閱讀時間約 8 分鐘

---

## 90 美元到 736 美元再回 597 美元

2022 年 11 月，Meta 跌到 **90 美元**。沒有新的壞訊息，只是市場突然統一了敘事。
"""


class TestRegressions(unittest.TestCase):
    """演練時實際踩到的四個誤判。"""

    def test_prose_year_after_hr_is_not_the_report_date(self):
        """正文裡的歷史年份（2022 年 11 月）不是報告日期。"""
        self.assertIsNone(rm.parse_header_date(H_SERIES_WITH_PROSE_DATE))

    def test_metadata_lines_stop_at_horizontal_rule(self):
        lines = rm.metadata_lines(H_SERIES_WITH_PROSE_DATE)
        self.assertEqual(len(lines), 2)
        self.assertTrue(all(l.startswith(">") for l in lines))

    def test_team_directory_beats_filename(self):
        """团队分析/ 底下整組算 team，不能被「财务估值分析」判成 valuation。"""
        for fn_ in ("01-商业模式分析-段永平视角", "02-财务估值分析-巴菲特视角",
                    "03-行业竞争分析-芒格视角", "04-风险管理层评估-李录视角"):
            with self.subTest(fn_):
                self.assertEqual(
                    rm.derive_type(f"reports/Meta/团队分析/{fn_}.md"), "team")

    def test_series_directory_still_wins_over_team(self):
        self.assertEqual(
            rm.derive_type("reports/Adobe/公众号/《看懂Adobe》/01-开篇.md"), "series")

    def test_touyan_baogao_is_research(self):
        """『投研报告』未被 build_graph.TYPE_RULES 涵蓋。"""
        self.assertEqual(
            rm.derive_type("reports/GE Vernova/投研报告/20260623-投研报告-GE Vernova-GEV.md"),
            "research")

    def test_exchange_prefixed_ticker(self):
        """（NASDAQ: MRVL）這種寫法要抓得到。"""
        self.assertEqual(rm.derive_ticker("# 邁威爾科技（NASDAQ: MRVL）投資研究報告"), "MRVL")
        self.assertEqual(rm.derive_ticker("# Foo (NYSE:ABC) bar"), "ABC")

    def test_plain_parenthesised_ticker_still_works(self):
        self.assertEqual(rm.derive_ticker("# 費埃哲(FICO) 晨星深度低估研究"), "FICO")

    def test_ticker_stopwords_still_filtered(self):
        self.assertIsNone(rm.derive_ticker("# 某公司 PE(TTM) 分析"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
