import { Configuration, RpcTrackerApi } from '~/rpctracker_client'

const safeMethods = ['GET', 'HEAD', 'OPTIONS', 'TRACE']

export const useApi = () => {
  const csrf = useCookie('csrftoken', { sameSite: 'strict' })
  const configuration = new Configuration({
    basePath: 'http://localhost:8088',
    middleware: [{
      pre: ({ init: { method, headers } }) => {
        // Add CSRF token for unsafe methods
        if (!safeMethods.includes(method)) {
          headers['X-CSRFToken'] = csrf.value
        }
      }
    }]
  })
  return new RpcTrackerApi(configuration)
}
