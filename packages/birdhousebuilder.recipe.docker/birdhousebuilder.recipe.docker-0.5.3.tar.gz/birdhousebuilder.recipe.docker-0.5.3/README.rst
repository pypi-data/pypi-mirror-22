******************************
birdhousebuilder.recipe.docker
******************************

.. image:: https://travis-ci.org/bird-house/birdhousebuilder.recipe.docker.svg?branch=master
   :target: https://travis-ci.org/bird-house/birdhousebuilder.recipe.docker
   :alt: Travis Build

Introduction
************

``birdhousebuilder.recipe.docker`` is a `Buildout`_ recipe to generate a `Dockerfile`_ for `Birdhouse`_ applications.

.. _`Buildout`: http://buildout.org/
.. _`Dockerfile`: https://www.docker.com/
.. _`Birdhouse`: http://bird-house.github.io/

Usage
*****

The recipe will generate a Dockerfile for your Birdhouse application. You can find the Dockerfile in the root folder of the application.

Supported options
=================

This recipe supports the following options:

**app**
   The name of your application. Default: birdhouse

**maintainer**
   The maintainer of the Dockerfile.

**description**
   Description of the Dockerfile.

**vendor**
   The vendor of the application. Default: Birdhouse

**version**
   The version of the application. Default: 1.0.0

**hostname**
   The hostname of the docker container. Default: localhost

**http-port**
   The HTTP port of the app service. Default: 8080

**https-port**
   The HTTPS port of the app service. Default: 8443

**output-port**
   The WPS output port of the wps apps service. Default: 8000


Example usage
=============

The following example ``buildout.cfg`` generates a Dockerfile:

.. code-block:: ini

  [buildout]
  parts = docker

  [docker]
  recipe = birdhousebuilder.recipe.docker
  app = emu
  maintainer = Birdhouse
  description = Emu WPS Application
  version = 0.5.0
  hostname = emu-demo.local
  http-port = 8094
  output-port = 38094
