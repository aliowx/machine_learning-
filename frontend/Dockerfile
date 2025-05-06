# Stage 0, "build-stage", based on Node.js, to build and compile the frontend
FROM node:lts-alpine

WORKDIR /app/frontend

COPY package.json yarn.lock ./

RUN yarn install --frozen-lockfile

COPY . .

ARG VITE_API_URL=${VITE_API_URL}

RUN yarn build

FROM nginx:alpine

COPY --from=builder /app/frontend/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
