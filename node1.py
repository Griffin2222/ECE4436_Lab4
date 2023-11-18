from utils import TRACE, YES, NO, Rtpkt, tolayer2, clocktime

class DistanceTable:
    costs = [[0 for j in range(4)] for i in range(4)]

dt = DistanceTable()
connectcosts1 = [1,  0,  1, 999]

# students to write the following two routines, and maybe some others

# modify this statement for different node
edges = [1, 0, 1, 999]
node_id = 1


def rtinit1():
    global dt, edges, node_id

    # Initialize distance table
    for i in range(4):
        for j in range(4):
            dt.costs[i][j] = 999  # Initialize with infinity

    # Set direct costs to neighbors
    for i in range(4):
        dt.costs[i][i] = connectcosts1[i]

    # Send initial distance vector to neighbors
    tolayer2(Rtpkt(node_id, 0, [dt.costs[x][0] for x in range(4)]))
    tolayer2(Rtpkt(node_id, 2, [dt.costs[x][2] for x in range(4)]))

    # Print initialization message
    print("rtinit1() called at time %f" % clocktime)
    printdt1(dt)


def rtupdate1(rcvdpkt):
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
    print("rtupdate1() called at time %f" % clocktime)
    print("Packet received from node %d" % rcvdpkt.sourceid)
    printdt1(dt)


def printdt1(dtptr):
    print("             via   \n")
    print("   D1 |    0     2 \n")
    print("  ----|-----------\n")
    print("     0|  %3d   %3d\n" % (dtptr.costs[0][0], dtptr.costs[0][2]))
    print("dest 2|  %3d   %3d\n" % (dtptr.costs[2][0], dtptr.costs[2][2]))
    print("     3|  %3d   %3d\n" % (dtptr.costs[3][0], dtptr.costs[3][2]))


def linkhandler1(linkid, newcost):
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
        tolayer2(Rtpkt(node_id, 0, [dt.costs[x][0] for x in range(4)]))
        tolayer2(Rtpkt(node_id, 2, [dt.costs[x][2] for x in range(4)]))

    # Print link cost change information
    print("Link cost change for link %d to %d at time %f" % (node_id, linkid, clocktime))
    print("New cost: %d" % newcost)
    printdt1(dt)
