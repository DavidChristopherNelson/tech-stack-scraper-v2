import json
import networkx as nx
import plotly.graph_objs as go
import community as community_louvain  # For community detection
import itertools

# Load your data
with open('extracted_job_data.txt', 'r') as f:
    data = json.load(f)

# Initialize an undirected graph
G_full = nx.Graph()

# Build the full graph
for job in data.values():
    tech_stack = job.get('tech_stack', [])
    # Standardize technology names
    tech_stack = [tech.strip().lower() for tech in tech_stack]
    # Add edges between all pairs of technologies in the same company
    for tech1, tech2 in itertools.combinations(set(tech_stack), 2):
        if G_full.has_edge(tech1, tech2):
            G_full[tech1][tech2]['weight'] += 1
        else:
            G_full.add_edge(tech1, tech2, weight=1)

# Calculate centrality measures on the full graph
degree_centrality_full = nx.degree_centrality(G_full)
betweenness_centrality_full = nx.betweenness_centrality(G_full)

# Print out node list with centrality measures
print("Node List with Centrality Measures:")
print("{:<50} {:<20} {:<20}".format("Technology", "Degree Centrality", "Betweenness Centrality"))
for node in G_full.nodes():
    print("{:<20} {:<20.4f} {:<20.4f}".format(
        node.title(),
        degree_centrality_full[node],
        betweenness_centrality_full[node]
    ))

# Parameters to adjust
N = 200  # Number of nodes to include after filtering
remove_top = False  # Set to True to remove most important nodes
M = 50    # Number of top nodes to remove if remove_top is True

# Remove the least or most important nodes based on degree centrality
sorted_nodes = sorted(degree_centrality_full.items(), key=lambda x: x[1], reverse=True)

if remove_top:
    # Remove top M nodes
    nodes_to_remove = [node for node, centrality in sorted_nodes[:M]]
else:
    # Remove bottom M nodes
    nodes_to_remove = [node for node, centrality in sorted_nodes[-M:]]

# Create a filtered graph
G = G_full.copy()
G.remove_nodes_from(nodes_to_remove)

# Further limit the number of nodes to N
degree_centrality = nx.degree_centrality(G)
top_nodes = dict(sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:N])
G = G.subgraph(top_nodes.keys()).copy()

# Recalculate centrality measures and community detection on the filtered graph
degree_centrality = nx.degree_centrality(G)
betweenness_centrality = nx.betweenness_centrality(G)
partition = community_louvain.best_partition(G)

# Generate six plots with different k values
k_values = [0.001, 0.005, 0.01, 0.03, 0.05, 0.1]
figures = []

for idx, k in enumerate(k_values):
    # Positions for all nodes
    pos = nx.spring_layout(G, k=k, seed=42)

    # Create edge traces
    edge_x = []
    edge_y = []

    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines'
    )

    # Create node traces
    node_x = []
    node_y = []
    node_text = []
    node_color = []
    node_size = []

    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_color.append(partition[node])
        size = degree_centrality[node] * 100  # Adjust the multiplier as needed
        node_size.append(size)
        node_info = f"{node.title()}<br>Degree Centrality: {degree_centrality[node]:.4f}"
        node_text.append(node_info)

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        text=node_text,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='Rainbow',
            reversescale=False,
            color=node_color,
            size=node_size,
            colorbar=dict(
                thickness=15,
                title='Community',
                xanchor='left',
                titleside='right'
            ),
            line_width=2)
    )

    # Create the figure for this k value
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title=f'Technology Co-occurrence Network (k={k})',
                        titlefont_size=16,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        annotations=[dict(
                            text="",
                            showarrow=False,
                            xref="paper", yref="paper")],
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))
    figures.append(fig)

# Display the figures
for fig in figures:
    fig.show()
