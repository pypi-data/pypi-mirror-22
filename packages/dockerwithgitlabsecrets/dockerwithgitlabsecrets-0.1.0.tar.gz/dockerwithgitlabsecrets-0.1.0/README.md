# Docker With GitLab Secrets

Example usage:
```bash

# Config will default to ~/.dwgs.conf if not specified
docker-with-gitlab-secrets --dwgs-config /somewhere/dwgs.conf --dwgs-project hgi-systems \
    --rm --env-file /higher/precedence -e HIGHEST_PRECEDENCE 123 -it run ubuntu bash
```

Example configuration:
```yml
---

gitlab:
  url: https://gitlab.example.com
  token: my-token
  project: hgi-systems  # Optional default project, which will be overriden by if `dwgs-project` is specified
  namespace: hgi        # Optional default namespace  
```


## Known Issues
- Docker [cannot pass newlines in variables via `--env-file`](https://github.com/moby/moby/issues/12997). Therefore 
GitLab variables
New lines in secret variables 