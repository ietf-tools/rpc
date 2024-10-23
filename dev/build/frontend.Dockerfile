FROM node:22 AS build
WORKDIR /workspace
COPY ./client ./
RUN npm install && \
    npm run build

FROM node:22
LABEL maintainer="IETF Tools Team <tools-discuss@ietf.org>"
WORKDIR /workspace
COPY --from=build /workspace/.output .
ENV NITRO_PORT=3000
CMD ["node", "server/index.mjs"]
EXPOSE 3000
