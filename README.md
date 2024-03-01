# Dont Be Like This
Because slluxx forgot to upload the source code to GitHub 💀

# Run the container
### Docker CLI
```docker run -d -v /somewhere/you/want/your/db:/app/db -e BOT_TOKEN=putyourtokenhere hax4dayz/dont-be-like-this```

### Docker Compose
```docker-compose
version: '3.7'

services:
  app:
    image: hax4dayz/dont-be-like-this
    volumes:
      - /somewhere/you/want/your/db:/app/db
    environment:
      BOT_TOKEN: putyourtokenhere
```

# Build the container yourself
```docker build -t YourDockerIOUsername/dont-be-like-this .```
