from utils import TRACE, YES, NO, Rtpkt, tolayer2, clocktime

class DistanceTable:
    costs = [[0 for j in range(4)] for i in range(4)]

dt = DistanceTable()

# students to write the following two routines, and maybe some others

# modify this statement for different node
edges = [7, 999, 2, 0]
node_id = 3


def rtinit3():
    global dt, edges, node_id

    # Initialize distance table
    for i in range(4):
        for j in range(4):
            dt.costs[i][j] = 999  # Initialize with infinity

    # Set direct costs to neighbors
    for i in range(4):
        dt.costs[i][i] = edges[i]

    # Send initial distance vector to neighbors
    tolayer2(Rtpkt(node_id, 0, [dt.costs[x][0] for x in range(4)]))
    tolayer2(Rtpkt(node_id, 2, [dt.costs[x][2] for x in range(4)]))

    # Print initialization message
    print("rtinit3() called at time %f" % clocktime)
    printdt3(dt)


def rtupdate3(rcvdpkt):
    global dt, edges, node_id

    # Update distance table based on received packet
    change = False
    for i in range(4):
        if rcvdpkt.mincost[i] + edges[rcvdpkt.sourceid] < dt.costs[i][rcvdpkt.sourceid]:
            dt.costs[i][rcvdpkt.sourceid] = rcvdpkt.mincost[i] + edges[rcvdpkt.sourceid]
            change = True

    # If there was a change, send updated distance vector to neighbors
    if change:
        tolayer2(Rtpkt(node_id, 0, [dt.costs[x][0] for x in range(4)]))
        tolayer2(Rtpkt(node_id, 2, [dt.costs[x][2] for x in range(4)]))

    # Print update information
    print("rtupdate3() called at time %f" % clocktime)
    print("Packet received from node %d" % rcvdpkt.sourceid)
    printdt3(dt)


def printdt3(dtptr):
    print("             via     \n")
    print("   D3 |    0     2 \n")
    print("  ----|-----------\n")
    print("     0|  %3d   %3d\n" % (dtptr.costs[0][0], dtptr.costs[0][2]))
    print("dest 1|  %3d   %3d\n" % (dtptr.costs[1][0], dtptr.costs[1][2]))
    print("     2|  %3d   %3d\n" % (dtptr.costs[2][0], dtptr.costs[2][2]))
