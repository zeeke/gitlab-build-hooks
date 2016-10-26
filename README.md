# Gitlab Build Hooks

This tool can be used in a gitlab project in order to integrate other
systems (currently only Trello) with the gitlab project.

## Features

Create a build job in the .gitlab-ci.yml file:


### Link Gitlab commit to Trello cards

```yaml
...

trello_integrations:
  image: zeeke/gitlab-build-hooks
  script: trello_commit_to_card.py \
                --gitlab-token <...> \
                --trello-board-id <...> \
                --trello-token <...> \
                --trello-api-key <...>
```

