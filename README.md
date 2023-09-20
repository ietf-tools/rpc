<div align="center">

<img src="https://raw.githubusercontent.com/ietf-tools/common/main/assets/logos/rpc.svg" alt="RPC" height="125" />

<!-- [![Release](https://img.shields.io/github/release/ietf-tools/rpc.svg?style=flat&maxAge=300)](https://github.com/ietf-tools/rpc/releases) -->
[![License](https://img.shields.io/github/license/ietf-tools/rpc)](https://github.com/ietf-tools/rpc/blob/main/LICENSE)
![Python Version](https://img.shields.io/badge/python-3.11-blue?logo=python&logoColor=white)
![Django Version](https://img.shields.io/badge/django-4-teal?logo=django&logoColor=white)
![Node Version](https://img.shields.io/badge/node.js-20-green?logo=node.js&logoColor=white)
![Nuxt Version](https://img.shields.io/badge/nuxt-3-green?logo=nuxt.js&logoColor=white)
![Vue Version](https://img.shields.io/badge/vue-3-green?logo=vue.js&logoColor=white)

##### Web tool for the RFC Production Center

</div>

- [**Production Website**](https://rpc.ietf.org)
- [Changelog](https://github.com/ietf-tools/rpc/releases)
- [Contributing](https://github.com/ietf-tools/.github/blob/main/CONTRIBUTING.md)
- [Development](#development)
  - [Prerequisites](#prerequisites)
  - [Getting Started](#getting-started)
  - [Using VS Code](#using-vs-code)
  - [Using Generic](#using-generic)
  - [Commands](#commands)
  - [Cleanup](#cleanup)

# Development

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install) *(Windows only)*

## Getting Started

1. Clone this repository locally.
2. Create an OIDC client in Datatracker:  
   - Run a local copy of [datatracker](https://github.com/ietf-tools/datatracker) in Docker. Use its default host port of `8000`. In the admin, add an OpenID Connect Provider client using the following settings:
      - Client type: `confidential`
      - Response type: `code` *(authorization code flow)*
      - Redirect URI: `http://localhost:8088/oidc/callback/`
      - JWT algorithm: `RS256`
      - Scopes: `openid profile email`
    - After saving the OpenID Connect Provider client, a **client ID** and **client SECRET** will be generated. Note these.
3. Back in the rpc project root folder, create a copy of `secrets.env.example` with the name `secrets.env`. Edit the file and add the values generated in the previous step:
    ```env
    # Do not commit this file!
    OIDC_RP_CLIENT_ID=<client ID from datatracker>
    OIDC_RP_CLIENT_SECRET=<client SECRET from datatracker>
    ```
4. Continue using the steps for your preferred IDE:
   - [Visual Studio Code](#using-vs-code)
   - [Generic](#using-generic)

## Using VS Code

1. Open the project in VS Code
2. When prompted, in the lower right corner, click <kbd>Reopen in container</kbd>
3. Wait for the devcontainer to initialize. *(This can take a few seconds/minutes the first time)*
4. The editor will automatically open 2 side-by-side terminals, running both the backend API server and the client dev server.
5. Open http://localhost:8088 in your browser and login using some datatracker user.

## Using Generic

1. In a terminal, from the project root folder, run the command:
    ```sh
    docker/run
    ```
2. Wait for the containers to initialize. *(This can take a few seconds/minutes the first time)*
3. A tmux session will automatically be started with the backend API server running on the left and the client dev server running on the right.
4. Open http://localhost:8088 in your browser and login using some datatracker user.

#### Tips

- The tmux default prefix binding is set to `Ctrl+Space` and mouse control is enabled by default.
- If you exit tmux, you'll land in a normal zsh prompt. Type `exit` again to quit and stop the containers.

## Commands

#### Django Backend API (`/workspace`)

- Start Server: `./manage.py runserver 8001`

#### Nuxt Client (`/workspace/client`)

- Run Dev Server: `npm run dev`
- Generate Production Build: `npm run build`

## Cleanup

To fully tear down the containers created in either of the VS Code or Generic steps, run the following command from the project root folder:
```sh
docker/cleanall
```
Press <kbd>Y</kbd> to confirm.
