# dsh-safety-ledger-check — Safety ledger check (हिन्दी)

[English](README.md) · [简体中文](README-zh.md) · [Español](README-es.md) · [Português](README-pt.md) · [हिन्दी](README-hi.md)

[![dshfind](https://dshfind.com/api/badge/PerryLink/dsh-safety-ledger-check?metric=downloads)](https://dshfind.com/en/plugins/PerryLink/dsh-safety-ledger-check?ref=badge)

`dsh-safety-ledger-check` साइट के सुरक्षा-योग्यता रजिस्टर की जाँच करता है: प्रशिक्षण घंटे विधिक न्यूनतम तक पहुँचते हैं या नहीं, रजिस्टर में अपेक्षित चार तत्व हैं या नहीं, और विशेष-संचालन प्रमाणपत्र दर्ज हैं तथा काम के दिन वैध थे या नहीं।

पैक आवास मंत्रालय के आदेश 60 का अनुसरण करता है (2025-12-17 प्रकाशित, **2026-06-01 से प्रभावी**), जिसका अनुच्छेद 45 आदेश 建质〔2008〕75号 को निरस्त करता है। 75号 का हवाला देने वाले नियम पुराने हैं और यह पैक किसी को उद्धृत नहीं करता।

## Install

```sh
dsh plugin --profile <name> add dsh-safety-ledger-check
dsh --profile <name> --dump-config | grep 'dsh-safety-ledger-check'
```

## What it looks like

![Workflow diagram for dsh-safety-ledger-check: document → rule pack → findings.](docs/assets/dsh-safety-ledger-check-flow.svg)

*Workflow overview: document → rule pack → findings.*

**सीमा:** यह रजिस्टर जाँचता है, साइट नहीं। प्रमाणपत्र की प्रामाणिकता नहीं जाँचता — उसके लिए राष्ट्रीय पर्यवेक्षण मंच चाहिए — और यह भी तय नहीं करता कि कोई कार्य विशेष-संचालन सूची में है या नहीं। खाली कक्ष «रजिस्टर में दर्ज नहीं» बताता है, «हुआ ही नहीं» नहीं।

## What it answers

- नए कर्मचारी 24 घंटे और प्रबंधक 32 घंटे तक पहुँचते हैं?
- हर रजिस्टर में समय, सामग्री, प्रतिभागी और परिणाम हैं?
- विशेष-संचालन कर्मियों का प्रमाणपत्र क्रमांक दर्ज है?
- काम के दिन प्रमाणपत्र वैध था?
- पहली बार प्रमाणपत्र लेने वाले ने छह माह प्रतीक्षा की?

## Standards it follows

उद्धरण चीनी सरकार के पोर्टल से शब्दशः हैं: आदेश 3 के अनुच्छेद 9, 12, 13, 22; और आदेश 60 के अनुच्छेद 3, 14, 20, 22। एक नियम जानबूझकर केवल `warn` तक है: आदेश 3 का अनुच्छेद 12 «विनिर्माण इकाइयों» की बात करता है और निर्माण कंपनियों का नाम नहीं लेता, इसलिए पैक अनुच्छेद जैसा है वैसा उद्धृत करता है।

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

Full family index: [choose a checker by material](https://perrylink.github.io/zh/checkers/choose/) and [all plugins](https://github.com/PerryLink). This repository is one of them.

## License

[Apache License 2.0](LICENSE) © 2026 dsh-safety-ledger-check contributors.
