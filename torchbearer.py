"""
CS 460 – Algorithms: Final Programming Assignment
The Torchbearer

Student Name: Julio Nevarez
Student ID:   130817489

"""

import heapq


# =============================================================================
# PART 1
# =============================================================================

def explain_problem():

    answer = """
    **Why a single shortest-path run from S is not enough:**
        A single shortest path run like Dijkstras would not be enough because it only takes into consideration the total distance from a specific starting path, in our case S. But we need to be able to keep track of different starting distances from different nodes when we are mid pathing.
    **What decision remains after all inter-location costs are known:**
        We need to figure out what path/order to visit the relic chambers/nodes in.

    **Why this requires a search over orders (one sentence):**
        This requires a search over orders because we have to try and compare the cost of different routes to figure out which is more efficient.
    """

    return answer


# =============================================================================
# PART 2
# =============================================================================

def select_sources(spawn, relics, exit_node):
    # start with spawn as the first source
    sourceList = [spawn]
    
    # add each relic as a source since we need distances from each one
    for relic in relics:
        sourceList.append(relic)
    
    return sourceList



def run_dijkstra(graph, source):
    # set every node's distance to infinity since we haven't found a path to any of them yet
    pathCosts = {node: float('inf') for node in graph}
    
    # at the start we are at the source node, so the distance to it is 0
    pathCosts[source] = 0
    
    # initialize priority queue to holds (cost, node) pairs, starts with just the source at cost 0
    pq = [(0, source)]
    
    # declare a visitedSet to keep track of which nodes we've finalized the shortest path to
    visitedNodes = set()
    
    # while the priority queue is not empty, keep exexcuting the proces
    while pq:
        # always grab the cheapest node available from the queue
        currentCost, currentNode = heapq.heappop(pq)
        
        # if we already finalized this node we can skip it
        # this handles the case where a node gets added to the queue multiple times
        if currentNode in visitedNodes:
            continue
        
        # now we mark this node as finalized since we found the cheapest path to it
        visitedNodes.add(currentNode)
        
        # check all the neighbors of the current node
        for neighbor, weight in graph[currentNode]:
            # calculate what it would cost to reach this neighbor through the current node
            newCost = currentCost + weight
            
            # if this new path is cheaper than what we have recorded, update it
            if newCost < pathCosts[neighbor]:
                pathCosts[neighbor] = newCost
                # add the neighbor to the queue with its updated cost so we can explore it later
                heapq.heappush(pq, (newCost, neighbor))

                # process continues until we have finalized the shortest path to every reachable node, at which point the queue will be empty and we can return our results
    
    return pathCosts


def precompute_distances(graph, spawn, relics, exit_node):
    # first need to declare a list of the source nodes we need to run Dijkstra's from as well as a table to hold the distances computed
    sourceNodes = select_sources(spawn, relics, exit_node)
    distanceTable = {}

    # for loop to run Dijkstra's from each source node and fill the distance table with the results
    for source in sourceNodes:
        pathsFromSource = run_dijkstra(graph, source)   # variable to hold the result from Dijkstras for this source node
        distanceTable[source] = pathsFromSource         # store the distance from this source to every other node in the table for easy lookup later
    
    return distanceTable

    


# =============================================================================
# PART 3
# =============================================================================

def dijkstra_invariant_check():
    answer = """
    - **For nodes already finalized (in S):**
        When a node gets finalized we are done with it. The distance we have recorded for it is the real shortest path and nothing can make it shorter at this point.

    - **For nodes not yet finalized (not in S):**
        Nodes that havent been finalized yet have a distance that is just our best estimate so far. As we keep exploring we might find a cheaper way to reach them and update their distance.

    - **Initialization : why the invariant holds before iteration 1:**
        The only distance we know for sure is that the source is 0 steps away from itself. Everything else is infinity since we havent explored anything yet.

    - **Maintenance : why finalizing the min-dist node is always correct:**
        Given that our edge weights are all nonnegative there is no way to find a shorter path to it in the future. Any future path to this node would have to pass through nodes with equal or greater distance, so the current minimum cannot be beaten.

    - **Termination : what the invariant guarantees when the algorithm ends:**
        Every node that has a valid path has its correct shortest distance and any node still sitting at infinity just means there was no path to it from the source.

    If the invariant did not hold it would mean the precomputed distances are wrong, the route planner would make decisions based on incorrect costs and could end up picking a suboptimal or invalid route.
    """

    return answer


# =============================================================================
# PART 4
# =============================================================================

def explain_search():
    answer = """
    - **The failure mode:** The failure mode is that greedy commits to a locally cheap decision early on without looking ahead, which can force it into expensive choices later that a different ordering would have avoided.
    - **Counter-example setup:** Using the illustration example and tweaking it a tiny bit. If we change the cost of S→B to cost 3 and S→C to cost 1. Everything else stays the same. Now C looks like the obvious first pick from S but leads to trouble later.
    - **What greedy picks:** Greedy picks S→C(cost 1) first since it is the cheapest from S, then C→B(cost 1), then B→D(cost 1), then D→T(cost 100) for a total cost of 103.
    - **What optimal picks:** Optimal picks S→B→D→C→T costing 6 by avoiding ending on D which has an expensive exit to T of 100.
    - **Why greedy loses:** Greedy loses because it only looks at the immediate next cheapest step and has no way of knowing that picking C first would eventually force it to exit through D→T at cost 100.
    - The algorithm has to try every order of visiting the relics and keep track of which one ends up being the cheapest overall.
        """

    return answer


# =============================================================================
# PARTS 5 + 6
# =============================================================================

def find_optimal_route(dist_table, spawn, relics, exit_node):
    bestCost = float('inf')
    bestOrder = []
    best = [bestCost, bestOrder]
    
    # all relics need to be visited at least once, so we can start with a set of all the relics that we need to visit and remove them as we go
    relicsRemaining = set(relics)
    
    # call the helper function to explore all possible orders of visiting the relics and keep track of the best one found
    _explore(dist_table, spawn, relicsRemaining, [], 0, exit_node, best)
    
    # after exploring all possibilities, best should hold the cheapest cost and the order of relics that produces it
    return (best[0], best[1])


def _explore(dist_table, current_loc, relics_remaining, relics_visited_order,
             cost_so_far, exit_node, best):
    # set up local variables from README
    currentNode = current_loc
    relicsVisited = relics_visited_order
    fuelSpent = cost_so_far

    # We only prune when we have already spent more fuel than our best so far complete route. Since fuel costs are always nonnegative we can never get cheaper from here, so we are not throwing away anything we might need.
    if fuelSpent >= best[0]:
        return

    # base case first, if we have visited all the relics we just need to head to the exit and see if this route is better than our best so far
    if not relics_remaining:
        costToExit = dist_table[currentNode][exit_node]
        totalCost = fuelSpent + costToExit
        if totalCost < best[0]:
            best[0] = totalCost
            best[1] = list(relicsVisited)
        return

    # lower bound math to make our pruning more efficient
    minToNextRelic = min(dist_table[currentNode][r] for r in relics_remaining)
    # cheapest cost from any remaining relic to exit
    minToExit = min(dist_table[r][exit_node] for r in relics_remaining)
    lowerBound = minToNextRelic + minToExit

    # we should be prune even if the best possible outcome from here is just equal to our best so far
    if fuelSpent + lowerBound >= best[0]:
        return

    # try visiting each remaining relic
    for relic in list(relics_remaining):
        pathCost = dist_table[currentNode][relic]
        if pathCost == float('inf'):
            continue
        relics_remaining.remove(relic)
        relicsVisited.append(relic)
        _explore(dist_table, relic, relics_remaining, relicsVisited,
                 fuelSpent + pathCost, exit_node, best)
        relics_remaining.add(relic)
        relicsVisited.pop()

    # by this point we have tried visiting each remaining relic and explored all the routes that come from those choices, so we backtrack to let the caller try different options as well



# =============================================================================
# PIPELINE
# =============================================================================

def solve(graph, spawn, relics, exit_node):
    # first need to hold all the distances given from precomputing them from running dijkstras
    distanceTable = precompute_distances(graph, spawn, relics, exit_node)
    
    # then need to hold the optimal route
    optimalRoute = find_optimal_route(distanceTable, spawn, relics, exit_node)
    
    # edge case check to make sure we return the correct output if there is no valid route to the exit
    if optimalRoute[0] == float('inf'):
        return (float('inf'), [])
    
    return optimalRoute


# =============================================================================
# PROVIDED TESTS (do not modify)
# Graders will run additional tests beyond these.
# =============================================================================

def _run_tests():
    print("Running provided tests...")

    # Test 1: Spec illustration. Optimal cost = 4.
    graph_1 = {
        'S': [('B', 1), ('C', 2), ('D', 2)],
        'B': [('D', 1), ('T', 1)],
        'C': [('B', 1), ('T', 1)],
        'D': [('B', 1), ('C', 1)],
        'T': []
    }
    cost, order = solve(graph_1, 'S', ['B', 'C', 'D'], 'T')
    assert cost == 4, f"Test 1 FAILED: expected 4, got {cost}"
    print(f"  Test 1 passed  cost={cost}  order={order}")

    # Test 2: Single relic. Optimal cost = 5.
    graph_2 = {
        'S': [('R', 3)],
        'R': [('T', 2)],
        'T': []
    }
    cost, order = solve(graph_2, 'S', ['R'], 'T')
    assert cost == 5, f"Test 2 FAILED: expected 5, got {cost}"
    print(f"  Test 2 passed  cost={cost}  order={order}")

    # Test 3: No valid path to exit. Must return (inf, []).
    graph_3 = {
        'S': [('R', 1)],
        'R': [],
        'T': []
    }
    cost, order = solve(graph_3, 'S', ['R'], 'T')
    assert cost == float('inf'), f"Test 3 FAILED: expected inf, got {cost}"
    print(f"  Test 3 passed  cost={cost}")

    # Test 4: Relics reachable only through intermediate rooms.
    # Optimal cost = 6.
    graph_4 = {
        'S': [('X', 1)],
        'X': [('R1', 2), ('R2', 5)],
        'R1': [('Y', 1)],
        'Y': [('R2', 1)],
        'R2': [('T', 1)],
        'T': []
    }
    cost, order = solve(graph_4, 'S', ['R1', 'R2'], 'T')
    assert cost == 6, f"Test 4 FAILED: expected 6, got {cost}"
    print(f"  Test 4 passed  cost={cost}  order={order}")

    # Test 5: Explanation functions must return non-placeholder strings.
    for fn in [explain_problem, dijkstra_invariant_check, explain_search]:
        result = fn()
        assert isinstance(result, str) and result != "TODO" and len(result) > 20, \
            f"Test 5 FAILED: {fn.__name__} returned placeholder or empty string"
    print("  Test 5 passed  explanation functions are non-empty")

    print("\nAll provided tests passed.")


if __name__ == "__main__":
    _run_tests()
