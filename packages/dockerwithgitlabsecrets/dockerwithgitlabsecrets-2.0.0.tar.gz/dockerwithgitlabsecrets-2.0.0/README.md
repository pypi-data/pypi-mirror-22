[![Build Status](https://travis-ci.org/wtsi-hgi/docker-with-gitlab-secrets.svg)](https://travis-ci.org/wtsi-hgi/docker-with-gitlab-secrets)
[![codecov.io](https://codecov.io/gh/wtsi-hgi/docker-with-gitlab-secrets/graph/badge.svg)](https://codecov.io/github/wtsi-hgi/docker-with-gitlab-secrets)
[![PyPI version](https://badge.fury.io/py/dockerwithgitlabsecrets.svg)](https://badge.fury.io/py/dockerwithgitlabsecrets)


# Docker With GitLab Secrets
*Wraps Docker to run with GitLab build variables.*

## Installation
Prerequisites:
- Python >= 3.6
- docker

Stable releases can be installed via [PyPI](https://pypi.python.org/pypi/dockerwithgitlabsecrets):
```bash
$ pip install dockerwithgitlabsecrets
```

Bleeding edge versions can be installed directly from GitHub:
```bash
$ pip install git+https://github.com/wtsi-hgi/docker-with-gitlab-secrets.git@commit_id_or_branch_or_tag#egg=dockerwithgitlabsecrets
```


## Usage
Wrap your prefixed Docker command with:
```bash
usage: docker-with-gitlab-secrets [-h] [--dwgs-config DWGS_CONFIG]
                                  [--dwgs-project DWGS_PROJECT]
                                  [--env-file ENV_FILE]

Docker With GitLab Secrets

optional arguments:
  -h, --help            show this help message and exit
  --dwgs-config DWGS_CONFIG
                        location of the configuration file (will default to
                        /Users/cn13/.dwgs-config.yml)
  --dwgs-project DWGS_PROJECT
                        GitLab project (if not namespaced in the form
                        "namespace/project", the default namespace defined in
                        the configuration file will be used). If not defined,
                        the default project in the configuration file will be
                        used
```

### Examples
Run a new container with secrets from a GitLab project:
```bash
docker-with-gitlab-secrets --dwgs-config my-config.yml --dwgs-project my-project \
    run --rm alpine printenv GITLAB_SECRET
```

Wrapping unrelated Docker commands will still work:
```bash
docker-with-gitlab-secrets --dwgs-config my-config.yml \
    version
```


## Configuration
Example:
```yml
gitlab:
  url: https://gitlab.example.com
  token: my-token
  project: hgi-systems  # Optional default project, which will be overriden by if `dwgs-project` is specified
  namespace: hgi        # Optional default namespace  
```


## Known Issues
- Docker [cannot pass newlines in variables via `--env-file`](https://github.com/moby/moby/issues/12997). Therefore 
multiline GitLab variables with have their line-breaks escaped to \\n.
