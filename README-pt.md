# dsh-safety-ledger-check — Safety ledger check (Português)

[English](README.md) · [简体中文](README-zh.md) · [Español](README-es.md) · [Português](README-pt.md) · [हिन्दी](README-hi.md)

[![dshfind](https://dshfind.com/api/badge/PerryLink/dsh-safety-ledger-check?metric=downloads)](https://dshfind.com/en/plugins/PerryLink/dsh-safety-ledger-check?ref=badge)

`dsh-safety-ledger-check` verifica o registo de qualificação em segurança de uma obra: se as horas de formação atingem o mínimo legal, se o registo contém os quatro elementos exigidos e se os certificados de operação especial estão registados e ainda válidos no dia em que a pessoa trabalhou.

O pacote segue a Portaria n.º 60 do Ministério da Habitação (publicada em 2025-12-17, **em vigor em 2026-06-01**), cujo artigo 45.º revoga a 建质〔2008〕75号. As regras que citavam a 75号 estão obsoletas e este pacote não cita nenhuma.

## Install

```sh
dsh plugin --profile <name> add dsh-safety-ledger-check
dsh --profile <name> --dump-config | grep 'dsh-safety-ledger-check'
```

## What it looks like

![Workflow diagram for dsh-safety-ledger-check: document → rule pack → findings.](docs/assets/dsh-safety-ledger-check-flow.svg)

*Workflow overview: document → rule pack → findings.*

**Limite:** verifica o registo, não a obra. Não confirma a autenticidade de um certificado — isso exige a plataforma nacional de supervisão — nem decide se um ofício pertence ao catálogo de operações especiais. Uma célula vazia é reportada como «o registo não o contém», nunca como «não aconteceu».

## What it answers

- Os novos trabalhadores atingem as 24 horas e os responsáveis as 32?
- Cada registo leva hora, conteúdo, participantes e resultado?
- Os operários de operação especial têm número de certificado?
- O certificado ainda era válido no dia trabalhado?
- Quem obteve o certificado pela primeira vez esperou seis meses?

## Standards it follows

As citações são literais do portal do Governo chinês: Portaria n.º 3, artigos 9.º, 12.º, 13.º e 22.º; e Portaria n.º 60, artigos 3.º, 14.º, 20.º e 22.º. Uma regra fica deliberadamente em `warn`: o artigo 12.º da Portaria n.º 3 fala de «empresas de transformação e manufactura» e não nomeia construtoras, pelo que o pacote cita o artigo como está e não inventa uma citação específica.

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
