
## Solution

### Approach & Analysis

[Describe how you analyzed the query patterns and what insights you found]

Since we know that the queries are from a standard distribution, we are trying to estimate this distribution to more accurately point into likely query nodes. Statistically, we will approach the distribution by simply counting the samples. We can act on this by recording the number of queries to each node and assuming that this is the distribution. Over time, this approximation will become better and better.

Like we expected from the prompt, the distribution seems almost exponential, so we will prioritize visiting likely nodes.

### Optimization Strategy

[Explain your optimization strategy in detail]

Generally, the optimization strategy is to point into nodes more likely to be queried, and point outwards from that node to other likely nodes. This takes the form of a chain, where we will connect each of the nodes in probability order (with the most likely at the start and least likely at the end). We will also have back edges from every node to the most probable node; this is how we will point into nodes more likely to be queried. Notice that the further down the chain we are, the less likely we are to find our query there, so we should have a higher chance of coming back to the starting node, corresponding to a higher weight on the back edge.

### Implementation Details

[Describe the key aspects of your implementation]

First, we have to analyze the queries. We use a dictionary to count how many times each node was queried. This will be our inferred distribution on the queries. Note that many nodes will not be queried at all, meaning they probably have a low frequency of being queried, however we still need to make it possible to find these nodes (with an appropriately low probability).

After we have our distribution, we will sort them by most likely to be queried (with our current information), and rank them in this order. We use an edge to connect each node to the its next ranked neighbor, and the lowest ranked node will be looped back to the highest rank node. Then, we use back edges to connect each node to the highest ranked node, scaling up its rank the lower we go.

### Results

[Share the performance metrics of your solution]

The success rate was always 100%. I never viewed it get any lower, but I can see in extreme cases in lots of queries that it may fail. In general, the median length reached 8 to 11, depending on the weight of the back edges. Typically, stronger back edges worked better (to an extent), as the distribution is quite skewed, and it is likely we want to head back to the first node as quickly as possible. Getting down to a median of 8 edges per path got combined scores of around 520 to 530, even reaching 541.88.

### Trade-offs & Limitations

[Discuss any trade-offs or limitations of your approach]

The chain approach is quite good for optimizing for median path length: our median outcome is still quite common (because of an exponential's right skew), so we can find it without too much problem. However, the mean should be worse: many nodes with low probability are quite hard to get to. I think in this case, the tree might be better, as we have many chances to get to a low probability node, each chance with relatively low path length. We also have that if our exponential distribution is quite flat, we prioritize the most probable nodes too much: in this case, it would have been better to not have back edges and our median outcome gets quite large.

### Iteration Journey

[Briefly describe your iteration process - what approaches you tried, what you learned, and how your solution evolved]

My immediate intuition was to create a star node, which would be the most likely, and then point to every other node with its probability of being the query.
This is clearly not allowed by the max edge per node, but led me to considering balanced binary trees, which will give you a good chance for a relatively small path length.
This inspired the idea of using back edges, as we would really like to start at the top, most probable node, so if we reach the bottom, we should head back to the top via a back edge to retry.

My second immediate intuition was to simply create a chain, ordered in probability order, hopefully starting at the most probable. We deterministically go down the line to find our node (and loop back if necessary).
Since we start at a random place however, this is an expected N/2 steps, which is somewhat long.

While reading through the README file, I noticed the tip "Both success rate and path length matter, but they often trade off". This seemed to match what I had seen: a tree is less probable to find our queried node, but should give you a short path in each try, while a chain is guaranteed to find our queried node but may have to go down a long path.

Combining ideas from the previous intuitions yielded chains with back edges: like trees, we really want to start at the most probable node, so we should use a back edge to get there: and we should go back to the most probable node with higher probability the further we are away: we want to prioritize going back, and we are unlikely to find the queried node near the end.

This also led to the idea of a tree that had more back edges more often, and with higher probability the lower we went down the tree, but I couldn't get it to be better than the chain.

I spent more than two hours total, but I had finished my best graph optimization (the chain with back edges) by the two hour mark. The rest of the time was trying to get the trees to work well.
---

* Be concise but thorough - aim for 500-1000 words total
* Include specific data and metrics where relevant
* Explain your reasoning, not just what you did
