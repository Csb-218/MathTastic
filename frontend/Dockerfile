FROM node:20.11.0-slim

WORKDIR /app

RUN adduser --system --group nodejs
USER nodejs

COPY --from=builder /app/dist ./dist
COPY package*.json ./

RUN npm install --production

ENV HOST=0.0.0.0
ENV PORT=5173

EXPOSE 5173

CMD ["npm", "run", "preview"]

