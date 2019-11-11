FROM node:8.14.0-jessie-slim
ENV PORT=3000
EXPOSE $PORT
COPY . /
RUN npm install
CMD ["node", "/server.js"]