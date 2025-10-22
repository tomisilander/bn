import networkx as nx

def bn2dg(bn):
    dg = nx.DiGraph()
    dg.add_nodes_from(bn.vars())
    dg.add_edges_from(bn.arcs())
    return dg

def is_dag(bn):
    dg = bn2dg(bn)
    return nx.is_directed_acyclic_graph(dg)

if __name__ == '__main__':
    import coliche
    from bn.bn import load
    def main(bnfile):
        print('DAG' if is_dag(load(bnfile, do_pic=False)) else 'not DAG')
    coliche.che(main, 'bnfile')
    
