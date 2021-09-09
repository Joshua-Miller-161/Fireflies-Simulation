# Fireflies-Simulation
Python simulation in which virtual fireflies communicate with one another to sync their flashes

Each 'firefly' is represented by a dot which alternates color between yellow and black. The rate at which they change colors is fixed but each firefly's phase for their flashing cycle is randomly initialized. If two or more fireflies wander within a certain radius of each other then they will set their phases equal. The simulation has numerous parameters which can affect how fast the fireflies sync up, if at all. These include the distance away from one another needed to sync phases, the rate of the flasing cycle, the maximum speed the fireflies can travel, and more.
