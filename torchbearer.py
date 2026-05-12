"""
CS 460 – Algorithms: Final Programming Assignment
The Torchbearer

Student Name: Julio Nevarez
Student ID:   130817489

INSTRUCTIONS
------------
- Implement every function marked TODO.
- Do not change any function signature.
- Do not remove or rename required functions.
- You may add helper functions.
- Variable names in your code must match what you define in README Part 5a.
- The pruning safety comment inside _explore() is graded. Do not skip it.

Submit this file as: torchbearer.py
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
    """
    Parameters
    ----------
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    list[node]
        No duplicates. Order does not matter.

    """
    # start with spawn as the first source
    sourceList = [spawn]
    
    # add each relic as a source since we need distances from each one
    for relic in relics:
        sourceList.append(relic)
    
    return sourceList



def run_dijkstra(graph, source):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
        graph[u] = [(v, cost), ...]. All costs are nonnegative integers.
    source : node

    Returns
    -------
    dict[node, float]
        Minimum cost from source to every node in graph.
        Unreachable nodes map to float('inf').

    """
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
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    dict[node, dict[node, float]]
        Nested structure supporting dist_table[u][v] lookups
        for every source u your design requires.

    
    """
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
    """
    Returns
    -------
    str
        Your Part 3 README answers, written as a string.
        Must match what you wrote in README Part 3.

    
    """

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
    """
    Returns
    -------
    str
        Your Part 4 README answers, written as a string.
        Must match what you wrote in README Part 4.

    TODO
    """
    return "TODO"


# =============================================================================
# PARTS 5 + 6
# =============================================================================

def find_optimal_route(dist_table, spawn, relics, exit_node):
    """
    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
        Output of precompute_distances.
    spawn : node
    relics : list[node]
        Every node in this list must be visited at least once.
    exit_node : node
        The route must end here.

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.

    TODO
    """
    pass


def _explore(dist_table, current_loc, relics_remaining, relics_visited_order,
             cost_so_far, exit_node, best):
    """
    Recursive helper for find_optimal_route.

    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
    current_loc : node
    relics_remaining : collection
        Your chosen data structure from README Part 5b.
    relics_visited_order : list[node]
    cost_so_far : float
    exit_node : node
    best : list
        Mutable container for the best solution found so far.

    Returns
    -------
    None
        Updates best in place.

    TODO
    Implement: base case, pruning, recursive case, backtracking.

    REQUIRED: Add a 1-2 sentence comment near your pruning condition
    explaining why it is safe (cannot skip the optimal solution).
    This comment is graded.
    """
    pass


# =============================================================================
# PIPELINE
# =============================================================================

def solve(graph, spawn, relics, exit_node):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.

    TODO
    """
    pass


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
