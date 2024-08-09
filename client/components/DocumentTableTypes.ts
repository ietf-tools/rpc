import type { Component } from 'vue'

export type Table<Columns extends Column[]> = {
    columns: Column<Keys>[],
    rows: Row[]
}

export type Column<Keys extends string[]> = {
    field: Keys[number],
    link: string,
    format?: () => Component,
    icon: string
}

export type Row<T extends string> = Record<T, Value>

export type Value = string | number | string[] | number[]