#!/usr/bin/env python3
import os
import pandas as pd
from scripts.ete3_phylo import Tree, add_face_to_node, TextFace, TreeStyle, RectFace
os.environ['QT_QPA_PLATFORM']='offscreen'
base_path = ''

# Load metadata and convert to dict
metadata = pd.read_csv(base_path+'../metadata/metadata.tsv', delimiter = '\t')
m_dict = dict()
for i, row in metadata.iterrows():
    m_dict[str(row['Key'])] = {'Date': row['Prøvedato'], 'Region': row['region'], 'SampleMaterial': row['SampleMaterial']}

# Create a color dict for regions
cols_dict = {'Region': {'Copenhagen': 'Blue', 'Jutland - M': 'Green', 'Zealand': 'Red', 'Jutland - N': 'Orange'}, 
            'SampleMaterial': {'Blod': 'Green', 'Spinalvæske': 'Steelblue', 'Andet': 'Purple'}}


# Create a layout function for the leafs
def my_layout(node):
    if node.is_leaf():
        reg_col = cols_dict.get('Region', {}).get(m_dict.get(node.name, {}).get('Region', ''), 'black')
        travel_col = cols_dict.get('SampleMaterial', {}).get(m_dict.get(node.name, {}).get('SampleMaterial', ''), 'black')
        name_face = TextFace(node.name, fgcolor=reg_col, fsize=10)
        node.add_face(name_face, column=0, position='branch-right')
        Rect = RectFace(10, 10, "black", travel_col)
        Rect.margin_left = 10
        node.add_face(Rect, column=0, position="aligned")

        Date = TextFace(m_dict.get(node.name, {}).get('Date', ""), fsize=10)
        Date.margin_left = 10
        add_face_to_node(Date, node, column=1, position='aligned')
        SampleMaterial = TextFace(m_dict.get(node.name, {}).get('SampleMaterial', ""), fsize=10)
        SampleMaterial.margin_left = 10
        add_face_to_node(SampleMaterial, node, column=2, position='aligned')
        Region = TextFace(m_dict.get(node.name, {}).get('Region', ""), fsize=10, fgcolor=reg_col)
        Region.margin_left = 10
        add_face_to_node(Region, node, column=3, position='aligned')

# Load the tree file 
t = Tree(base_path + 'iqtree/ML_iqtree.treefile.nwk', format=1)

# Apply stypes
ts = TreeStyle()
ts.show_leaf_name = False
ts.layout_fn = my_layout

# Render the tree
t.render(base_path + 'mytree.png', w=288, units='mm', tree_style=ts)
