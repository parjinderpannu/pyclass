'''Create a network diagram showing average ping time between hosts

   The diagram can be built with:
        python3 project_ping.py | dot -Tsvg >project_ping.svg

        On Windows, replace the dot command for its full path:
            "C:\Program Files (x86)\Graphviz2.38\bin\dot.exe"

   Links:
      http://interactive.blockdiag.com/graphviz/
      http://graphviz.org

   For extra credit, collect the data in a dictionary like:
        d[fromserver, toserver] = pingtime )
'''

#  Dot example
graph = """\
digraph {
    "localhost" -> "10.65.24.7" [label="31.23ms"];
    "localhost" -> "104.20.44.44" [label="24.68ms"];
}
"""

print(graph)
