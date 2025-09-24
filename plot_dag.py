# import matplotlib.pyplot as plt
import pydotplus
import plotly.graph_objects as go
import gravis as gv
import networkx as nx


graph = pydotplus.graph_from_dot_file("dag.dot")
nodes = graph.get_nodes()
edges = graph.get_edges()
print(f"Nodes: {len(nodes)}, Edges: {len(edges)}")
print("Node examples:")
for node in nodes[:5]:
    print(f" - {node.get_name()}: {node.get_label()}")  
print("Edge examples:")
for edge in edges[:5]:
    print(f" - {edge.get_source()} -> {edge.get_target()}")
    
fig = go.Figure()

for edge in edges:
    fig.add_trace(go.Scatter(
        x = [node.get_z() for node in nodes if node.get_name() == edge.get_source()],
        y = [node.get_y() for node in nodes if node.get_name() == edge.get_target()],
        mode = 'lines',
        line = dict(width=2, color='black')
    ))
fig.show()
