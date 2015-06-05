==============================
Tutorial: Moving a Data Volume
==============================

.. note:: This tutorial takes roughly 30 minutes, but because there are a few things to download, times might vary depending on the speed of your connection.

You will use Flocker to migrate a Docker container with its data volume from one host to another.
The container you move will be part of a two-container application, the other container will not move and the two will remain connected even when they are on different hosts.

To begin the tutorial you will first install the Flocker client on your local machine, then install Flocker onto two hosts.
You will then be ready to use Flocker to migrate a Docker container with a volume attached from one host to the other.

You will be controlling your Flocker cluster via the CLI you've installed locally.
The following diagram illustrates the initial server-side Flocker setup that you will control via the CLI:

.. image:: images/flocker-tutorial-initial-setup.svg
   :width: 60 %
   :alt: In the initial server-side Flocker setup there are two servers, one of which has two Docker containers running; one container is a running a web application, the other has a Redis database with a volume.
   :align: center

The following diagram illustrates how the server-side Flocker setup will be configured at the end of the tutorial:

.. image:: images/flocker-tutorial-final-setup.svg
   :width: 60 %
   :alt: Following the completion of this tutorial the server-side Flocker setup will be configured with the web application still running within a container on the first server, while the Redis server with a volume is running on the second server.
   :align: center

Flocker manages the data migration and the link between the two containers.

To find out more about how Flocker manages migration of containers with volumes, see :ref:`data-volumes`.

If you have any feedback or problems, you can :ref:`talk-to-us`.

.. contents:: 
	:local:
	:backlinks: none
	:depth: 2

Before You Begin
================

Requirements
------------

To replicate the steps demonstrated in this tutorial, you will need:

* Ubuntu 14.04 or OS X with `Homebrew <http://brew.sh/>`_ installed.
* Two Virtual Machines (VMs) on your local machine.
  For this tutorial, you are supplied with Vagrant images to create the tutorial environment on VMs using VirtualBox, so you must have `Vagrant`_ and `VirtualBox`_ installed.
* At least 4GB RAM available.

Installing the client
=====================

The Flocker client runs locally on your machine, and will control the two instances of Flocker located on the hosts.
To install the Flocker client, run the following in your terminal:

OS X
----

.. task:: test_homebrew flocker-|latest-installable|
   :prompt: you@laptop:~$

Ubuntu 14.04
------------

.. task:: install_cli ubuntu-14.04
   :prompt: you@laptop:~$

To test your installation, run the following to check that you have the Flocker client installed correctly:

.. prompt:: bash you@laptop:~$

   flocker-deploy --version

Installing Flocker on local VMs
===============================

Install two instances of Flocker, each on a separate node.
Flocker manages the links, ports, and volumes associated with Docker containers and can move them around after deployment.
To install Flocker on the nodes, run the following command and Vagrant will create the environments you need:

.. version-code-block:: console

   you@laptop:~$ curl -O https://docs.clusterhq.com/en/|latest-installable|/_downloads/Vagrantfile && \
   curl -O https://docs.clusterhq.com/en/|latest-installable|/_downloads/cluster.crt && \
   curl -O https://docs.clusterhq.com/en/|latest-installable|/_downloads/user.crt && \
   curl -O https://docs.clusterhq.com/en/|latest-installable|/_downloads/user.key && \
   vagrant up && \
   [ -e "${SSH_AUTH_SOCK}" ] || eval $(ssh-agent) && \
   ssh-add ~/.vagrant.d/insecure_private_key

Deploying an app on the first host
==================================

You will now have the client installed on your local machine, and two instances of Flocker, each on a different node.
Firstly, you will create two Docker containers on one of the hosts.
One is a Python web application and the other is Redis server, which stores its data on a volume.

Download the following :file:`.yml` files:

.. version-code-block:: console

   you@laptop:~$ curl -O https://docs.clusterhq.com/en/|latest-installable|/_downloads/docker-compose.yml
   you@laptop:~$ curl -O https://docs.clusterhq.com/en/|latest-installable|/_downloads/deployment-node1.yml
   you@laptop:~$ curl -O https://docs.clusterhq.com/en/|latest-installable|/_downloads/deployment-node2.yml

.. note:: You can edit these files if you need to change the IP addresses to match your nodes.

The :file:`docker-compose.yml` file describes your distributed application (:file:`docker-compose.yml` was formerly known as :file:`fig.yml`):

    .. literalinclude:: docker-compose.yml
       :language: yaml

The :file:`deployment-node1.yml` file describes which containers to deploy, and where:

    .. literalinclude:: deployment-node1.yml
       :language: yaml

Secondly, install the web application and server on the first host:

.. prompt:: bash you@laptop:~$

	flocker-deploy 172.16.255.250 deployment-node1.yml docker-compose.yml

Visit http://172.16.255.250/ (or the IP of the first host that you are using). You will see the visit count displayed.

Visit http://172.16.255.251/ (or the IP of the second host that you are using).
You will see that the count persists because Flocker routes the traffic from either node named in the deployment file to the one that has the application.

Migrating a container to the second host
========================================

The diagram below illustrates your current server-side Flocker setup:

.. image:: images/flocker-tutorial-initial-setup.svg
   :width: 60 %
   :alt: In the server-side Flocker setup there are two servers, one of which has two Docker containers running; one container is a running a web application, the other has a Redis database with a volume.
   :align: center

To move the container with the Redis server along with its data volume, use the :file:`deployment-node2.yml` file:

    .. literalinclude:: deployment-node2.yml
       :language: yaml

Run the following:

.. prompt:: bash you@laptop:~$

	flocker-deploy 172.16.255.250 deployment-node2.yml docker-compose.yml

The container on the Redis server and its volume have now both been moved to the second host.
Flocker has maintained its link to the web application on the first host.

Visit http://172.16.255.250/ (or the IP of the first host that you are using).
You will see the visit count is still persisted.

Visit http://172.16.255.251/ (or the IP of the second host that you are using).
You will see that the count still persists, even though the container with the volume has moved between hosts.

Success!
========

You have now set up your first Flocker cluster and moved a Docker container with its volume while persisting its link to a web app on another server.

The following diagram illustrates how your server-side Flocker setup looks now:

.. image:: images/flocker-tutorial-final-setup.svg
   :width: 60 %
   :alt: The web application is still running within a container on the first server, while the Redis server with a volume is now running on the second server.
   :align: center
