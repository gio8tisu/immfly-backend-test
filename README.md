# Immfly backend test

API Immfly media platform which allows us to display contents following a
hierarchical structure.

## Usage
1. Run Postgres and Django services using docker-compose:
```bash
docker-compose up [--build]
```

2. Fetch API on http:///localhost:8000:
```bash
curl http://localhost:8000/api/channels/
```

3. Initially, there won't be any contents or channels. You can create them
   though Djago admin page (browse to http://localhost:8000/admin/).

## Decisions
* Language and genre implemented as separate model/table in order to add structure.
* Content can exist without associated channel. But, when a channel is deleted, its contents are also deleted.
* Content metadata is included on the same Content model.
* Only one file per content.
* Use function-based views, instead relying on DRF's generic APIs, to allow flexibility.
* Channel cannot have itself as subchannel (implemented as database constraint).
* Channel can be subchannel of only one channel (a channel can only belong to 1 or no channels).
* Channel rating as separate function instead of model property.
* Channel constraints are applied on custom creation method instead of on model (`clean` method) or DB.
* Channels list endpoint returns only root channels (the rest should be nested).
* Dev. enviroment only (i.e., no WSGI with web server configuration).
* CI/CD just builds the docker image (doesn't push it to registry).
