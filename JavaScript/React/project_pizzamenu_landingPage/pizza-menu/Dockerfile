FROM node:18-alpine

WORKDIR /app

# Install dependencies first
COPY package*.json ./
RUN npm install

# Copy source code (only needed if you want a working image without volumes)
COPY . .

EXPOSE 3000

# Enable file polling for Docker
ENV WATCHPACK_POLLING=true
ENV CHOKIDAR_USEPOLLING=true

# Run in dev mode (hot reload)
CMD ["npm", "run", "dev"]
