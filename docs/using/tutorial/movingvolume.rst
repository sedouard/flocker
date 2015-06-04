.. _tutorial-moving-a-data-volume:

==============================
Tutorial: Moving a Data Volume
==============================

In this tutorial (30 minutes)
-----------------------------

You will use Flocker to migrate a Docker container with its data volume from one host to another.
The container you move will be part of a two-container application, the other container will not move and the two will remain connected even when they are on different hosts.

To begin the tutorial you will first install the Flocker client on your local machine, then install Flocker onto two hosts.
You will then be ready to use Flocker to migrate a Docker container with a volume attached from one host to the other.

.. note:: This tutorial takes roughly 30 minutes, but because there are a few things to download, times might vary depending on the speed of your connection.

You will need
-------------

1. Somewhere to install the Flocker client.
Make sure you have **one** of the following on your machine:

- OS X with `Homebrew <http://brew.sh/>`_ installed.
- Ubuntu 14.04.

2. Two hosts for two instances of Flocker.
The options are:

- Two Virtual Machines (VMs) on your local machine. For this tutorial, you are supplied with Vagrant images to create the tutorial environment on VMs using VirtualBox, so you must have `Vagrant <https://www.vagrantup.com/>`_ and `VirtualBox <https://www.virtualbox.org/>`_ installed.
- AWS or Rackspace (you will need an account with root access).
- Physical hosts with a supported operating system.
- Any combination of the above.

.. note:: If you choose to use VMs on your local machine, you’ll need at least 4GB RAM.

Contents
--------

.. contents:: 
	:local:
	:backlinks: none
	:depth: 2
	
Overview
^^^^^^^^

You will be controlling your Flocker cluster via the CLI you've installed locally.
The following diagram illustrates the initial server-side Flocker setup that you will control via the CLI.

.. image:: images/try-flocker-tutorial-initial-setup.svg
   :width: 60 %
   :alt: In the initial server-side Flocker setup there are two servers, one of which has two Docker containers running; one container is a running a web application, the other has a Redis database with a volume.
   :align: center

The following diagram illustrates how the server-side Flocker setup will be configured at the end of the tutorial:

.. image:: images/try-flocker-tutorial-final-setup.svg
   :width: 60 %
   :alt: Following the completion of this tutorial the server-side Flocker setup will be configured with the web application still running within a container on the first server, while the Redis server with a volume is running on the second server.
   :align: center

Flocker manages the data migration and the link between the two containers.

.. To find out more about how Flocker manages migration of containers with volumes, see *add link here* 

Step 1: Installing the Flocker client
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The Flocker client runs locally on your machine, and will control the two instances of Flocker located on the hosts.
To install the Flocker client, run the following in your terminal:

OS X
****
.. task:: test_homebrew flocker-|latest-installable|
   :prompt: you@laptop:~$

Ubuntu 14.04
************
.. task:: install_cli ubuntu-14.04
   :prompt: you@laptop:~$

To test your installation, run the following to check that you have the Flocker client installed correctly:

.. prompt:: bash [you@laptop:~$]

   flocker-deploy --version
   
Successful installation will display the version of Flocker.

Step 2: Installing Flocker on your hosts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Option A: Installing Flocker on local VMs
*****************************************

.. note:: You must have `Vagrant <https://www.vagrantup.com/>`_ and `VirtualBox <https://www.virtualbox.org/>`_  installed to create the VMs and start the containers for this tutorial.

In Step 1 you installed the Flocker client on your local machine.
For the next step in this tutorial you now need two instances of Flocker, each on a separate host.
Flocker manages the links, ports, and volumes associated with Docker containers and can move them around after deployment.
To install Flocker (plus dependencies) on the hosts, run the following command and Vagrant will create the environments you need:

.. version-code-block:: console

   you@laptop:~$ curl -O https://docs.clusterhq.com/en/|latest-installable|/_downloads/Vagrantfile && \
   curl -O https://docs.clusterhq.com/en/|latest-installable|/_downloads/cluster.crt && \
   curl -O https://docs.clusterhq.com/en/|latest-installable|/_downloads/user.crt && \
   curl -O https://docs.clusterhq.com/en/|latest-installable|/_downloads/user.key && \
   vagrant up && \
   [ -e "${SSH_AUTH_SOCK}" ] || eval $(ssh-agent) && \
   ssh-add ~/.vagrant.d/insecure_private_key

Option B: Installing Flocker on AWS or Rackspace
************************************************

The two instances of Flocker each run on a separate host.
Flocker manages the links, ports, and volumes associated with Docker containers and can move them around after deployment.
To install Flocker (plus dependencies), follow the links to the direct instructions:

- :ref:`AWS install instructions <aws-install>`
- :ref:`Rackspace install instructions <rackspace-install>`

Step 3: Deploying an app on the first host
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You will now have the Flocker client installed on your local machine and two instances of Flocker, each on a different host.
Now you will create two Docker containers on one of the hosts.
One is a Python web application and the other is Redis server, which stores its data on a volume.

Download the first 2 .yml files that we have provided:

.. version-code-block:: console

	you@laptop:~$ curl -O https://docs.clusterhq.com/en/|latest-installable|/_downloads/docker-compose.yml
	you@laptop:~$ curl -O https://docs.clusterhq.com/en/|latest-installable|/_downloads/deployment-node1.yml

.. note:: There are 3 .yml files to download. These contain the application and deployment configuration. You can edit these files if you need to change the IP addresses to match your hosts'.

The ``docker-compose.yml`` file describes your distributed application (note, Docker Compose was formerly known as Fig):

    .. literalinclude:: docker-compose.yml
       :language: yaml

The ``deployment-node1.yml`` file describes which containers to deploy, and where:

    .. literalinclude:: deployment-node1.yml
       :language: yaml

.. note:: If you are using real servers on AWS, you'll need to change the IP addresses in the deployment file.

Secondly, install the web application and server on the first host:

.. prompt:: bash [you@laptop:~$]

	flocker-deploy 172.16.255.250 deployment-node1.yml fig.yml

Visit http://172.16.255.250/ (or the IP of the first host that you are using). You will see the visit count displayed.

Visit http://172.16.255.251/ (or the IP of the second host that you are using).
You will see that the count persists because Flocker routes the traffic from either host named in the deployment file to the one that has the application.

Run the following from within the :file:`/vagrant-flocker` folder to check that the Redis server container is running on the first host:

.. prompt:: bash [you@laptop:~$]
   
   cd vagrant-flocker
   vagrant ssh node1 -c "docker ps" 
     
You should see the Redis server container in the output from Docker.
   
If you are running on AWS, manually SSH onto the first node and run :code:`docker ps` to see the same output.

Step 4: Migrating a container to the second host
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The diagram below illustrates your current server-side Flocker setup:

.. image:: images/try-flocker-tutorial-initial-setup.svg
   :width: 60 %
   :alt: In the server-side Flocker setup there are two servers, one of which has two Docker containers running; one container is a running a web application, the other has a Redis database with a volume.
   :align: center

You'll need to download the last of the .yml files that we have provided:

.. version-code-block:: console

	you@laptop:~$ curl -O https://docs.clusterhq.com/en/|latest-installable|/_downloads/deployment-node2.yml

To move the container with the Redis server along with its data volume, use the deployment-node2.yml file:

    .. literalinclude:: deployment-node2.yml
       :language: yaml

Run the following:

.. prompt:: bash [you@laptop:~$]

	flocker-deploy 172.16.255.250 deployment-node2.yml fig.yml
	
The container on the Redis server and its volume have now both been moved to the second host.
Flocker has maintained its link to the web application on the first host.

Visit http://172.16.255.250/ (or the IP of the first host that you are using).
You will see the visit count is still persisted.

Visit http://172.16.255.251/ (or the IP of the second host that you are using).
You will see that the count still persists, even though the container with the volume has moved between hosts.

Run the following from within the vagrant-flocker folder to check that the Redis server container is running on the first host:

.. prompt:: bash [you@laptop:~$]

   cd vagrant-flocker
   vagrant ssh node2 -c "docker ps"

You should see the Redis server container in the output from Docker.

If you are running on AWS, manually SSH onto the second node and run :code:`docker ps` to see the same output.

Success!
^^^^^^^^

You have now set up your first Flocker cluster and moved a Docker container with its volume while persisting its link to a web app on another server.

The following diagram illustrates how your server-side Flocker setup looks now:

.. image:: images/try-flocker-tutorial-final-setup.svg
   :width: 60 %
   :alt: The server-side Flocker setup is be configured with the web application still running within a container on the first server, while the Redis server with a volume is now running on the second server.
   :align: center
