import string

# DEFINE_NODES function
#create the array
#use networkx classes
import networkx
from networkx import *
import networkx.cliques
import networkx.threshold


#####SUBROUTINES######################################################
#find key of a given value
def find_key(val):
    for key, value in clique_dict.items():
        if value == val: return key
    return none

#remove duplicate items
#from ASPN Python Cookbook, code by Tim Peters
#http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/52560
def unique(s):
    """Return a list of the elements in s, but without duplicates.

    For example, unique([1,2,3,1,2,3]) is some permutation of [1,2,3],
    unique("abcabc") some permutation of ["a", "b", "c"], and
    unique(([1, 2], [2, 3], [1, 2])) some permutation of
    [[2, 3], [1, 2]].

    For best speed, all sequence elements should be hashable.  Then
    unique() will usually work in linear time.

    If not possible, the sequence elements should enjoy a total
    ordering, and if list(s).sort() doesn't raise TypeError it's
    assumed that they do enjoy a total ordering.  Then unique() will
    usually work in O(N*log2(N)) time.

    If that's not possible either, the sequence elements must support
    equality-testing.  Then unique() will usually work in quadratic
    time.
    """

    n = len(s)
    if n == 0:
        return []

    # Try using a dict first, as that's the fastest and will usually
    # work.  If it doesn't work, it will usually fail quickly, so it
    # usually doesn't cost much to *try* it.  It requires that all the
    # sequence elements be hashable, and support equality comparison.
    u = {}
    try:
        for x in s:
            u[x] = 1
    except TypeError:
        del u  # move on to the next method
    else:
        return u.keys()

    # We can't hash all the elements.  Second fastest is to sort,
    # which brings the equal elements together; then duplicates are
    # easy to weed out in a single pass.
    # NOTE:  Python's list.sort() was designed to be efficient in the
    # presence of many duplicate elements.  This isn't true of all
    # sort functions in all languages or libraries, so this approach
    # is more effective in Python than it may be elsewhere.
    try:
        t = list(s)
        t.sort()
    except TypeError:
        del t  # move on to the next method
    else:
        assert n > 0
        last = t[0]
        lasti = i = 1
        while i < n:
            if t[i] != last:
                t[lasti] = last = t[i]
                lasti += 1
            i += 1
        return t[:lasti]

    # Brute force is all that's left.
    u = []
    for x in s:
        if x not in u:
            u.append(x)
    return u

#find all combinations of a list
#from Programming Python, p.1016
def combo(list, size):
    if size == 0 or not list:
        return [list[:0]]
    else:
        result=[]
        for i in range(0, (len(list) - size) + 1):
            pick = list[i:i+1]
            rest = list[i+1:]
            for x in combo (rest, size - 1):
                result.append(pick +x)
        return result

def rem_cycle(T,C,weights):
    max_weight = max(weights)
    x=1
    while x <= max_weight:
        edge_num = 0
        for edge in C.edges():
            if weights[edge_num] == x:
                T.delete_edge(edge)
                #print "connected nodes"
                #print connected_components(T)
                if connected_components(T)[0] != C.nodes():
                    T.add_edge(edge)
            edge_num = edge_num + 1
        x = x + 1

#create the graph data structure from a file  
def load_graph_from_file(G,graph_def_file):
    graph_file = open(graph_def_file,'r')
    line_count=0
    for line in graph_file.readlines():
        if line_count==0:
            num_of_nodes = int(line)
            G.add_nodes_from([1,num_of_nodes])
            #print "the number of nodes is: %s" % num_of_nodes
        else:
            n1, n2 = string.split(line)
            #create the edges
            G.add_edge(int(n1),int(n2))
            #print "first col: %s, second col: %s" % (n1,n2)
        line_count = line_count + 1
    graph_file.close()
#make a clique graph out of a triangulated graph
#don't need this
def make_clique_graph(G,C):
    #name the clique graph nodes
    total_cliques = graph_number_of_cliques(G, cliques=None)

    x=0
    while x<total_cliques:
        C.add_node(x)
        x = x+1
    print "clique graph nodes"
    print C.nodes()

    #create the clique graph edges
    #print all_cliques[0]
    #create a dictionary of the cliques with clique node IDs
    global clique_dict
    clique_dict = {}
    x=0
    while x<total_cliques:
        clique_dict[x] = all_cliques[x]
        x=x+1

    #show the list of cliques containing each node
    #print cliques_containing_node(G, nodes=1, cliques=None, with_labels=True)
    n=1
    my_edges = []
    edge_cost = []
    while n <= number_of_nodes(G):
        found_node = cliques_containing_node(G, nodes=n, cliques=None, with_labels=False)

        #make an edge
        length = len(found_node)
        cedge = []
        for x in found_node:
            if cedge != []:
                    edge1 = find_key(x)
                    cedge = cedge + [edge1]
            else:
                    edge1 = find_key(x)
                    cedge = cedge + [edge1]
                
        my_edges = my_edges + combo(cedge,2)
        n = n + 1

    #get rid of the duplicates
    cedge_final = unique(my_edges)
    print "final clique edges:"
    #save the edges to the clique graph
    C.add_edges_from(cedge_final)
    print C.edges()

#make a junction tree out of the clique graph
def make_junction_tree(J,C):
    max_cliques = find_cliques(C)
    #print "the cliques are"
    #print max_cliques
    J.add_nodes_from(C.nodes())
    #print "my new J graph is"
    #print J.nodes()
    for cycle in max_cliques:
        size_of_cycle = len(cycle)
        #create the new edges if cycle is not just an edge
        #if len(cycle) > 2:
        count=0
        for cgnode in cycle:
            #not the last node in the cycle
            #print "looking at %d" % cgnode
            #print "count is %d, size of cycle is %d" % (count,size_of_cycle) 
            if (count+1) < size_of_cycle:
                J.add_edge(cgnode,cycle[count+1])
                #print "adding an edge from %d to %d" % (cgnode,cycle[count+1])
            else:
                J.add_edge(cgnode,cycle[0])

            count = count + 1
    #print "my new J graph edges are"
    #print J.edges()

def check_for_cycles(J):
    leftover_cliques = find_cliques(J)
    for node in J.nodes():
        found_node = cliques_containing_node(J, nodes=node, cliques=None, with_labels=False)
        #print found_node
    
    for cycle in leftover_cliques:
        if len(cycle) > 2:
            print "there's still cycles"
            print leftover_cliques
        else:
            print "no cycles found, we have a junction tree"
            #print leftover_cliques

def edge_weights(all_cliques,C,weights,all_edge_sets):
    weight_index = 0
    for edge in C.edges():
        n1 = (edge[0] - 1)
        n2 = (edge[1] - 1)
        weight_count = 0
        edge_set = []
        for n1node in all_cliques[n1]:
            for n2node in all_cliques[n2]:
                if n1node == n2node:
                    weight_count = weight_count + 1
                    edge_set = edge_set + [n1node]
        weights[weight_index] = weight_count
        all_edge_sets[weight_index] = edge_set
        weight_index = weight_index + 1

def edge_weight_pair(weights,C,pair):
    index_val = 0
    for w in weights:
        pair.append([C.nodes()[index_val],w])
        index_val = index_val + 1

def find_alternating_4_cycle(J):
    """
    Returns False if there aren't any alternating 4 cycles.
    Otherwise returns the cycle as [a,b,c,d] where (a,b)
    and (c,d) are edges and (a,c) and (b,d) are not.
    """
    for (u,v) in J.edges():
        for w in J.nodes():
            if not J.has_edge(u,w) and u!=w:
                for x in J.neighbors(w):
                    if not J.has_edge(v,x) and v!=x:
                        return [u,v,w,x]
    return False

def build_routes(T,jt_routes_file):
    routes = []
    jt_rt = open(jt_routes_file,'w')
    for node_source in T.nodes():
        for node_target in T.nodes():
            if node_source != node_target:
                path = shortest_path(T, node_source, node_target)
                #in the format: source:destination:nexthop
                entry = "%d:%d:%d\n" % (node_source,node_target,path[1])
                jt_rt.write(entry)
                routes = routes + [path]
    jt_rt.close()
    return routes


    
######################################################################

graph_def_file = "graph-8nodes.txt"
jt_routes_file = "jt-routes.txt"

G=networkx.Graph()
load_graph_from_file(G,graph_def_file)

#display the graph information
#print "All the nodes"
#print G.nodes()

#print "All the cliques"
all_cliques = find_cliques(G)
#print all_cliques

#make a clique graph
C=networkx.Graph()
#make_clique_graph(G,C)
C = make_max_clique_graph(G, create_using=None)
#setup the weights array
weights = [[]] * len(C.edges())
all_edge_sets = [[]] * len(C.edges())
edge_weights(all_cliques,C,weights,all_edge_sets)
#print "clique graph edges"
#print len(C.edges())
#print C.edges()
print "weights"
#print len(weights)
print weights
print "edge sets"
print all_edge_sets

#get rid of cycles in the clique graph
#foreach cycle, delete one of the edges
#check for cycles, if found one, delete one edge
#check again until all cycles are gone
#print "the cycles are: "

#create a new graph for the junction tree
J=networkx.Graph()
make_junction_tree(J,C)
#check_for_cycles(J)

found_cycles=find_alternating_4_cycle(C)
print "found cycles"
print found_cycles
T=networkx.Graph()
T = C
rem_cycle(T,C,weights)
print all_cliques[0]

print "junction tree"
print T.nodes()
print T.edges()


# MESSAGES function
#get the routes between the cliques
routes = build_routes(T,jt_routes_file)



