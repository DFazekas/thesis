#!/usr/bin/env python3

import os
import sys


# We need to import some python modules from the $SUMO_HOME/tools directory.
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit('Please declare environment variable: "SUMO_HOME"')

import traci
from constants import *
from simulation import *


def getEstimatedRouteTime(vehId):
    print("getEstimatedRouteTime()")

    route = traci.vehicle.getRoute(vehId)

    # An index that represents which edge along their route the vehicle is currently on.
    currentEdgeIndex = traci.vehicle.getRouteIndex(vehId)
    currentEdgeId = route[currentEdgeIndex]
    currentLaneId = getLaneId(currentEdgeId)

    estimatedTravelTimes = []

    # Calculate the estimated travel times for the edge that the vehicle is currently on.
    estimatedTravelTimes.append({
        'id': currentEdgeId,
        'minTravelTime': computeMinTravelTime(currentLaneId, vehId),
        'projectedTravelTime': computeProjectedTravelTime(currentLaneId, vehId)
    })

    # Calculates the estimated travel times for upcoming edges,
    # not the one the vehicle is currently on.
    for edgeId in route[currentEdgeIndex + 1:]:
        laneId = getLaneId(edgeId)

        # The minimum time any vehicle could traverse this edge.
        minTravelTime = computeMinTravelTime(laneId, vehId)

        # The projected travel time based on the vehicle's current speed.
        projectedTravelTime = computeProjectedTravelTime(laneId, vehId)

        estimatedTravelTimes.append({
            'id': edgeId,
            'minTravelTime': minTravelTime,
            'projectedTravelTime': projectedTravelTime
        })

    print("Estimated travel times:")
    print(estimatedTravelTimes)


def computeMinTravelTime(distance: float or None, laneId: str, vehId: str):
    """Computes the minimum travel time for a given vehicle over a given
        lane, assuming constant velocity.

        Args:
            laneId (str): The ID of the lane.
            vehId (str): The ID of the vehicle.

        Returns:
            [float]: The estimated travel time.
    """
    distance = getLaneLength(laneId) if distance == None else distance
    maxSpeed = traci.lane.getMaxSpeed(laneId)
    speedFactor = traci.vehicle.getSpeedFactor(vehId)
    travelTime = distance / (maxSpeed * speedFactor)
    return travelTime


def computeProjectedArrivalTime(laneId, vehId, previousTime):
    projectedTravelTime = computeProjectedTravelTime(laneId, vehId)
    result = previousTime + projectedTravelTime
    print("\t\tPrevious time (%f) + projectedTravelTime (%f) = %f" %
          (previousTime, projectedTravelTime, result))
    return result


def computeMinArrivalTime(laneId, vehId, previousTime):
    minTravelTime = computeMinTravelTime(laneId, vehId)
    result = previousTime + minTravelTime
    print("\t\tPrevious time (%f) + minTravelTime (%f) = %f" %
          (previousTime, minTravelTime, result))
    return result


def getArrivalTimes(vehId: str):
    """Estimates the time at which the vehicle will arrive at each edge
        along their route.

        Args:
            vehId (str): The ID of the vehicle to query.
    """
    print("\n-------------------\n\nExtracting arrival times:\n\n")
    edgeArrivalTimes = {}

    remainingRoute = getRemainingRoute(vehId)

    # An index that represents which edge along their route the vehicle is currently on.
    currentEdgeId = getCurrentEdge(vehId)
    currentLaneId = getLaneId(currentEdgeId)
    print(f'\tVehicle ( {vehId} )\n \
        \t\tCurrent edge ( {currentEdgeId} )\n \
        \t\tRoute: {getRoute(vehId)}\n \
        \t\tRemaining route: {remainingRoute}')

    # The vehicle may be midway through an edge, so using the edge's full length would be inaccurate.
    # Take the difference of the vehicle's current position to the length of the edge its on.
    currentEdgeLength = getLaneLength(currentLaneId)
    distanceAlongCurrentEdge = getPosAlongLane(vehId)
    partialDistance = currentEdgeLength - distanceAlongCurrentEdge
    currentTime = getTime()

    sumMinTravelTime = 0
    sumProjectedTravelTime = 0
    for (index, edgeId) in enumerate(remainingRoute):
        # Only use the partial distance for the edge the vehicle is currently on.
        if index != 0:
            partialDistance = None

        laneId = getLaneId(edgeId)

        # Travel times
        minTravelTime = computeMinTravelTime(
            distance=partialDistance, laneId=laneId, vehId=vehId)
        projectedTravelTime = computeProjectedTravelTime(
            distance=partialDistance, laneId=laneId, vehId=vehId)

        # Arrival times
        minArrivalTime = currentTime + sumMinTravelTime + minTravelTime
        projectedArrivalTime = currentTime + \
            sumProjectedTravelTime + projectedTravelTime

        # Record the arrival times.
        edgeArrivalTimes[edgeId] = {
            "minTravelTime": minTravelTime,
            "projectedTravelTime": projectedTravelTime,
            "minArrivalTime": minArrivalTime,
            "projectedArrivalTime": projectedArrivalTime
        }

        # Track the cumulative travel time.
        sumMinTravelTime += minTravelTime
        sumProjectedTravelTime += projectedTravelTime

    print("Arrival Times:\n\n", edgeArrivalTimes)
    return edgeArrivalTimes


def computeProjectedTravelTime(distance: float, laneId: str, vehId: str):
    """Computes the projected travel time for a given vehicle over a given
        lane, assuming constant velocity.

        Args:
            laneId (str): The ID of the lane.
            vehId (tr): The ID of the vehicle.

        Returns:
            [float]: The estimated projected travel time.
    """
    distance = traci.lane.getLength(laneId) if distance is None else distance
    currentSpeed = traci.vehicle.getSpeed(vehId)
    travelTime = 999 if currentSpeed == 0 else distance / currentSpeed
    return travelTime


def findOverlappingRoutes():
    """Generates a list of (civilian, ER) pairs with overlapping edges in their routes.

        Returns:
            [list({})]: The conflicting vehicle pairs.
    """
    # Get all the relevant vehicles.
    emergVehs = getEVs()
    civilianVehs = getConnCivilians()

    # Get all the routes from the relevent vehicles.
    emergRoutes = getMultipleRoutes(emergVehs)
    connCivilRoutes = getMultipleRoutes(civilianVehs)

    # Generate pairs of civilians and EVs whose routes overlap.
    print(f"\nLooking for conflicting routes @ Time (T+{getTime()}):")
    print(f"\nShow all current routes:\n")
    overlappingRoutes = []

    # Go through all the connected civilian vehicles.
    for civilianVehicle in connCivilRoutes:
        civVehId = civilianVehicle['veh']['id']
        civEdgeIndex = civilianVehicle['currentIndex']
        civRoute = civilianVehicle['route']
        civRemainingRoute = getRemainingRoute(civVehId)
        print(f"\tCivilian ({civVehId})\n \
            \t\tRoute: {civRoute}\n \
            \t\tCurrent edge index: {civEdgeIndex}\n \
            \t\tEdge length: {getLaneLength(getLaneId(civRoute[civEdgeIndex]))}\n \
            \t\tCurrent pos: {getPosAlongLane(civVehId)}\n \
            \t\tUpcoming edges: {getRemainingRoute(civVehId)}")

        # Go through all the EVs.
        for emergencyVeh in emergRoutes:
            emergVehId = emergencyVeh['veh']['id']
            emergEdgeIndex = emergencyVeh['currentIndex']
            emergRoute = emergencyVeh['route']
            emergRemainingRoute = getRemainingRoute(emergVehId)

            # If any edge in the civilian's route matches an edge
            # in the ER's route, this could be a possible conflict.
            if any(civEdge in emergRemainingRoute for civEdge in civRemainingRoute):
                print("\tCONFLICTING ER (", emergVehId, ")\n \
                    \tRoute: ", emergRoute, "\n \
                    \tCurrent edge index:", emergEdgeIndex, "\n \
                    \tEdge length:", getLaneLength(getLaneId(emergRoute[emergEdgeIndex])), "\n \
                    \tCurrent pos:", getPosAlongLane(emergVehId), "\n \
                    \tUpcoming edges:", getRemainingRoute(emergVehId))

                overlappingRoutes.append(
                    {
                        'civilian': civVehId,
                        'ER': emergVehId
                    }
                )
                break

    print("\n\tConflicting routes:\n\t\t", overlappingRoutes)
    return overlappingRoutes


def findArrivalTimeConflicts(civArrivalTimes, emergArrivalTimes):
    print("\nFinding arrival time conflicts:\n\n")
    edgesToResolves = []

    for edgeId in civArrivalTimes:
        print(f"EdgeId: ( {edgeId} )")
        print(f"ER Arrival times: {emergArrivalTimes}")
        if emergArrivalTimes.get(edgeId) != None:
            # A negative delta means the ER arrives first; the civilian is behind the ER.
            absDeltaMinArrivalTime = abs(emergArrivalTimes[edgeId]['minTravelTime'] -
                                         civArrivalTimes[edgeId]['minTravelTime'])

            if absDeltaMinArrivalTime <= SAFETY_TIME_HEADWAY:
                print(
                    f"\n\nTOO CLOSE!\n\t\tDelta arrival at ({edgeId}) = ({absDeltaMinArrivalTime})\n")
                edgesToResolves.append(edgeId)
    return edgesToResolves
