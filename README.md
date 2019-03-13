# script-run
Deamon for starting, running, monitoring and stopping arbitrary scripts on a debian system (e.g rasbian) 

## Installation
We offer a debian package in our repository. Add

	deb http://www.bayceer.uni-bayreuth.de/repos/apt/debian stretch main

to your /etc/apt/source.list and import the key:

	sudo su
	wget -O - http://www.bayceer.uni-bayreuth.de/repos/apt/conf/bayceer_repo.gpg.key |apt-key add -

Then run

	sudo apt-get update
	sudo apt-get install script-run

## Configuration
Edit /etc/script-run.conf. Just add one line per script to start. Scripts are started as user root. Don't forget
to restart the service on each change of configuration:

	sudo /etc/init.d/script-run restart


## Autostart
The package does not put script-run in the autostart. To start script-run per default, run the following command:

	sudo update-rc.d script-run defaults
