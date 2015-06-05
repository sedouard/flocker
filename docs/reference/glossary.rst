.. glossary::

.. note:: All Flocker documentation will refer the :term:`Production ready` product, unless tagged :term:`Alpha` or :term:`Beta`.

Production ready
   This product or feature is suitable for production use. You can expect API stability between versions, robust security, and product stability for all supported uses.

Beta
   This product or feature is approaching readiness. You can expect minor API instability between versions, incomplete security, and product stability for most common uses.

Alpha
   This product or feature is a proof-of-concept. You can expect API instability, lack of security, and product instability.

Flocker API
  A collection of RESTful API endpoints that allow you to configure a Flocker cluster programmatically with the tool and language of your choice.

Flocker CLI
  This is a tool for controlling Flocker directly via the command line. It interacts with the :term:`Flocker API`.

Flocker Container Agent
  An agent which manages the Docker containers on a node.
  It manages containers using the Docker REST API.

Flocker Control Service
  This service stores the configuration and state of the cluster.
  The Flocker Control Service can be deployed on a dedicated node or on one of the cluster nodes.
  The Flocker Control Service manages the :term:`Flocker ZFS Agent` and the :term:`Flocker Container Agent`, which in turn implement the changes to the configuration and state of the cluster.
  For more information, see :ref:`architecture`.

The `flocker-cli` package
  An operating system package which will install the Flocker client on a computer which is running a Linux operating system or OS X.

The `flocker-node` package
  An operating system package which will install the :term:`Flocker ZFS Agent` and the :term:`Flocker Container Agent` on a node which is running a Linux operating system.

Flocker ZFS Agent
  An agent which manages Flocker datasets on ZFS filesystems on a node.

Container
   A Docker container - a virtual environment consisting of an application and its dependencies.
   It isolates processes on the host operating system and uses the host kernel.

Client
   A tool that controls the deployment and management of a container or group of containers, their contents and other attributes.
   For Flocker this is command line tool, often run locally.

Cluster
   A system of connected nodes.

Migrate
   To move a volume or container to another node.

Node
   Either a physical or virtual machine within a network.
