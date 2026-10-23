# Changelog

## 0.1.0

First release. Ten rules over one safety-qualification ledger.

- Follows 住建部令第60号 (published 2025-12-17, **in force 2026-06-01**), which
  repealed 建质〔2008〕75号 in its 第四十五条. Rules quoting 75号 are stale; the pack
  quotes none of them.
- One rule is deliberately capped at `warn`: 令第3号 第十二条 names 「加工、制造业等
  生产单位」 and does not name construction enterprises, so the three-level induction
  is quoted as it stands and marked `derived-from-principle` rather than given a
  fabricated construction citation.
- **One rule is deliberately not implemented.** 60号令第二十条 makes 证书工种 ≠ 实际工种
  equivalent to working without a certificate (up to ¥100,000). The engine has no
  exact text-equality kind, and the nearest one compares bigrams — it would score
  「塔式起重机司机」 and 「塔式起重机信号工」 as the same trade. A false negative on a
  rule of that weight is worse than not running it, so SL-009 is listed under
  `notImplemented` with the reason, in the pack and in the report.
- Nine of the ten ledgers are listed as not covered, by name.
- 33 tests.
