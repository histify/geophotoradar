FROM node:22-alpine3.20 AS base
ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable
WORKDIR /app
COPY pnpm-lock.yaml package.json ./
RUN --mount=type=cache,id=pnpm,target=/pnpm/store pnpm install --frozen-lockfile

FROM base AS dev
EXPOSE 3000
CMD [ "pnpm", "run", "dev", "--host", "0.0.0.0" ]


FROM base AS builder
RUN pnpm generate


FROM nginx:1.27.1-alpine AS prod
COPY ./docker/frontend.nginx.conf /etc/nginx/templates/default.conf.template
COPY --from=builder /app/dist /usr/share/nginx/html
ENV API_HOST=api
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
