import type { VNode } from 'vue'

export interface Table {
  columns: Column[]
  rows: Row[]
}

export interface Column {
  key: string
  label: string
  labels?: (row: Row) => string[]
  labelDefaultColor?: string
  field?: string
  classes?: string | ((val: Value) => string)
  sortable?: boolean
  link?: string | ((row: Row, val: Value) => string)
  format?: (value: Value) => VNode | string
  icon?: string
}

export type Row = Record<string, Value>

export type Value = unknown
