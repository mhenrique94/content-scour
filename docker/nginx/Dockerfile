FROM node:18.18-slim as build

WORKDIR /app/front
COPY ./front/package.json ./
COPY ./front/package-lock.json ./
RUN npm ci --silent
COPY ./front/ ./
RUN npm run build

FROM nginx:stable-alpine
COPY --from=build /app/front/dist /usr/share/nginx/html
CMD ["nginx", "-g", "daemon off;"]