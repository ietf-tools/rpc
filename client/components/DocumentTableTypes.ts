import type { VNode } from 'vue'
import type { ColorEnum, Label } from '~/rpctracker_client'

export type Value = unknown

export type Row = Record<string, Value>

export interface Column<RowT extends Row> {
  key: keyof RowT
  label: string
  labels?: (row: RowT) => (Label | string)[]
  labelDefaultColor?: ColorEnum
  field?: keyof RowT
  classes?: string | ((val: Value) => string)
  sortable?: boolean
  link?: string | ((row: RowT, val: Value) => string)
  formatType?: 'all'
  format?: (value: Value) => VNode | VNode[] | string
  icon?: string
}
