FROM centos:centos7

WORKDIR /app

RUN curl -sL https://rpm.nodesource.com/setup_12.x --output addNodeRepo.sh
RUN sh addNodeRepo.sh
RUN yum install -y nodejs

COPY . .
RUN npm install
RUN npm install @vue/cli -g

CMD ["npm", "run", "serve"]
