#!/usr/bin/env python3
import json
import os
import sys
import random
import numpy as np
from collections import defaultdict, Counter
from typing import Dict, List, Tuple, Any

# Add project root to path to import scripts
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
sys.path.append(project_dir)

# Import constants
from scripts.constants import (
    NUM_NODES,
    MAX_EDGES_PER_NODE,
    MAX_TOTAL_EDGES,
)


def load_graph(graph_file):
    """Load graph from a JSON file."""
    with open(graph_file, "r") as f:
        return json.load(f)


def load_results(results_file):
    """Load query results from a JSON file."""
    with open(results_file, "r") as f:
        return json.load(f)


def save_graph(graph, output_file):
    """Save graph to a JSON file."""
    with open(output_file, "w") as f:
        json.dump(graph, f, indent=2)


def verify_constraints(graph, max_edges_per_node, max_total_edges):
    """Verify that the graph meets all constraints."""
    # Check total edges
    total_edges = sum(len(edges) for edges in graph.values())
    if total_edges > max_total_edges:
        print(
            f"WARNING: Graph has {total_edges} edges, exceeding limit of {max_total_edges}"
        )
        return False

    # Check max edges per node
    max_node_edges = max(len(edges) for edges in graph.values())
    if max_node_edges > max_edges_per_node:
        print(
            f"WARNING: A node has {max_node_edges} edges, exceeding limit of {max_edges_per_node}"
        )
        return False

    # Check all nodes are present
    if len(graph) != NUM_NODES:
        print(f"WARNING: Graph has {len(graph)} nodes, should have {NUM_NODES}")
        return False

    # Check edge weights are valid (between 0 and 10)
    for node, edges in graph.items():
        for target, weight in edges.items():
            if weight <= 0 or weight > 10:
                print(f"WARNING: Edge {node} -> {target} has invalid weight {weight}")
                return False

    return True


def optimize_graph(
    initial_graph,
    results,
    num_nodes=NUM_NODES,
    max_total_edges=int(MAX_TOTAL_EDGES),
    max_edges_per_node=MAX_EDGES_PER_NODE,
):
    """
    Optimize the graph to improve random walk query performance.

    Args:
        initial_graph: Initial graph adjacency list
        results: Results from queries on the initial graph
        num_nodes: Number of nodes in the graph
        max_total_edges: Maximum total edges allowed
        max_edges_per_node: Maximum edges per node

    Returns:
        Optimized graph
    """
    print("Starting graph optimization...")

    # Create a copy of the initial graph to modify
    optimized_graph = {}
    for node, edges in initial_graph.items():
        optimized_graph[node] = dict(edges)

    # =============================================================
    # TODO: Implement your optimization strategy here
    # =============================================================
    #
    # Your goal is to optimize the graph structure to:
    # 1. Increase the success rate of queries
    # 2. Minimize the path length for successful queries
    #
    # You have access to:
    # - initial_graph: The current graph structure
    # - results: The results of running queries on the initial graph
    #
    # Query results contain:
    # - Each query's target node
    # - Whether the query was successful
    # - The path taken during the random walk
    #
    # Remember the constraints:
    # - max_total_edges: Maximum number of edges in the graph
    # - max_edges_per_node: Maximum edges per node
    # - All nodes must remain in the graph
    # - Edge weights must be positive and ≤ 10

    # # Simple Loop implementation
    # for node in optimized_graph:
    #     optimized_graph[node] = {str(int(node)+1):1}
    # optimized_graph["499"] = {"0":1}

    # Sorted loop implementation, with back edges
    # calculating the frequency of each query target
    freq_dict = {}
    for val in range(500):
        freq_dict[val] = 0
    for query in results["detailed_results"]:
        freq_dict[query["target"]] += 1

    # sorting by the found frequency
    sorted_list = [i for i in range(500)]
    sorted_list.sort(key = lambda x: -1 * freq_dict[x])

    # creating the chain and back edges
    p = 2 #paramater for scaling the weights of the back edges
    for i in range(len(sorted_list)):
        # creating the forward edge for the chain
        optimized_graph[str(sorted_list[i])] = {str((sorted_list[(i+1)%500])): 1}
        # creating the back edges
        if i!=0:
            optimized_graph[str(sorted_list[i])][str(sorted_list[0])] = i * p/500

    # # Tree implementation, with back edges
    # # calculating the frequency of each query target
    # freq_dict = {}
    # for val in range(500):
    #     freq_dict[val] = 0
    # for query in results["detailed_results"]:
    #     freq_dict[query["target"]] += 1
    # sorted_list = [i for i in range(500)]
    # sorted_list.sort(key = lambda x: -1 * freq_dict[x])
    #
    # # creating the tree and backprop
    # for i in range(len(sorted_list)):
    #
    #     # has children: propagate downwards
    #     if 2* i + 2 < len(sorted_list):
    #
    #         # fixing for 0s
    #         if freq_dict[2 * i + 1] == 0 or freq_dict[2 * i  + 2] == 0:
    #             optimized_graph[str(sorted_list[i])] = {
    #                 str(sorted_list[2 * i + 1]): freq_dict[2 * i + 1] + 1,
    #                 str(sorted_list[2 * i + 2]): freq_dict[2 * i + 2] + 1
    #             }
    #         else:
    #             optimized_graph[str(sorted_list[i])] = {
    #                 str(sorted_list[2 * i + 1]): freq_dict[2 * i + 1] / (freq_dict[2 * i + 1] + freq_dict[2 * i + 2]),
    #                 str(sorted_list[2 * i + 2]): freq_dict[2 * i + 2] / (freq_dict[2 * i + 1] + freq_dict[2 * i + 2])
    #             }
    #         if i!=0:
    #             optimized_graph[str(sorted_list[i])][str(sorted_list[0])] = i * 0.7 / 500
    #
    #     # leaf: backprop
    #     else:
    #         optimized_graph[str(sorted_list[i])] = {str(sorted_list[0]): 1}

    # =============================================================
    # End of your implementation
    # =============================================================

    # Verify constraints
    if not verify_constraints(optimized_graph, max_edges_per_node, max_total_edges):
        print("WARNING: Your optimized graph does not meet the constraints!")
        print("The evaluation script will reject it. Please fix the issues.")

    return optimized_graph


if __name__ == "__main__":
    # Get file paths
    initial_graph_file = os.path.join(project_dir, "data", "initial_graph.json")
    results_file = os.path.join(project_dir, "data", "initial_results.json")
    output_file = os.path.join(
        project_dir, "candidate_submission", "optimized_graph.json"
    )

    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    print(f"Loading initial graph from {initial_graph_file}")
    initial_graph = load_graph(initial_graph_file)

    print(f"Loading query results from {results_file}")
    results = load_results(results_file)

    print("Optimizing graph...")
    optimized_graph = optimize_graph(initial_graph, results)

    print(f"Saving optimized graph to {output_file}")
    save_graph(optimized_graph, output_file)

    print("Done! Optimized graph has been saved.")
