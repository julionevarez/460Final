# Development Log – The Torchbearer

**Student Name:** Julio Nevarez
**Student ID:** 130817489
---

## Entry 1 – [5/10/2026]: Initial Plan

Going to start with the Dijkstra implementation first since I already have a good understanding of how it works from class, but for the most part I am just going to follow the given structure and work on the README planning first and then the actual code implementation for its respective part.

After looking over the assignment instructions the parts I am most worried about is the recursive search in Parts 5 and 6 as I still have trouble tracing through sometimes and keeping track of the logic when it gets a bit complex as well as the pruning.

I am planning to test as I go using the provided tests and work through the given example by hand to make sure my distances are correct before touching the search.

---

## Entry 2 – [5/11/2026]: Part 1 and 2 Check-in

Finished implementing Part 1 and 2. While I was going through the functions in torchbearer, I was confused at first as I saw exit_node as a parameter for select_sources and precompute_distances and was stuck on thinking where it plays a role in this/how to implement it and then realized that we don't need to do anything with it as its always just going to be an exit node, or in other words, a dead-end node with no path to take. 

---

## Entry 3 – [5/13/2026]: README DONE

Just finshed the README for the remaining parts, and I gotta say that I was kind of intimidated at the beginning when looking over the assignment and this being the final and all, but when the problem is layed out like this, and the specific questions that are being asked basically being a guide for us, it made it really easy to think through the problem logically which was really helpful. The pruning section took the most thought but I think I have a solid understanding of why it works now.

Now, onto the the hard part for me, the coding.

---

## Entry 4 – [5/13/2026]: Post-Implementation Reflection

Got everything working and all tests passing. Looking back I think the lower bound pruning could be improved. Right now it only estimates the minimum cost to the nearest relic and then to the exit, but i think a smarter way to go about the lower bound would be where is also accounts for all remaining relics, and this would mean it prunes more branches. The recursive search was definitely the hardest part like I expected, specifically making sure the backtracking was undoing the state correctly as I always get mixed up at times. Would also add more edge case testing given more time.

---

## Final Entry – [Date]: Time Estimate

| Part | Estimated Hours |
|---|---|
| Part 1: Problem Analysis | 1 hour |
| Part 2: Precomputation Design |1-2 hours |
| Part 3: Algorithm Correctness | 1-2 hours |
| Part 4: Search Design | 1 hour |
| Part 5: State and Search Space | 1 hour |
| Part 6: Pruning | 2ish hours |
| Part 7: Implementation | 4-6 hours |
| README and DEVLOG writing | 1 hour |
| **Total** | 11-12 hours |
