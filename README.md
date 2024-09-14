docker run -e MAILJET_API_KEY=<key> \
           -e MAILJET_API_SECRET=<secret> \
           -e SENDER_EMAIL=niyud3@gmail.com \
           -e RECIPIENT_EMAIL=<email> \
           -e DATA_FILE=/data/latest_id.txt \
           -v /Users/zivkalderon/Code/new-cars/data:/data \
           car-data-monitor