FROM node:20
WORKDIR /app

# Copy only package.json first to leverage layer caching
COPY frontend/package.json ./

# Install deps (works even without a lockfile)
RUN npm install --no-audit --no-fund

# Now copy the rest of the app
COPY frontend/ .

EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
