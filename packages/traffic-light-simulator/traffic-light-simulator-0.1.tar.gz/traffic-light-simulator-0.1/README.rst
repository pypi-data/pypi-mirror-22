##############################
Traffic Light Simulator Goals
##############################

This is an attempt to simulate a simple traffic light. You can specify how long you want each light show before it changes to the next light, as well as the number of light changes you want before the simulator stops running the current light.

#############################
Install
#############################

Install with pip
#####################

You may want to do this in a virtualenv if you don't want to clutter up your global packages. If you want to use a virtualenv just: ::

  $ virtuanelv testenv
  $ cd testenv
  $ . bin/activate

Then simply install with pip: ::

  $ pip install traffic-light-simulator
  
Clone the repo
##################

Clone this repo, cd into the traffic_light_simulator module

#############################
 Running the simulator
#############################

If you installed with pip, you have a script available to you to run the simulator. Simply enter into your terminal: ::

  $ traffic-light-simulator

Otherwise if you cloned the repo just run the user_interface.py with your interpreter: ::

  $ python user_interface.py

