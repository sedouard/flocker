.. _glossary:

========
Glossary
========

.. contents::
  :local:

Flocker release types
=====================

.. note:: All Flocker documentation will refer the Production ready product, unless tagged Alpha or Beta.

.. _alpha-definition:

Alpha
   This product or feature is a proof-of-concept; expect API instability; lack of security; product instability.

.. _beta-definition:

Beta
   This product or feature is approaching readiness; expect minor API instability between versions; incomplete security; product stability for most common uses.

.. _production-ready-definition:

Production ready
   This product or feature is suitable for production use; expect API stability between versions; robust security; product stability for all supported uses.

Flocker terms
=============

.. _api-definition:

Flocker API
  A collection of RESTful API endpoints that allow you to configure a Flocker cluster programmatically with the tool and language of your choice.

.. _cli-definition:

Flocker CLI
  Also known as the Flocker client.
  This is a tool for controlling Flocker directly via the command line. It interfaces with the Flocker API.

.. _container-agent-definition:

Flocker Container Agent
  An agent which manages the Docker containers on a node.
  It manages containers using the Docker REST API.

.. _control-service-definition:

Flocker Control Service
  This service stores the configuration and state of the cluster. The Flocker Control Service can be deployed on a dedicated host or on one of the cluster nodes.
  The Flocker Control Service manages the Flocker ZFS Agent and the Flocker container, which in turn implement the changes to the configuration and state of the cluster.

.. _flocker-cli-definition:

The :code:`flocker-cli` package
  An operating system package which will install the Flocker client on a computer which is running a Linux operating system.

.. _flocker-node-definition:

The :code:`flocker-node` package
  An operating system package which will install the Flocker ZFS Agent and the Flocker Container Agent on a node which is running a Linux operating system.

.. _zfs-agent-definition:

Flocker ZFS Agent
  An agent which manages Flocker datasets on ZFS filesystems on a node.

Other terms
===========

.. _container-definition:

Container
   A virtual environment comprising an application and its dependencies. It isolates processes on the host operating system and uses the host kernel.

.. _client-definition:

Client
   A tool that controls the deployment and management of a container or group of containers, their contents and other attributes. For Flocker this is command line tool, often run locally.

.. _cluster-definition:

Cluster
   A system of connected containers.

.. _migrate-definition:

Migrate
   To move a volume, container, or cluster (or part of a cluster) to another node.

.. _node-definition:

Node
   A terminal in a network, either a physical or virtual machine.
