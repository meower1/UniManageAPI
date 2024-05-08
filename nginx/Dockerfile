FROM nginx

COPY nginx.conf /etc/nginx/nginx.conf
COPY fullchain.pem /etc/letsencrypt/live/uk1.meower1.tech/fullchain.pem
COPY privkey.pem /etc/letsencrypt/live/uk1.meower1.tech/privkey.pem
COPY options-ssl-nginx.conf /etc/letsencrypt/options-ssl-nginx.conf
COPY ssl-dhparams.pem /etc/letsencrypt/ssl-dhparams.pem
COPY static /app/static
