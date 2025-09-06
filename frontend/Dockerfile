FROM node:18-alpine
WORKDIR /app
COPY package.json package.json
COPY tsconfig.json tsconfig.json
COPY vite.config.ts vite.config.ts
COPY index.html index.html
COPY src src
RUN npm install
CMD ["npm", "run", "dev", "--", "--host"]
