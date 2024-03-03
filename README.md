# Dont Be Like This

Because slluxx forgot to upload the source code to GitHub 💀

# Run the container

### Docker Compose

```docker-compose
version: '3.7'

services:
  app:
    image: hax4dayz/dont-be-like-this
    volumes:
      - database:/app/db
    environment:
      BOT_TOKEN: putyourtokenhere


volumes:
  database:
```

# Build the container yourself

`docker build -t YourDockerIOUsername/dont-be-like-this .`
