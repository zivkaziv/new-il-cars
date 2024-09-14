docker run -d --restart unless-stopped \
           -e MAILJET_API_KEY=<key> \
           -e MAILJET_API_SECRET=<secret> \
           -e SENDER_EMAIL=niyud3@gmail.com \
           -e RECIPIENT_EMAIL=<email> \
           -e DATA_FILE=/data/latest_id.txt \
           -e SLEEP_TIME=14400 \
           -v /Users/zivkalderon/Code/new-cars/data:/data \
           car-data-monitor