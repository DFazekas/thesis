#!/usr/bin/env python3

import os
import sys


# We need to import some python modules from the $SUMO_HOME/tools directory.
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit('Please declare environment variable: "SUMO_HOME"')
sys.path.append("./experiments/globalConfigs")

import traci
from constants import *


def getAllVehicleTypes():
    """Returns the vehicles for all vehicles actively in the simulation.

      Returns:
          [str]: The vehicle types.
    """
    return [{"id": id, "vehType": traci.vehicle.getTypeID(id)}
            for id in traci.vehicle.getIDList()]


def getConnCivilians():
    """Returns the IDs of all connected civilian vehicles actively
        in the simulation.

        Returns:
            [str]: IDs of connected civilian vehicles.
    """
    vehTypes = getAllVehicleTypes()
    return [
        veh for veh in vehTypes if veh['vehType'] == C_CIVILIAN]


def getEVs():
    """Returns all emergency vehicles."""
    vehTypes = getAllVehicleTypes()
    return [veh for veh in vehTypes if veh['vehType'] in [ER, C_ER]]


def getMultipleRoutes(vehList):
    """Returns the list routes for all vehicles provided.

    Args:
        vehList ([{id: str, vehType: str}]): Vehicles to search.

    Returns:
        [{veh: {id: str, vehType: str}, route: list(str)}]: [description]
    """
    routes = [{
        'veh': veh,
        'currentIndex': traci.vehicle.getRouteIndex(veh['id']),
        'route': getRoute(veh['id']),
        'remainingRoute': getRoute(veh['id'])[traci.vehicle.getRouteIndex(veh['id']):]}
        for veh in vehList]

    return routes


def anyActiveEV():
    """Checks if there are any emergency vehicles in the simulation."""
    vehs = getAllVehicleTypes()
    return any(veh['vehType'] in [ER, C_ER] for veh in vehs)


def getRouteIndex(vehId: str):
    """Returns the index of the current edge within the vehicles route or -1 if the
        vehicle has not yet departed

        Args:
            vehId (str): The ID of the vehicle to query.

        Returns:
            [int]: The index of the edge in the route.
    """
    return traci.vehicle.getRouteIndex(vehId)


def getPosAlongLane(vehId: str):
    """The position of the vehicle along the lane, measured in meters.

        Example:
            If route = [e1, e2, e3] and currentEdge = e2, then
            return index 1, as the current edge sits at index 1 in the route.

        Args:
            vehId (str): The ID of the vehicle to query.

        Returns:
            [double]: The distance from the start of the edge.
    """
    return traci.vehicle.getLanePosition(vehId)


def getCurrentEdge(vehId: str):
    """Returns the ID of the edge the vehicle is currently on.

        Args:
            vehId (str): The ID of the vehicle.

        Returns:
            [str]: The ID of the edge.
    """
    index = getRouteIndex(vehId)
    route = getRoute(vehId)
    return route[index]


def getRoute(vehId: str):
    """Returns the route of the vehicle.

        Args:
            vehId (str): The ID of the vehicle to query.

        Returns:
            [list(str)]: The list of edges that constitute a route.
    """
    return traci.vehicle.getRoute(vehId)


def nextStep():
    """Jumps to the next step in the simulation."""
    traci.simulationStep()


def getLaneLength(laneId: str):
    """Returns the length in meters.

        Args:
            laneId (str): The ID of the lane to query.

        Returns:
            [double]: The length of the lane.
    """
    return traci.lane.getLength(laneId)


def getLaneLength(laneId: str):
    """Returns the length in meters.

        Args:
            laneId (str): The ID of the lane to query.

        Returns:
            [double]: The length of the lane.
    """
    return traci.lane.getLength(laneId)


def getTime():
    """Returns the current simulation time in seconds.

        Returns:
            [double]: The current time.
    """
    return traci.simulation.getTime()


def getRemainingRoute(vehId: str):
    """Returns the remaining edges in the route from the vehicle's current edge onward.

        Args:
            vehId (str): The ID of the vehicle to query.

        Returns:
            [str]: The route.
    """
    route = getRoute(vehId)
    currentPos = getRouteIndex(vehId)
    return route[currentPos:]


def getLaneId(edgeId: str):
    """Returns the lane ID given a parent edge ID.

    Args:
        edgeId (str): The ID of the parent edge.

    Returns:
        [str]: The ID of the lane.
    """
    return edgeId + "_0"


def findRoute(fromEdge: str, toEdge: str):
    """Computes the fastest route between the given edges for the given vehicle.

        Args:
            fromEdge (str): The ID of the origin edge.
            toEdge (str): The ID of the destination edge.

        Returns:
            [str]: The route.
    """
    return traci.simulation.findRoute(fromEdge=fromEdge, toEdge=toEdge)


def setTravelTime(vehId: str, edgeId: str, time: float = 999.0, begTime: float = None, endTime: float = None):
    """Inserts the information about the travel time of edge "edgeID" valid
        from begin time to end time into the vehicle's internal edge weights
        container.
        If the time is not specified, any previously set values for that edge
        are removed.
        If begTime or endTime are not specified the value is set for the whole
        simulation duration.

        Args:
            vehId (str): The ID of the vehicle.
            edgeId (str): The ID of the edge.
            time (float): Current time. Defaults to 999.0.
            begTime (float, optional): The start of the time range. Defaults to None.
            endTime (float, optional): The end of the time range. Defaults to None.
    """
    traci.vehicle.setAdaptedTraveltime(
        vehId, edgeId, time, begTime=begTime, endTime=endTime)


def getCarCount():
    """Returns the number of all active vehicles and persons which are in the net plus the
        ones still waiting to start. Vehicles and persons currently stopped with a
        'trigger' are excluded from this number (if only triggered objects
        remain, the trigger condition cannot be fulfilled and all objects remain
        stopped without user intervention).
        The returned number may also be smaller than
        the actual number of vehicles still to come because of delayed
        route file parsing. If the number is 0 however, it is
        guaranteed that all route files have been parsed completely.

        Returns:
            [integer]: The number of active vehicles.
    """
    return traci.simulation.getMinExpectedNumber()


def getOriginalTravelTime(edgeId: str):
    """Returns the estimated travel time in seconds for the last time step on the given edge.

        Args:
            edgeId (str): The ID of the edge.

        Returns:
            [double]: The travel time.
    """
    return traci.edge.getTraveltime(edgeId)


def resetTravelTime(vehId: str):
    """Resets the adapted travel times for all edges on a vehicle.

        Args:
            vehId (str): The ID of the vehicle.
    """
    route = getRoute(vehId)
    for edgeId in route:
        travelSpeed = getOriginalTravelTime(edgeId)
        setTravelTime(vehId, edgeId, time=travelSpeed)
