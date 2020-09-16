# Use the official image as a parent image.
FROM node:12.18-slim

# Set the working directory.
WORKDIR /evolve/react_app

# Copy the file from your host to your current location.
COPY package.json .

# Run the command inside your image filesystem.
RUN npm install
ENV PATH /evolve/react_app/node_modules/.bin:$PATH

# Copy the rest of your app's source code from your host to your image filesystem.
COPY . .

# Inform Docker that the container is listening on the specified port at runtime.
EXPOSE 3000

# Run the specified command within the container.
CMD ["npm","start"]
