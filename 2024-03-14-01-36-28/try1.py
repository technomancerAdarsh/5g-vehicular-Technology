import traci
import time
import pytz
import datetime
import pandas as pd

def getdatetime():
    utc_now = pytz.utc.localize(datetime.datetime.utcnow())
    currentDT = utc_now.astimezone(pytz.timezone("Asia/Calcutta"))
    DATIME = currentDT.strftime("%Y-%m-%d %H:%M:%S")
    return DATIME

# Start SUMO
sumoCmd = ["sumo", "-c", "osm.sumocfg"]
traci.start(sumoCmd)

packBigData = []

while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()
    
    edges = traci.edge.getIDList()
    
    for edge_id in edges:
        start_node = traci.edge.getFromJunction(edge_id)
        end_node = traci.edge.getToJunction(edge_id)
        
        tlsList = [start_node, end_node]
        packBigData.append(tlsList)

traci.close()

# Generate Excel file
column_names = ['start_node', 'end_node']
dataset = pd.DataFrame(packBigData, columns=column_names)
dataset.to_excel("try.xlsx", index=False)
