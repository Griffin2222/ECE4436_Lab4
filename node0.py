from utils import TRACE, YES, NO, Rtpkt, tolayer2, clocktime

class DistanceTable:
    costs = [[0 for j in range(4)] for i in range(4)]

dt = DistanceTable()

# modify this statement for different node
edges = [0, 1, 3, 7]
node_id = 0


def rtinit0():
    global dt, edges, node_id

    # Initialize distance table
    for i in range(4):
        for j in range(4):
            dt.costs[i][j] = 999  # Initialize with infinity

    # Set direct costs to neighbors
    dt.costs[1][1] = edges[1]
    dt.costs[2][2] = edges[2]
    dt.costs[3][3] = edges[3]

    # Send initial distance vector to neighbors
    tolayer2(Rtpkt(node_id, 1, [dt.costs[x][1] for x in range(4)]))
    tolayer2(Rtpkt(node_id, 2, [dt.costs[x][2] for x in range(4)]))
    tolayer2(Rtpkt(node_id, 3, [dt.costs[x][3] for x in range(4)]))

    # Print initialization message
    print("rtinit0() called at time %f" % clocktime)
    printdt0(dt)


def rtupdate0(rcvdpkt):
    global dt, edges, node_id

    # Update distance table based on received packet
    change = False
    for i in range(4):
        if rcvdpkt.mincost[i] + edges[rcvdpkt.sourceid] < dt.costs[i][rcvdpkt.sourceid]:
            dt.costs[i][rcvdpkt.sourceid] = rcvdpkt.mincost[i] + edges[rcvdpkt.sourceid]
            change = True

    # If there was a change, send updated distance vector to neighbors
    if change:
        tolayer2(Rtpkt(node_id, 1, [dt.costs[x][1] for x in range(4)]))
        tolayer2(Rtpkt(node_id, 2, [dt.costs[x][2] for x in range(4)]))
        tolayer2(Rtpkt(node_id, 3, [dt.costs[x][3] for x in range(4)]))

    # Print update information
    print("rtupdate0() called at time %f" % clocktime)
    print("Packet received from node %d" % rcvdpkt.sourceid)
    printdt0(dt)


def printdt0(dtptr):
    print("                via     \n")
    print("   D0 |    1     2    3 \n")
    print("  ----|-----------------\n")
    print("     1|  %3d   %3d   %3d\n" %
          (dtptr.costs[1][1], dtptr.costs[1][2], dtptr.costs[1][3]))
    print("dest 2|  %3d   %3d   %3d\n" %
          (dtptr.costs[2][1], dtptr.costs[2][2], dtptr.costs[2][3]))
    print("     3|  %3d   %3d   %3d\n" %
          (dtptr.costs[3][1], dtptr.costs[3][2], dtptr.costs[3][3]))


def linkhandler0(linkid, newcost):
    global dt, edges, node_id, clocktime

    # Update the cost in the distance table
    old_cost = edges[linkid]
    edges[linkid] = newcost

    # Update distance table entries affected by the link cost change
    for i in range(4):
        if i != linkid and dt.costs[i][linkid] == old_cost:
            dt.costs[i][linkid] = newcost

    # Check if the minimum cost to any node has changed
    min_cost_change = False
    for i in range(4):
        if i != node_id and dt.costs[i][linkid] + edges[linkid] < dt.costs[i][node_id]:
            dt.costs[i][node_id] = dt.costs[i][linkid] + edges[linkid]
            min_cost_change = True

    # If there was a change in minimum cost, send updated distance vector to neighbors
    if min_cost_change:
        tolayer2(Rtpkt(node_id, 1, [dt.costs[x][1] for x in range(4)]))
        tolayer2(Rtpkt(node_id, 2, [dt.costs[x][2] for x in range(4)]))
        tolayer2(Rtpkt(node_id, 3, [dt.costs[x][3] for x in range(4)]))

    # Print link cost change information
    print("Link cost change for link %d to %d at time %f" % (node_id, linkid, clocktime))
    print("New cost: %d" % newcost)
    printdt0(dt)

