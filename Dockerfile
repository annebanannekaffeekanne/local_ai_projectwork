FROM python:3.11-slim

RUN apt-get update && apt-get install -y cron build-essential python3-dev

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# create documents directory and set permissions
RUN mkdir -p /app/documents
RUN touch /app/cron.log /app/background_update.log
RUN chmod -R 755 /app/documents
RUN chmod 666 /app/cron.log /app/background_update.log

# update cron job to use the updater.py script
RUN echo "0 3 * * * python /app/updater.py >> /app/cron.log 2>&1" > /etc/cron.d/dailyjob

RUN chmod 0644 /etc/cron.d/dailyjob
RUN crontab /etc/cron.d/dailyjob

CMD ["cron", "-f"]
