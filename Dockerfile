FROM prestashop/prestashop:1.7.8.7-fpm

WORKDIR /
RUN rm -rf /var/www/html
COPY ./prestashop/root /var/www/html
WORKDIR /var/www/html

RUN chmod -R 777 /var/www/html

CMD ["/tmp/docker_run.sh"]

