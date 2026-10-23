import { describeTablePlugin } from './table-plugin-suite.ts'
import { Config } from '../src/config.ts'
import { parseMaterial, runCheck, SPEC } from '../src/model.ts'
import { buildView } from '../src/view.ts'
import { inject, name, resolvePackageFile, TOOL_NAME } from '../src/index.ts'

/** A well-formed row: a tower-crane operator whose record and certificate agree. */
const good = {
  target: '安全教育与资格台账',
  rows: [
    {
      姓名: '李强',
      工种: '塔式起重机司机',
      教育级别: '班组',
      学时: '24',
      管理岗学时: '32',
      培训日期: '2026-03-01',
      培训内容: '岗位安全操作规程',
      考核结果: '合格',
      证书编号: '京A0120260001',
      证书工种: '塔式起重机司机',
      实际工种: '塔式起重机司机',
      发证日期: '2026-01-10',
      证书有效期至: '2029-01-10',
      作业日期: '2026-06-01',
      独立作业日期: '2026-09-01',
      备注: '',
    },
  ],
}

/** The same row with one column the spec does not know. */
const unknownColumn = {
  target: '安全教育与资格台账',
  rows: [{ 不存在的列: 'x', 另一个不存在的列: 'y' }],
}

describeTablePlugin({
  name,
  inject,
  TOOL_NAME,
  resolvePackageFile,
  Config,
  rulesFile: 'rules/safety-ledger-check.yaml',
  parseMaterial,
  runCheck,
  buildView,
  columnNames: SPEC.columns,
  samples: { good, unknownColumn },
})
