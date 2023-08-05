Changes
*******

0.5.3 (2017-05-11)
==================

* added volume for etc/ in Dockerfile.

0.5.2 (2016-10-21)
==================

* changed default ports, generate .env file for docker-compose

0.5.1 (2016-10-20)
==================

* fix folder permissions of etc/ and var/run/ in Dockerfile.

0.5.0 (2016-10-19)
==================

* update recipe to buildout deployment.
* simplified Dockerfile.
* removed custom.cfg template.

0.4.8 (2015-12-23)
==================

* update readme.
* fixed settings and buildout-options.

0.4.7 (2015-12-23)
==================

* fixed /data volume permissions.
* added update-user as default command.
* add buildout-options for docker.cfg.
* added default envs hostname and user.

0.4.6 (2015-12-22)
==================

* using only volume /data for /var/lib in Dockerfile.

0.4.5 (2015-12-17)
==================

* fixed command generation in Dockerfile.

0.4.4 (2015-12-16)
==================

* added ``command`` option.
* custom.cfg for docker is copied to ``.docker.cfg``.
* added ``.dockerignore`` file.

0.4.3 (2015-12-15)
==================

* added settings option to generate a custom.cfg for docker image.

0.4.2 (2015-12-14)
==================

* added git-url, git-branch, subdir and buildout-cfg options.

0.4.1 (2015-12-10)
==================

* fixed setting of EXPOSE in Dockerfile.

0.4.0 (2015-12-10)
==================

* added environment and expose options.
* enabled travis.

0.3.2 (2015-09-25)
==================

* fixed malleefowl default port in dockerfile template.
* changed dockerfile volumes.

0.3.1 (2015-09-24)
==================

* updated Dockerfile template.
* added output-port option.

0.3.0 (2015-09-22)
==================

* updated Dockerfile template.
* more options added.

0.2.2 (2015-08-05)
==================

* cleaned up ... removed conda dependency.
* update to buildout 2.x.

0.2.1 (2015-04-13)
==================

* Updated Dockerfile template for CentOS builds (sudo was missing).

0.2.0 (2015-03-16)
==================

* Updated Dockerfile template for birdhouse environments.

0.1.1 (2014-11-13)
==================

* Updated Dockerfile template ... starts only supervisord.
* Fixed example in Readme.

0.1.0 (2014-11-05)
==================

* Initial Release.
