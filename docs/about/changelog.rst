*********
Changelog
*********

This changelog is used to track all major changes to **nlpsandboxclient**.

For older releases, visit the `GitHub releases`_.

.. _Github releases: https://github.com/nlpsandbox/nlpsandbox-client/releases

v1.0.0
------
- Client uses NLP sandbox API version 1.0.2
- Update annotate note to accept `Note` instead of `TextAnnotatorRequest` object
- Update client to support v1.0.2 schemas
- Change `date`, `person`, `address` to `nlpsandbox:date-annotator`, `nlpsandbox:person-name-annotator` and `nlpsandbox:physical-address-annotator`
- Add support for `Python` 3.9
- Add initial unit tests
- Create `tool` and `datanode` cli modules

v0.4.1
------
- Client uses NLP sandbox API version 1.0.1

v0.3.1
------
- Client uses NLP sandbox API version 1.0.0
