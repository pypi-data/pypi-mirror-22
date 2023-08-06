docker-compose wrapper allowing for user data and env. var defaults
===================================================================

``dcw`` can be invoked with exactly the same commands as
docker-compose.  If ``-f``/``--file`` is specified as the first option
the filename to be read will be taken from the argument. Otherwise
``docker-compose.yml`` is assumed (currently the alternative default
files are not tested/read) the YAML file.

The YAML file has to be in the version: "2" format.

``dcw`` loads and processes the YAML file and invokes
``docker-compose --file=-`` and the original commandline arguments,
then pipes in the processed data (as YAML).

The examples in usage refer to a container `smtp` that implements an SMTP
"filter", accepting material on an incoming port, filtering spam and
viruses, and sending mail on to a relay for delivery.

version
=======

Tested version combinations:
- `docker-compose 1.8.1`, `dcw 0.5.0`

processing
==========

The following subsections describe the processing that ``dcw`` does
and the reasons for doing so.

reading defaults
----------------

The key value pairs under ``user-data -> env-defaults`` are taken
to populate ``os.environ``, unless the key already exists. This means
you can set defaults for the environment variables used in the
docker-compose YAML file.


For `smtp` this allows you to have specific ports that will be used on
the deployment machine "backed in", while on the development machine
(where there is the need for uninterrupted "normal" mail during
testing) some environment variables can be set, for port-numbers and
directories, that override the values in the YAML file.


stripping user-data
-------------------

Any existing top-level key "user-data" or starting with "user-data-" is
removed. This allows for storing additional data in the file
(which would require yet another configuration file or extraction
from YAML comments).

including defaults in Dockerfile actions
----------------------------------------

All of the environment variables specified in `env-defaults` are
written to the file ``.dcw_env_vars.inc`` (if the YAML file is newer
than that file). They are written with the environment variable value
if that is available, otherwise with the default as specified in the
YAML file.

The file looks like::

  export DOCKER_SMTP_HOST="some_host_name"
  export DOCKER_SMTP_DOMAIN="your_domain.com"
  export DOCKER_SMTP_RELAY="192.168.0.101"

and this file can be mapped in the Dockerfile with::

  ADD .dcw_env_vars.inc /tmp/env_vars.inc

and then used in some script in later (RUN) stanzas with::

  source /tmp/env_vars.inc


Example
=======

This is the first part of one of my ``docker-compose.yml`` files::

  version: '2'
  user-data:
    author: Anthon van der Neut <a.van.der.neut@ruamel.eu>
    description: postfix container
    env-defaults:
      NAME: submission
      PORT: 587    # external port, overridden during development
      DOCKER_HOST_IP: <hostip
  services:
    submission:
      container_name: ${NAME}
      build: .
      extra_hosts:
      - docker-host:${DOCKER_HOST_IP}
      ports:
      - ${PORT}:587


The "author" and "description" information can easily be extracted and
used by other processes.

While developing I cannot use the submission port (587) as that is
already taken, and there I do `export PORT=10587`. On my deployment machine
I don't want to have to set PORT to the default value. With ``dcw``
the PORT env. var is set to 587 because there is no environment var "PORT"
defined on that machine.

Volumes: directories vs files
=============================

If the volume you create doesn't exist yet on the host, Docker will
create a directory even though you might prefer an empty file.

If dcw finds that any of the host parts of the `volumes` list end in
`/` (i.e. has a slash before the ':') it will assume all directories have such a slash, and
any files will not have that. Based on that information each host
based path will be checked (and reported if not correct) and **each
non-existing path will be created** (i.e. empty directory or empty
file, as appropriate).


Extra commands
==============

The wrapper adds a few extra commands to `docker-compose`::

 bash               run bash in container
 generate           generate systemd/upstart auto startup file
 templates          list files used as template
 expand             show expanded YAML and .dcw_env_vars.inc
 truncate           truncate log file (needs sudo)

Limiting log size in 2.0
========================

Truncating is rather cruel. A better way to restrict output is
by adding a few lines to the `docker-compose.yaml` file (in the container section)::

    logging:   # https://docs.docker.com/engine/admin/logging/overview/#/json-file-options
      driver: json-file
      options:
        max-size: 100k
        max-file: "10"  # this is a number, has to be a string for Go


Templates
=========

The ``templates`` and ``generate`` option are used to generate systemd/upstart templates.
The templates are expanded and use ``\`` to limit the line length a bit.


