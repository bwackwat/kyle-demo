# Kyle Demo

## Inspect Docker Stuff

```bash
sudo systemctl status docker
sudo systemctl status | less  # SHIFT + G scroll to bottom in less
sudo systemctl status | grep "docker"

sudo docker container ls -a  # All containers
sudo docker image ls -a  # All images
sudo docker status

sudo docker compose up -d
sudo docker compose up -d --build demo webserver  # Build a selection of services from docker-compose.yaml
sudo docker compose logs
sudo docker compose logs demo  # Logs from a specific service (name separate from image name OR container name)
```
