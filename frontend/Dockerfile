FROM node:18-alpine

WORKDIR /app

# Copy package files
ADD package*.json ./

# Install dependencies
RUN npm install --production

# Copy application
ADD src/ ./src/
ADD public/ ./public/

# Expose port
EXPOSE 3000

# Set environment variables
ENV NODE_ENV=production

# Start the application
CMD ["npm", "start"]