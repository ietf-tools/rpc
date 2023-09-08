<div align="center">

<img src="https://raw.githubusercontent.com/ietf-tools/common/main/assets/logos/rpc.svg" alt="RPC" height="125" />

<!-- [![Release](https://img.shields.io/github/release/ietf-tools/rpc.svg?style=flat&maxAge=300)](https://github.com/ietf-tools/rpc/releases) -->
[![License](https://img.shields.io/github/license/ietf-tools/rpc)](https://github.com/ietf-tools/rpc/blob/main/LICENSE)
![Node Version](https://img.shields.io/badge/node.js-18.x-green?logo=node.js&logoColor=white)
![Nuxt Version](https://img.shields.io/badge/nuxt-3-green?logo=nuxt.js&logoColor=white)
![Vue Version](https://img.shields.io/badge/vue-3-green?logo=vue.js&logoColor=white)

##### Web tool for the RFC Production Center

</div>

# Development in Docker

## Getting Started

### Creating an OIDC client
1. Run a local copy of datatracker in Docker. Use its default host port of 8000. In the admin, add an OpenID Connect Provider client. Settings are
   - Client type: confidential
   - Response type: code (authorization code flow)
   - Redirect URI: `http://localhost:8888/oidc/callback/`
   - JWT algorithm: RS256
   - Scopes: `openid profile email`
2. After saving the OpenID Connect Provider client, a client ID and client SECRET will be generated. Note these.

### Set up the RPC back end
1. Check out a working copy of this repository
2. In your working copy, create `secrets.env` containing
```
# Do not commit this file!
POSTGRES_PASSWORD=<whatever you want>
OIDC_RP_CLIENT_ID=<client ID from datatracker>
OIDC_RP_CLIENT_SECRET=<client SECRET from datatracker>
```
3. Start the docker containers with `docker compose up`
4. Open `http://localhost:8888`, click "Login", and authenticate with some datatracker user.

If this works, you will be redirected to a page that identifies you with the primary email address of the user you authenticated with.
