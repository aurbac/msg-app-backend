FROM public.ecr.aws/bitnami/node:latest
ENV PORT=3000
EXPOSE $PORT
COPY . /app
WORKDIR /app
RUN npm install
CMD ["node", "server.js"]