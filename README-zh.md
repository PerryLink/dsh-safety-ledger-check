# dsh-safety-ledger-check — 施工安全资格台账核对

[English](README.md) · [简体中文](README-zh.md) · [Español](README-es.md) · [Português](README-pt.md) · [हिन्दी](README-hi.md)

<!-- topblock:v1 -->
> **这是什么**　核对施工安全资格台账：三级教育、培训档案、特种作业证书、有效期、工种匹配。
> **给谁用**　施工安全员、资料员；不用懂命令行。
> **你交什么**　这项核对用到的原始材料（表格、清单或文书）；不改原件。Excel 可先转成 JSON/YAML，对话里也能代转。
> **它不做什么**　不判合规、不认定责任、不替代审核人；只列材料内部能逐条指认的差异。
> **怎么开始**　在 WorkBuddy / 扣子搜「安全合规核对包」（本检查是其中一项；上架以商城为准）；或命令行：
> `dsh plugin --profile <name> add dsh-safety-ledger-check`
<!-- /topblock:v1 -->

[![dshfind](https://dshfind.com/api/badge/PerryLink/dsh-safety-ledger-check?metric=downloads)](https://dshfind.com/en/plugins/PerryLink/dsh-safety-ledger-check?ref=badge)

`dsh-safety-ledger-check` 核对施工安全资格台账：培训学时是否达到法定下限、培训档案是否有规章要求的四要素、特种作业证书是否有登记且在作业当日仍然有效。

规则库跟随**住建部令第60号**（2025-12-17 公布，**2026-06-01 施行**），其第四十五条明确废止建质〔2008〕75号。凡引用 75 号的规则都已过期，本包一条都不引。

## Install

```sh
dsh plugin --profile <name> add dsh-safety-ledger-check
dsh --profile <name> --dump-config | grep 'dsh-safety-ledger-check'
```

## What it looks like

![Workflow diagram for dsh-safety-ledger-check: document → rule pack → findings.](docs/assets/dsh-safety-ledger-check-flow.svg)

*Workflow overview: document → rule pack → findings.*

**边界：** 核对的是台账，不是现场。不验证证书真伪（那要上全国工程质量安全监管信息平台），也不判断某工种是否属于特种作业范围（工种目录按 60 号令第二条另行规定）。空格报的是「台账没有记录」，不是「没有发生过」。

## What it answers

- 新上岗人员的岗前培训是否达到 24 学时？负责人/安管人员是否达到 32 学时？
- 每条培训记录是否都有时间、内容、参加人员、考核结果？
- 特种作业人员是否登记了证书编号？
- 作业当日证书是否仍在有效期内？
- 首次取证人员是否满 6 个月才独立作业？

## Standards it follows

引文逐字取自中国政府网：

- 《生产经营单位安全培训规定》（令第3号）第九条（32/12 学时）、第十二条（三级教育）、第十三条（24 学时）、第二十二条（档案四要素）。
- 《建筑施工特种作业人员管理规定》（住建部令第60号）第三条、第十四条（3 年有效期）、第二十条（按证载工种作业）、第二十二条（六个月实习）。

有一条**故意只到 warn**：令第3号第十二条写的是「加工、制造业等**生产单位**」，没有点名建筑施工企业。建筑工地的三级教育来自行业规定与地方细则，所以本包照原文引用，标 `derived-from-principle`，不伪造一条针对建筑业的引文。

## Compatibility

| Surface | Status |
|---|---|
| Harness | peer range `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` |
| Node | `^22.19.0 || >=24.0.0` |
| Platforms | all (pure ESM; no native code, no network, no model call) |

## What it does

Ten rules over one flat ledger. dateGap compares two dates with a required minimum gap, so validity is expressed as expiry minus work date at least one day. One rule is deliberately not implemented and the pack says why.

## Configuration

| Key | Default | Meaning |
|---|---|---|
| `rulesFile` | `rules/safety-ledger-check.yaml` | 规则库路径 |

## Material format

One row per person per training record or certificate; aliases are declared in src/model.ts.

## Rule sources

Quotations live in rules/evidence/clauses.md and in the pack. Known limits: certificates are not verified against the national platform, the special-operation catalogue is not embedded, and only one of the ten ledgers is covered.

## Troubleshooting

- **The plugin installs but the tool never appears**: check that `main` resolves to `lib/index.mjs` and that `pnpm run build` produced it.
- **`dsh plugin add` rejects the package**: the peer range covers `0.1.x` and `0.2.x`; outside it, grant an explicit exemption.
- **A rule did not run**: read the `skipped` array.

## Development

```sh
pnpm install
pnpm run typecheck
pnpm test
pnpm run build
node ../scripts/sync-shared.mjs dsh-safety-ledger-check
```

## PerryLink DSH Plugin Family

完整清单（62 个核查器 + 通用插件）见 [按材料选核查器](https://perrylink.github.io/zh/checkers/choose/)；本仓只是其中一个。

## License

[Apache License 2.0](LICENSE) © 2026 dsh-safety-ledger-check contributors.
