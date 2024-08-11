import type { Component, VNode } from 'vue'

export type Table = {
    columns: Column[]
    rows: Row[]
}

export type Column = {
    key: string
    label: string
    labels: (row: Row) => string[]
    labelDefaultColor: string
    field: string
    classes: string | ((val: Value) => string)
    sortable: boolean
    link: string
    format?: (value: Value) => VNode
    icon: string
}

export type Row = Record<string, Value>

export type Value = string | number | string[]