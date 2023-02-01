# Node as a builder
FROM node:16-alpine as builder

# copy the package.json to install dependencies
COPY package.json package-lock.json ./

# Install depedencies
RUN npm install && mkdir /evolve-ui && mv ./node_modules ./evolve-ui

# Change working directory
WORKDIR /evolve-ui

# COPY everything 
COPY . .

# Build frontend
RUN npm run build

# nginx 
FROM nginx:alpine

# Copy nginx config
COPY ./nginx.conf /etc/nginx/nginx.conf

## Remove default nginx index page
RUN rm -rf /usr/share/nginx/html/*

COPY --from=builder /evolve-ui/build /usr/share/nginx/html

EXPOSE 80

ENTRYPOINT ["nginx", "-g", "daemon off;"]