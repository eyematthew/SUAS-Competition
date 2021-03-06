from ObjAvoidSimplified import *
import numpy as np

class Map(object):
    """
    Wrapper class for a map where obstacles are placed
    """

    def __init__(self, mass_holder, drone_mass):
        """
        Initialize

        :param mass_holder: The mass holder to initialize the map with
        :param drone_mass: The drone mass
        """
        self.mass_holder = mass_holder
        self.drone_mass = drone_mass

    def append_mass(self, mass):
        """
        Append a mass to the map

        :param mass: The mass you want to append to the map
        """
        self.mass_holder.append_mass(mass)

    def avoid_obstacles(self):
        """
        Run the map once to avoid obstacles
        """
        direction_change = self.drone_mass.apply_motions(self.mass_holder)
        self.mass_holder.update_obstacle_mass(self.drone_mass)

        return direction_change

    def add_waypoint(self, waypoint):
        """
        Add a waypoint to the drone_mass

        :param waypoint: The waypoint to add to the drone mass
        """
        self.drone_mass.add_waypoint(waypoint)

    def set_drone_location(self, new_drone_location):
        """
        Set the drone's location in the map & update the masses of all of the
        obstacles

        :param new_drone_location: The new location for the drone
        """
        self.drone_mass.set_point(new_drone_location)
        self.mass_holder.update_obstacle_mass(self.drone_mass)

    def get_drone_location(self):
        """
        Return's the drone mass' current position within the map
        """
        return self.drone_mass.get_point()

    def get_mass_holder(self):
        return self.mass_holder

    def get_drone_mass(self):
        return self.drone_mass

    def drawStationaryObjects(self, win):
        self.mass_holder.draw(win)
        self.drone_mass.get_waypoint_holder().draw(win)

    def draw(self, win):
        self.drone_mass.draw(win)

    def __repr__(self):
        representation = str(self.mass_holder) + "\n"
        representation += str(self.drone_mass) + "\n"

        return representation
