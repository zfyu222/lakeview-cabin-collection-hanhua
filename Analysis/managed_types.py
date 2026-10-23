from UnityPy.helpers.TypeTreeGenerator import TypeTreeGenerator
from UnityPy.helpers import TypeTreeHelper as H
H.read_typetree_boost = None

def generator(game):
    g = TypeTreeGenerator('5.3.4f1')
    g.load_local_game(str(game))
    return g

def fixed_nodes(g, assembly, fullname):
    node = g.get_nodes_up(assembly, fullname)
    def fix(n):
        if n.m_Name == 'm_Enabled' and n.m_Level == 1:
            n.m_MetaFlag |= 16384
        if n.m_Children and n.m_Children[0].m_Type == 'Array' and n.m_Type in H.FUNCTION_READ_MAP and n.m_Children[0].m_Children[1].m_Type != 'char':
            n.m_Type = 'vector'
        for child in n.m_Children:
            fix(child)
    fix(node)
    return node
