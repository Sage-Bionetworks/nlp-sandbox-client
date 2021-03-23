# NLP Sandbox Client

[![GitHub Release](https://img.shields.io/github/release/nlpsandbox/nlpsandbox-client.svg?include_prereleases&color=94398d&labelColor=555555&logoColor=ffffff&style=for-the-badge&logo=github)](https://github.com/nlpsandbox/nlpsandbox-client/releases)
[![GitHub CI](https://img.shields.io/github/workflow/status/nlpsandbox/nlpsandbox-client/ci.svg?color=94398d&labelColor=555555&logoColor=ffffff&style=for-the-badge&logo=github)](https://github.com/nlpsandbox/nlpsandbox-client)
[![GitHub License](https://img.shields.io/github/license/nlpsandbox/nlpsandbox-client.svg?color=94398d&labelColor=555555&logoColor=ffffff&style=for-the-badge&logo=github)](https://github.com/nlpsandbox/nlpsandbox-client)
[![PyPi](https://img.shields.io/pypi/v/nlpsandbox-client.svg?color=94398d&labelColor=555555&logoColor=ffffff&style=for-the-badge&label=PyPi&logo=PyPi)](https://pypi.org/project/nlpsandbox-client)
[![Docker Pulls](https://img.shields.io/docker/pulls/nlpsandbox/cli.svg?color=94398d&labelColor=555555&logoColor=ffffff&style=for-the-badge&label=pulls&logo=docker)](https://hub.docker.com/r/nlpsandbox/cli)
[![Discord](https://img.shields.io/discord/770484164393828373.svg?color=94398d&labelColor=555555&logoColor=ffffff&style=for-the-badge&label=Discord&logo=discord)](https://nlpsandbox.io/discord "Realtime support / chat with the community and the team")
[![Coverage Status](https://img.shields.io/coveralls/github/nlpsandbox/nlpsandbox-client.svg?color=94398d&labelColor=555555&logoColor=ffffff&style=for-the-badge&label=coverage&logo=Coveralls)](https://coveralls.io/github/nlpsandbox/nlpsandbox-client?branch=)

## Overview

NLP Sandbox Client Library for Python.  This repository consists of 3 packages

- `datanode`: Python SDK client that wraps [data-node API](https://nlpsandbox.github.io/nlpsandbox-schemas/data-node/latest/openapi.json)
- `annotator`: Python SDK client for the NLP annotators ([date-annotator API](https://nlpsandbox.github.io/nlpsandbox-schemas/date-annotator/latest/openapi.json), [person-name-annotator API](https://nlpsandbox.github.io/nlpsandbox-schemas/person-name-annotator/latest/openapi.json), [physical-address-annotator API](https://nlpsandbox.github.io/nlpsandbox-schemas/physical-address-annotator/latest/openapi.json))
- `nlpsandboxclient` - Convenience functions that infer user behavior of the above two SDK clients.

## Specification

- API version: 1.0.1
- Docker image: `nlpsandbox/cli`

## Documentation

`nlpsandboxclient` functionality is documented [here](https://nlpsandbox.github.io/nlpsandbox-client/)

## Installation

```
pip install nlpsandbox-client
nlp-cli --version
```

## Contributing and developing

Thinking about contributing to `nlpsandbox-client`? Get started by reading our [Contributor Guide](CONTRIBUTING.md).
