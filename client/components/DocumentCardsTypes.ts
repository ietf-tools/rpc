export interface ADocument {
  id: string
  name: string
  external_deadline: string
  needsAssignment?: {
    name: string
  }
  assignments: string[]
  pages: number
}
