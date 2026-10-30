# dsh-safety-ledger-check — Safety ledger check (Español)

[English](README.md) · [简体中文](README-zh.md) · [Español](README-es.md) · [Português](README-pt.md) · [हिन्दी](README-hi.md)

[![dshfind](https://dshfind.com/api/badge/PerryLink/dsh-safety-ledger-check?metric=downloads)](https://dshfind.com/en/plugins/PerryLink/dsh-safety-ledger-check?ref=badge)

`dsh-safety-ledger-check` verifica el registro de cualificación en seguridad de una obra: si las horas de formación alcanzan el mínimo legal, si el registro de formación contiene los cuatro elementos exigidos y si los certificados de operación especial están registrados y siguen vigentes el día en que la persona trabajó.

El paquete sigue la Orden n.º 60 del Ministerio de Vivienda (publicada el 2025-12-17, **en vigor el 2026-06-01**), cuyo artículo 45 deroga la 建质〔2008〕75号. Las reglas que citaban la 75号 están obsoletas y este paquete no cita ninguna.

## Install

```sh
dsh plugin --profile <name> add dsh-safety-ledger-check
dsh --profile <name> --dump-config | grep 'dsh-safety-ledger-check'
```

## What it looks like

![Workflow diagram for dsh-safety-ledger-check: document → rule pack → findings.](docs/assets/dsh-safety-ledger-check-flow.svg)

*Workflow overview: document → rule pack → findings.*

**Límite:** verifica el registro, no la obra. No comprueba la autenticidad de un certificado —eso exige la plataforma nacional de supervisión— ni decide si un oficio pertenece al catálogo de operaciones especiales. Una celda vacía se informa como «el registro no lo recoge», nunca como «no ocurrió».

## What it answers

- ¿Alcanzan los nuevos trabajadores las 24 horas y los responsables las 32?
- ¿Cada registro lleva hora, contenido, asistentes y resultado?
- ¿Tienen número de certificado los operarios de operación especial?
- ¿Seguía vigente el certificado el día trabajado?
- ¿Esperó seis meses quien obtuvo el certificado por primera vez?

## Standards it follows

Las citas son literales del portal del Gobierno chino: Orden n.º 3, artículos 9, 12, 13 y 22; y Orden n.º 60, artículos 3, 14, 20 y 22. Una regla se limita deliberadamente a `warn`: el artículo 12 de la Orden n.º 3 habla de «empresas de transformación y manufactura» y no nombra a las constructoras, así que el paquete cita el artículo tal cual y no inventa una cita específica para la construcción.

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
