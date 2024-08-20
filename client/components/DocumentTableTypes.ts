import type { VNode } from 'vue'
import type { ColorEnum } from '~/rpctracker_client'

export type Value = unknown

export type Row = Record<string, Value>

export interface Column {
  key: string
  label: string
  labels?: (row: Row) => string[]
  labelDefaultColor?: ColorEnum
  field: string
  classes?: string | ((val: Value) => string)
  sortable?: boolean
  link?: string | ((row: Row, val: Value) => string)
  format?: (value: Value) => VNode | string
  icon?: string
}

export interface Table {
  columns: Column[]
  rows: Row[]
}
