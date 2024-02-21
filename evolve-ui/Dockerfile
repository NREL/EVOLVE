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

EXPOSE 3000

CMD ["npm", "run", "start"]
