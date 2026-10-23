/**
 * dsh-safety-ledger-check — table shape and material contract.
 *
 * One row per person per training record or certificate. The ledger is deliberately
 * flat: a real site keeps 安全教育 and 特种作业 in separate books, but both are
 * "one person, one event, some fields", and joining them is the reader's job, not a
 * schema's. Keeping them in one table also means a single pass can answer "is this
 * welder allowed to work today", which is the question the tool exists for.
 *
 * What this cannot do: verify a certificate is genuine (that needs the national
 * platform), or decide whether a trade falls inside the special-operation catalogue
 * (that catalogue is published separately, per 60号令第二条).
 */

import { canonicaliseRow, parseTable, type TableSpec } from './shared/table.ts'
import { runTableCheck, type TableCheckOptions, type TableInput } from './shared/rows.ts'
import type { Ruleset } from './shared/rules.ts'

/** Tool id exposed to the model, and the row id in `cordis.patch.yml`. */
export const TOOL_NAME = 'safety_ledger_check'

/** The ledger's column aliases, declared once so both the spec and the guard see them. */
const COLUMNS = {
  personName: ['姓名', '人员姓名', '作业人员', 'personName'],
  trade: ['工种', '作业工种', 'trade'],
  educationLevel: ['教育级别', '三级教育', '培训级别', 'educationLevel'],
  trainingHours: ['学时', '培训学时', '岗前培训学时', 'trainingHours'],
  managerHours: ['管理岗学时', '负责人学时', 'managerHours'],
  trainingDate: ['培训日期', '培训时间', 'trainingDate'],
  trainingContent: ['培训内容', '内容', 'trainingContent'],
  assessResult: ['考核结果', '考核', '成绩', 'assessResult'],
  certNo: ['证书编号', '证书号', '特种作业证号', 'certNo'],
  certTrade: ['证书工种', '证载工种', 'certTrade'],
  workTrade: ['实际工种', '作业工种', 'workTrade'],
  certIssueDate: ['发证日期', '初次发证日期', 'certIssueDate'],
  certExpiryDate: ['证书有效期至', '有效期至', 'certExpiryDate'],
  workDate: ['作业日期', '上岗日期', 'workDate'],
  soloWorkDate: ['独立作业日期', '首次独立作业', 'soloWorkDate'],
  remark: ['备注', '说明', 'remark'],
} as const

/** How the material declares its table. */
export const SPEC: TableSpec = {
  rowKeys: ['rows', 'items', 'records', '台账', '人员'],
  columns: COLUMNS,
  header: {
    project: ['project', '项目名称', '工程名称'],
    unit: ['unit', '施工单位', '单位名称'],
    period: ['period', '期间', '月份'],
    checkedAt: ['checkedAt', '核对日期'],
    basis: ['basis', '依据'],
  },
}

/** Fields the material must carry somewhere for the reader to accept it. */
export const REQUIRE_ANY_OF = ['姓名', 'personName', '证书编号', 'certNo', '培训工时', 'trainingHours']

/**
 * Parse the material and attach its canonical field names.
 *
 * @param source - JSON or YAML text.
 * @param target - description of where the material came from.
 * @returns the normalised table, with each row's aliases resolved to field names.
 */
export function parseMaterial(source: string, target: string): TableInput {
  const table = parseTable(source, target, { ...SPEC, requireAnyOf: REQUIRE_ANY_OF })
  for (const row of table.rows) canonicaliseRow(row, SPEC)
  return table
}

/**
 * Run the rule pack against the material.
 *
 * @param input - normalised table.
 * @param ruleset - validated rule pack.
 * @param options - plugin identity, clock value, rule selection and overrides.
 * @returns the report.
 */
export function runCheck(input: TableInput, ruleset: Ruleset, options: TableCheckOptions) {
  return runTableCheck(input, ruleset, options)
}

export type { TableCheckOptions, TableInput }
