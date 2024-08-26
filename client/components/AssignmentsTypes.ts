import type { Assignment, RfcToBe, RpcPerson, RpcRole } from '~/rpctracker_client'

export type ResolvedAssignment = Omit<Assignment, 'person'> & {
    person?: RpcPerson
}

export type ResolvedDocument = RfcToBe & {
    assignments?: ResolvedAssignment[]
    needsAssignment: RpcRole | null | undefined
}

export type ResolvedPerson = RpcPerson & {
    assignments?: Assignment[]
}