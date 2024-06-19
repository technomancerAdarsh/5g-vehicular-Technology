import traci
import time
import traci.constants as tc
import pytz
import datetime
from random import randrange
import pandas as pd

def getdatetime():
    utc_now = pytz.utc.localize(datetime.datetime.utcnow())
    currentDT = utc_now.astimezone(pytz.timezone("Asia/Singapore"))
    DATIME = currentDT.strftime("%Y-%m-%d %H:%M:%S")
    return DATIME

sumoCmd = ["sumo", "-c", "osm.sumocfg"]
traci.start(sumoCmd)

packBigData = []

while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()

    vehicles = traci.vehicle.getIDList()
    edges = traci.edge.getIDList()

    for veh_id in vehicles:
        x, y = traci.vehicle.getPosition(veh_id)
        coord = [x, y]
        lon, lat = traci.simulation.convertGeo(x, y)
        gps_coord = [lon, lat]
        spd = round(traci.vehicle.getSpeed(veh_id) * 3.6, 2)
        edge = traci.vehicle.getRoadID(veh_id)
        lane = traci.vehicle.getLaneID(veh_id)
        displacement = round(traci.vehicle.getDistance(veh_id), 2)
        turn_angle = round(traci.vehicle.getAngle(veh_id), 2)
        next_tls = traci.vehicle.getNextTLS(veh_id)

        # Additional parameters
        co = traci.vehicle.getParameter(veh_id, "emissionCO")
        co2 = traci.vehicle.getParameter(veh_id, "emissionCO2")
        electricity = traci.vehicle.getParameter(veh_id, "emissionElectricity")
        fuel = traci.vehicle.getParameter(veh_id, "emissionFuel")
        hc = traci.vehicle.getParameter(veh_id, "emissionHC")
        mean_friction = traci.vehicle.getParameter(veh_id, "meanFriction")
        nox = traci.vehicle.getParameter(veh_id, "emissionNOx")
        noise = traci.vehicle.getParameter(veh_id, "emissionNoise")
        pmx = traci.vehicle.getParameter(veh_id, "emissionPMx")
        pending_veh = traci.vehicle.getParameter(veh_id, "pendingVehicles")

        # Get the starting and ending node IDs associated with the edge
        edge_id = traci.vehicle.getRoadID(veh_id)

        # Get the starting and ending junction IDs associated with the edge
        start_node = traci.edge.getFromJunction(edge_id)
        end_node = traci.edge.getToJunction(edge_id)
        
        veh_list = [getdatetime(), veh_id, coord, gps_coord, spd, edge, lane, displacement, turn_angle, next_tls,
                    co, co2, electricity, fuel, hc, mean_friction, nox, noise, pmx, pending_veh, start_node, end_node]

        packBigData.append(veh_list)

    traci.simulationStep()

traci.close()

column_names = ['dateandtime', 'vehid', 'coord', 'gpscoord', 'spd', 'edge', 'lane', 'displacement', 'turnAngle', 'nextTLS',
                'co', 'co2', 'electricity', 'fuel', 'hc', 'meanFriction', 'nox', 'noise', 'pmx', 'pendingVeh', 'startNode', 'endNode']
dataset = pd.DataFrame(packBigData, index=None, columns=column_names)
with open("test.csv", "w") as file:
    dataset.to_csv(file, index=False)
