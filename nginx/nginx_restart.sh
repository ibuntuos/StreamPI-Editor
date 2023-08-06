docker stop streampi
docker cp /etc/nginx/rtmp.conf streampi:/etc/nginx/rtmp.conf
docker start streampi
