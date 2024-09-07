FROM node:22-alpine3.20 AS base
ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable
WORKDIR /app
COPY pnpm-lock.yaml package.json ./
RUN --mount=type=cache,id=pnpm,target=/pnpm/store pnpm install --frozen-lockfile

FROM base AS dev
EXPOSE 3000
CMD [ "pnpm", "run", "dev", "--host", "0.0.0.0", "--port", "80" ]


FROM base AS builder
COPY . /app/
RUN pnpm generate


FROM nginx:1.27.1-alpine AS prod
COPY --from=builder /app/.output/public /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
