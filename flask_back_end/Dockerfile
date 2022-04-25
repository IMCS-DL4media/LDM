FROM python:3-alpine

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . /app
WORKDIR /app

# Expose the Flask port
EXPOSE 5000

CMD [ "python", "-u", "./server.py" ]

