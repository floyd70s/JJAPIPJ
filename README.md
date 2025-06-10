# JJAPIPJ

docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
docker rmi $(docker images -q)
docker volume rm $(docker volume ls -q)
docker network rm $(docker network ls -q | grep -vE '^(bridge|host|none)$')

esto limpia todo:
docker system prune -a --volumes -f


paso a paso para ejecutar:
docker network create test-network

docker run -d \
  --name selenium \
  --network test-network \
  --network-alias selenium \
  -p 4444:4444 \
  selenium/standalone-firefox:latest


Sitúate en la carpeta de tu proyecto
docker build -t corte-suprema-app .


docker run -d \
  --name jjapi \
  --network test-network \
  -p 5001:5000 \
  -e SELENIUM_REMOTE_URL=http://selenium:4444/wd/hub \
  corte-suprema-app

  Verifica que ambos contenedores estén en la red
docker network inspect test-network

