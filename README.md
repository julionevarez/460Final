# The Torchbearer

**Student Name:** Julio Nevarez
**Student ID:** 130817489
**Course:** CS 460 – Algorithms | Spring 2026

> This README is your project documentation. Write it the way a developer would document
> their design decisions , bullet points, brief justifications, and concrete examples where
> required. You are not writing an essay. You are explaining what you built and why you built
> it that way. Delete all blockquotes like this one before submitting.

---

## Part 1: Problem Analysis

> Document why this problem is not just a shortest-path problem. Three bullet points, one
> per question. Each bullet should be 1-2 sentences max.

- **Why a single shortest-path run from S is not enough:**
  A single shortest path run like Dijkstras would not be enough because it only takes into consideration the total distance from a specific starting path, in our case S. But we need to be able to keep track of different starting distances from different nodes when we are mid pathing.
- **What decision remains after all inter-location costs are known:**
  We need to figure out what path/order to visit the relic chambers/nodes in.

- **Why this requires a search over orders (one sentence):**
  This requires a search over orders because we have to try and compare the cost of different routes to figure out which is more efficient.

---

## Part 2: Precomputation Design

### Part 2a: Source Selection

> List the source node types as a bullet list. For each, one-line reason.

| Source Node Type | Why it is a source |
|-------------------|-------------------------------------------------------------------------|
| Entrance/Spawn Node 'S' | We always begin at S so we need the cost of getting from S to any relic. |
| Relic Node 'm' | Once we collect a relic we need to know the cheapest way to reach the next one from that location. |

### Part 2b: Distance Storage

> Fill in the table. No prose required.

| Property | Your answer |
|----------|-------------|
| Data structure name | Nested Dictionary/Dictionary of dictonaries |
| What the keys represent | The starting node that we are running Dijkstras from |
| What the values represent | Another dictionary of all the shortest distances from that source node to all other nodes|
| Lookup time complexity | O(1) since we are just looking up a key in a dictionary |
| Why O(1) lookup is possible | Because dictionaries are hash tables and whether searching, adding or deleting items, these all average O(1) |

### Part 2c: Precomputation Complexity

> State the total complexity and show the arithmetic. Two to three lines max.

- **Number of Dijkstra runs:** Spawn = 1 run + each k relic to visit. k + 1 runs  
- **Cost per run:** O(m log n) per run where m is edges and n is nodes
- **Total complexity:** O(kmlog n) since we run dijkstra k + 1 times and each run costs O(mlog n)
- **Justification (one line):** We run dijkstra once per source node and each run touches every edge once through the priority queue

---

## Part 3: Algorithm Correctness

> Document your understanding of why Dijkstra produces correct distances.
> Bullet points and short sentences throughout. No paragraphs.

### Part 3a: What the Invariant Means

> Two bullets: one for finalized nodes, one for non-finalized nodes.
> Do not copy the invariant text from the spec.

- **For nodes already finalized (in S):**
  When a node gets finalized we are done with it. The distance we have recorded for it is the real shortest path and nothing can make it shorter at this point.

- **For nodes not yet finalized (not in S):**
  Nodes that havent been finalized yet have a distance that is just our best estimate so far. As we keep exploring we might find a cheaper way to reach them and update their distance.

### Part 3b: Why Each Phase Holds

> One to two bullets per phase. Maintenance must mention nonnegative edge weights.

- **Initialization : why the invariant holds before iteration 1:**
  The only distance we know for sure is that the source is 0 steps away from itself. Everything else is infinity since we havent explored anything yet.

- **Maintenance : why finalizing the min-dist node is always correct:**
  Given that our edge weights are all nonnegative there is no way to find a shorter path to it in the future.
  
  Any future path to this node would have to pass through nodes with equal or greater distance, so the current minimum cannot be beaten.

- **Termination : what the invariant guarantees when the algorithm ends:**
  Every node that has a valid path has its correct shortest distance and any node still sitting at infinity just means there was no path to it from the source.

### Part 3c: Why This Matters for the Route Planner

> One sentence connecting correct distances to correct routing decisions.

  If the invariant did not hold it would mean the precomputed distances are wrong, the route planner would make decisions based on incorrect costs and could end up picking a suboptimal or invalid route.

---

## Part 4: Search Design

### Why Greedy Fails

> State the failure mode. Then give a concrete counter-example using specific node names
> or costs (you may use the illustration example from the spec). Three to five bullets.

- **The failure mode:** _Your answer here._
- **Counter-example setup:** _Your answer here._
- **What greedy picks:** _Your answer here._
- **What optimal picks:** _Your answer here._
- **Why greedy loses:** _Your answer here._

### What the Algorithm Must Explore

> One bullet. Must use the word "order."

- _Your answer here._

---

## Part 5: State and Search Space

### Part 5a: State Representation

> Document the three components of your search state as a table.
> Variable names here must match exactly what you use in torchbearer.py.

| Component | Variable name in code | Data type | Description |
|---|---|---|---|
| Current location | | | |
| Relics already collected | | | |
| Fuel cost so far | | | |

### Part 5b: Data Structure for Visited Relics

> Fill in the table.

| Property | Your answer |
|----------|--------------|
| Data structure chosen | |
| Operation: check if relic already collected | Time complexity: |
| Operation: mark a relic as collected | Time complexity: |
| Operation: unmark a relic (backtrack) | Time complexity: |
| Why this structure fits | |

### Part 5c: Worst-Case Search Space

> Two bullets.

- **Worst-case number of orders considered:** _Your answer (in terms of k)._
- **Why:** _One-line justification._

---

## Part 6: Pruning

### Part 6a: Best-So-Far Tracking

> Three bullets.

- **What is tracked:** _Your answer here._
- **When it is used:** _Your answer here._
- **What it allows the algorithm to skip:** _Your answer here._

### Part 6b: Lower Bound Estimation

> Three bullets.

- **What information is available at the current state:** _Your answer here._
- **What the lower bound accounts for:** _Your answer here._
- **Why it never overestimates:** _Your answer here._

### Part 6c: Pruning Correctness

> One to two bullets. Explain why pruning is safe.

- _Your answer here._

---

## References

> Bullet list. If none beyond lecture notes, write that.

- _Your references here._
