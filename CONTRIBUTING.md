# Contributing

A big welcome and thank you for considering contributing to this project.

This project is a community effort and lives off your contributions, be it in
the form of bug reports, feature requests, discussions, or fixes and other
code changes.

Reading and following these guidelines will help us make the contribution
process easy and effective for everyone involved. It also communicates that you
agree to respect the time of the developers managing and developing these open
source projects. In return, we will reciprocate that respect by addressing your
issue, assessing changes, and helping you finalize your pull requests.

## Quicklinks

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
    - [Issues](#issues)
    - [Pull Requests](#pull-requests)
    - [Setup Development Environment](#setup-development-environment)
    - [Updating the SDK clients](#updating-the-sdk-clients)
    - [Testing](#testing)
    - [Documentation](#documentation)
- [Release Procedure](#release-procedure)
- [Getting Help](#getting-help)

## Code of Conduct

We take our open source community seriously and hold ourselves and other
contributors to high standards of communication. By participating and
contributing to this project, you agree to uphold our [Code of Conduct].

## Getting Started

Contributions are made to this repo via Issues and Pull Requests (PRs). A few
general guidelines that cover both:

- Search for existing Issues and PRs before creating your own.
- We work hard to makes sure issues are handled in a timely manner but,
  depending on the impact, it could take a while to investigate the root cause.
  A friendly ping in the comment thread to the submitter or a contributor can
  help draw attention if your issue is blocking.

### Issues

Issues should be used to report problems with this project, request a new
feature, or to discuss potential changes before a PR is created. When you
create a new Issue, a template will be loaded that will guide you through
collecting and providing the information we need to investigate.

If you find an Issue that addresses the problem you're having, please add your
own reproduction information to the existing issue rather than creating a new
one. Adding a [reaction] can also help be indicating to our maintainers that a
particular problem is affecting more than just the reporter.

### Pull Requests

PRs to our repositories are always welcome and can be a quick way to get your
fix or improvement slated for the next release. In general, PRs should:

- Only fix/add the functionality in question **OR** address wide-spread
  whitespace/style issues, not both.
- Add unit or integration tests for fixed or changed functionality
  (if a test suite already exists).
- Address a single concern in the least number of changed lines as possible.
- Include documentation in the repo or on our [docs site].
- Be accompanied by a complete Pull Request template (loaded automatically
  when a PR is created).

For changes that address core functionality or would require breaking changes
(e.g. a major release), it's best to open an Issue to discuss your proposal
first. This is not required but can save time creating and reviewing changes.

In general, we follow the [Forking Workflow]:

1. Fork the repository to your own Github account
2. Clone the project to your machine
3. Create a branch locally with a succinct but descriptive name
4. Commit changes to the branch
5. Following any formatting and testing guidelines specific to this repo
6. Push changes to your fork
7. Open a PR in our repository and follow the PR template so that we can
   efficiently review the changes.

We recommend that you add this repository as an [upstream remote] to your local
git repository so that you can fetch the latest updates.

On your local machine make sure you have the latest version of the `develop`
branch from this upstream repository:

    git checkout develop
    git pull upstream develop

### Setup Development Environment

We highly recommend using a new conda or pipenv environment.

    conda create --name nlp-sandbox-client python=3.8.5
    conda activate nlp-sandbox-client

Install the project in *develop* mode. This command must be executed each time
the content of *setup.py* is updated.

    pip install -e .

### Updating the SDK clients

The SDK clients have to be updated when the API version is updated.  Here are the steps to updating the SDK clients:

- `data-node` package
  ```
  openapi-generator generate -g python -o . --package-name datanode -i https://nlpsandbox.github.io/nlpsandbox-schemas/data-node/edge/openapi.json
  ```

- `annotator` package
  Must merge the three NLP annotator specifications together into one `openapi.yaml`:
  - [date](https://github.com/nlpsandbox/nlpsandbox-schemas/tree/develop/openapi/date-annotator)
  - [person](https://github.com/nlpsandbox/nlpsandbox-schemas/tree/develop/openapi/person-name-annotator)
  - [address](https://github.com/nlpsandbox/nlpsandbox-schemas/tree/develop/openapi/physical-address-annotator)
  ```
  openapi-generator generate -g python -o . --package-name annotator -i openapi.yaml
  ```

### Testing

Please add tests for new code. These might include unit tests (to test specific functionality of code that was added to support fixing the bug or feature), integration tests (to test that the feature is usable - e.g., it should have complete the expected behavior as reported in the feature request or bug report), or both.

This package uses [`pytest`](https://pytest.org/en/latest/) to run tests. The test code is located in the [test](./test) subdirectory.

Here's how to run the test suite:

```
pytest -vs test/
```

Tests are also run automatically by github actions on any pull request and are required to pass before merging.

### Documentation

`nlpsandboxclient` uses [Google style Python docstrings](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html).  All functions you add must abide by these standards.  The Documentation of each python module can be found in `docs/python` folder and are auto generated by `sphinx`.  If you are adding a new module, you must add to a `.rst` file into this folder.  If you are adding or modifying a command line client function, you must add/modify the files in `docs/client`.

To build documentation:

```
cd docs
make html
open _build/html/index.html
```

## Release Procedure

Maintainers are required to follow the procedure below when creating a new release.

TBA

## Getting Help

Join us on the [NLP Sandbox Discord server] and post your question to the
channel that best matches the topic of your request.

<!-- Links -->

[Code of Conduct]: https://github.com/auth0/open-source-template/blob/master/CODE-OF-CONDUCT.md
[upstream remote]: https://help.github.com/en/articles/configuring-a-remote-for-a-fork
[reaction]: https://github.blog/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/
[docs site]: https://github.com/nlpsandbox/nlpsandbox-website-synapse
[Forking Workflow]: https://www.atlassian.com/git/tutorials/comparing-workflows/forking-workflow
[NLP Sandbox Discord server]: https://nlpsandbox.io/discord