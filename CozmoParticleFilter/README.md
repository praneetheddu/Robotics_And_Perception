# Cozmo Particle Filter

Cozmo uses particle filter to localize within its arena. Cozmo identifies the symbol cards as localization markers that allows
the robot to recognize the image, gather position and orientation information, and calculates robot's odometry. This parameters 
are passed into the particle filter for convergence to take place. The robot travels in a small circle around the arena and 
waits for the particle markers to converge. Once the markers converged, the robot can travel to any given coordinates in the arena.
In this program, the robot travels to (6,10) (6 and 10 inches away from the origin).


Collaborated with David Joshua Dulle.
