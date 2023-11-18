from utils import TRACE, YES, NO, Rtpkt, tolayer2, clocktime

class DistanceTable:
    costs = [[0 for j in range(4)] for i in range(4)]

dt = DistanceTable()

# students to write the following two routines, and maybe some others

# modify this statement for different node
edges = [3, 1, 0, 2]
node_id = 2


def rtinit2():
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
    tolayer2(Rtpkt(node_id, 1, [dt.costs[x][1] for x in range(4)]))
    tolayer2(Rtpkt(node_id, 3, [dt.costs[x][3] for x in range(4)]))

    # Print initialization message
    print("rtinit2() called at time %f" % clocktime)
    printdt2(dt)


def rtupdate2(rcvdpkt):
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
        tolayer2(Rtpkt(node_id, 1, [dt.costs[x][1] for x in range(4)]))
        tolayer2(Rtpkt(node_id, 3, [dt.costs[x][3] for x in range(4)]))

    # Print update information
    print("rtupdate2() called at time %f" % clocktime)
    print("Packet received from node %d" % rcvdpkt.sourceid)
    printdt2(dt)


def printdt2(dtptr):
    print("                via     \n")
    print("   D2 |    0     1    3 \n")
    print("  ----|-----------------\n")
    print("     0|  %3d   %3d   %3d\n" %
          (dtptr.costs[0][0], dtptr.costs[0][1], dtptr.costs[0][3]))
    print("dest 1|  %3d   %3d   %3d\n" %
          (dtptr.costs[1][0], dtptr.costs[1][1], dtptr.costs[1][3]))
    print("     3|  %3d   %3d   %3d\n" %
          (dtptr.costs[3][0], dtptr.costs[3][1], dtptr.costs[3][3]))
