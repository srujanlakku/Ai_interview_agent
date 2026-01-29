FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm install

# Copy application code
COPY frontend/src ./src
COPY frontend/public ./public
COPY frontend/*.html ./
COPY frontend/*.config.js ./

# Build
RUN npm run build

# Expose port
EXPOSE 3000

# Serve built app
CMD ["npm", "run", "preview"]
