# Practical: Phylogenetic analysis
In this practical, you will learn to create a phylogenetic tree from an alignment and visualise it in different tools. 

## Overview 
1.	Phylogeny on alignment from morning session using different methods:
    - Simple Neighbor-joining (MEGA)
    - Maximum parsimony with bootstrap (MEGA)
    - Approximate maximum likelihood (fasttree)
    - Maximum likelihood (IQTREE)
2.	Visualisation of tree with Microreact, iTOL and ETE3


## Before you start
### Stand alone software
For this exercise, you will need the following stand alone software: 
- Figtree (http://tree.bio.ed.ac.uk/software/figtree/)
- MEGA ≥v10 (https://www.megasoftware.net)
- A Web browser (in order to use Microreact and iTol and to visualize a .png image)

### Exercise data
> **Note:** If you have done these steps for session 1, there is no need to redo them  

All required files for the practicals are deposited in the github repo [github.com/ssi-dk/GenEpi-BioTrain_Virtual_Training_7](https://github.com/ssi-dk/GenEpi-BioTrain_Virtual_Training_7).  
To get started, clone this repo to your computer.  
```sh
cd <your preferred location>
git clone https://github.com/ssi-dk/GenEpi-BioTrain_Virtual_Training_7.git
cd GenEpi-BioTrain_Virtual_Training_7
```
To have the required tools installed on your computer, use `conda` with the provided environment `.yaml` files:
```sh
conda env create -f alignment.env.yaml
conda env create -f phylo.env.yaml
```
Important: Create a subfolder within the repo folder for each tool you are running on the command line, so the output of each tool is in its own folder. 

## Part 1
In Part 1 of this practical, we will create phylogenetic trees using different methods. 

### Exercise 1: Create a Neighbour-joining tree
Neighbor joining (NJ) is a bottom-up (agglomerative) clustering method for the creation of phylogenetic trees, created by Naruya Saitou and Masatoshi Nei in 1987. Neighbour joining takes a distance matrix, which specifies the distance between each pair of taxa, as input. The algorithm starts with a completely unresolved tree, whose topology corresponds to that of a star network, and iterates over several deterministic steps, until the tree is completely resolved, and all branch lengths are known.  

Here we use the [*MEGA*](https://www.megasoftware.net) software to create a NJ tree.  

>If you don't have it available yet, download the required file `16s_sequences_mafft_alignment.fasta` from EVA or via command line using:
> ```sh
> wget https://raw.githubusercontent.com/ssi-dk/GenEpi-BioTrain_Virtual_Training_7/main/data/16s_data/16s_sequences_mafft_alignment.fasta
> ```
1.	Open MEGA on your Computer
2.	Drag-n-drop the `16s_sequences_mafft_alignment.fasta` file from session 1 on the window
3.	Choose `Analize` because the file is already aligned
4.	Choose `Nucleotide Sequences`
5.	Choose `Yes` when asked if these are protein-coding sequences because we are using the full 16S sequence.
6.	Choose `Standard`
7.	Click on Phylogeny and choose a `NJ phyologeny`
8.	Choose `yes` for the current file
9.	Check the parameters and press `OK`  

A tree showing the phylogenetic relationship appears. Read the caption and decide if you agree. 

Questions: 
1.	Which isolates cluster together?
2.	Which genomes are most closely related to the *S. aureus* genomes?
3.	Is this a reliable tree? 


### Exercise 2: Create a Maximum parsimony tree with 100 bootstrap replicates
We again use the [*MEGA*](https://www.megasoftware.net) software to create a Maximum parsimony tree. 

1.	Click on Phylogeny and choose a maximum parsimony phyologeny
2.	Choose `yes` for the current file
3.	Check the parameters and press `OK`. Make sure you enter `100` bootstrap replicates in the “Test phylogeny” field. 

A tree showing the phylogenetic relationship appears. Read the caption and decide if you agree. 

Questions: 
1.	What do the numbers mean? 
2.	Which groupings are most reliable based on this data?


### Exercise 3: Remove recombinant sites from SNP matrix
Now we switch to the command line and to the core genome SNPs from the *L. monocytogenes* dataset from session 1.  

>If you don't have it available yet, download the required file `core.aln` from EVA or via command line using:
> ```sh
> wget https://raw.githubusercontent.com/ssi-dk/GenEpi-BioTrain_Virtual_Training_7/main/data/core.aln
> ```

Load the `phylo` environment using the following command:
```sh
source activate phylo
```
And cd into the directory with the course data:
```sh
cd <your_repo_path>
```
To obtain a good alignment of SNPs, we need to take care of regions of putative recombination. We use [gubbins](https://github.com/nickjcroucher/gubbins) to remove these regions from the SNP matrix.  
To do so, we first need to strip odd characters from the matix using a sed command because gubbins doesn’t like these:
```sh
mkdir gubbins
cd gubbins
sed -r 's/::.*//' ../snippy/core.aln > core_stripped.fasta
```
This creates a copy of the matrix with the odd characters stripped.  
We can then run the gubbins command:
```sh
run_gubbins.py core_stripped.fasta -c 8
```
This will output a purged SNP matrix with fewer sites but the same number of taxa called `core_stripped.filtered_polymorphic_sites.fasta`


### Exercise 4: Create a maximum likelihood tree with IQTREE
We use the very versatile software [*IQTREE*](http://www.iqtree.org) to produce a high-quality maximum likelihood tree from the purged SNP matrix.  

>If you don't have it available yet, download the required file `core.aln` from EVA or via command line using:
> ```sh
> wget https://raw.githubusercontent.com/ssi-dk/GenEpi-BioTrain_Virtual_Training_7/main/data/core_stripped.filtered_polymorphic_sites.fasta
> ```

Run iqtree: 
```sh
cd ..; mkdir iqtree; cd iqtree
iqtree -s ../gubbins/core_stripped.filtered_polymorphic_sites.fasta -m TEST+ASC -T AUTO --threads-max 8 -pre ML_iqtree -mem 8GB
```
This creates the output file `ML_iqtree.treefile`, which is a *NEWICK* format tree file. To use it further, we need to make a copy with extension .nwk: 
```sh
cp ML_iqtree.treefile ML_iqtree.treefile.nwk 
```

### Exercise 5 (optional): Create a fast approximate maximum likelihood tree with fasttree
We use the very fast software [fasttree](http://www.microbesonline.org/fasttree/) to produce a fast approximate maximum likelihood tree from the purged SNP matrix. 
```sh
cd ..; mkdir fasttree; cd fasttree
fasttree -nt -gtr ../gubbins/core_stripped.filtered_polymorphic_sites.fasta > core_fasttree.nwk
```
This creates the output file `core_fasttree.nwk`, which is a *NEWICK* format tree file. 

## Part 2
In this part, we will visualize the obtained tree using different methods. 

### Exercise 1: Visualize a tree using Microreact
[Microreact](https://microreact.org) is a tool for open data visualization and sharing for genomic epidemiology. It is freely available and is widely used in public health data analysis.  

>If you don't have them available yet, download the required files from EVA or via command line using:
> ```sh
> wget https://raw.githubusercontent.com/ssi-dk/GenEpi-BioTrain_Virtual_Training_7/main/data/ML_iqtree.treefile.nwk
> wget https://raw.githubusercontent.com/ssi-dk/GenEpi-BioTrain_Virtual_Training_7/main/metadata/metadata.tsv
> ```

To get your tree visualized and annotated in Microreact, do the following:
1.	Go to [https://microreact.org](https://microreact.org) and watch the video if you want to
2.	Click on `upload`
3.	Choose or drop your tree file
4.	Click continue
5.	Find out how to display the labels.
6.	Re-root your tree with the ancestor of samples `SRR27240812` and `SRR27240820` as outgroup (use the right-click menu on the correct internal node)
7.	Add the metadata file `metadata.tsv` (available in the `metadata` folder) to the tree by linking `key` column to the tree tip labels
8.	Add color columns for `Region`, `KMA` and `SampleMaterial` using the `Metadata blocks` button
9.	Add a map using the `lat` and `long` columns from the metadata by clicking on the pencil (Add or edit panels) on the top right.
10.	Download the map as a `.png` and the tree as a `.svg` file. 
  
Questions: 
1.	Which isolates are closely related and are therefore probably part of the same outbreak?
2.	Do they all come from the same region? 

### Exercise 2: Visualize a tree using iTOL
[iTOL](https://itol.embl.de) is an online tool for visualizing phylogenies and related metadata. The tool is free to use, but for saving your annotations, paied subscription has been introduced a few years ago.  
The tool is frequently used for publication ready phylogenetic trees.  
>If you don't have them available yet, download the required files from EVA or via command line using:
> ```sh
> wget https://raw.githubusercontent.com/ssi-dk/GenEpi-BioTrain_Virtual_Training_7/main/data/ML_iqtree.treefile.nwk
> wget https://raw.githubusercontent.com/ssi-dk/GenEpi-BioTrain_Virtual_Training_7/main/metadata/metadata.tsv
> wget https://raw.githubusercontent.com/ssi-dk/GenEpi-BioTrain_Virtual_Training_7/main/metadata/dataset_color_gradient_template.txt
> wget https://raw.githubusercontent.com/ssi-dk/GenEpi-BioTrain_Virtual_Training_7/main/metadata/dataset_color_strip_template.txt
> ```

To get your tree visualized and annotated in iTOL do the following:
1.	Open iTOL on [https://itol.embl.de](https://itol.embl.de) 
2.	Click on `Upload`
3.	Upload your newick tree file by clicking `choose file`
4.	Re-root your tree with the ancestor of samples `SRR27240812` and `SRR27240820` as outgroup (use the submenu `Tree structure`)
5.	Use the provided templates `dataset_color_strip_template.txt` and `dataset_color_gradient_template.txt` from the `metadata` folder to add annotations:  
    a. Go to `Datasets` in the Control panel  
    b. Click on `Upload annotation files`  
    c. Choose the two files and click `upload`  
    >*Note*: More templates can be downloaded from [https://itol.embl.de/help.cgi#annoTemplate](https://itol.embl.de/help.cgi#annoTemplate)
6.	Export and save your tree with annotations as a `.pdf`

### Exercise 3: Visualize a tree using the python library ETE3 (for command line users only)
[*ETE3*](http://etetoolkit.org) is a python toolkit to do phylogenetic analysis and visualize phylogenetic trees.  

Here we have prepared a basic script to plot our tree, called `ete3_phylo.py` (available in the `scripts` folder).  
> This script is dependent on the correct folder structure and file names, namely: `iqtree/ML_iqtree.treefile.nwk` and `metadata/metadata.tsv` as well as the script in the `scripts` folder.

To run the script, open a console and type the following commands:
```sh
python scripts/ete3_phylo.py
open mytree.png
```
Open the file mytree.png and compare it to the figures obtained in other tools.

Inspect the script and try to answer the following questions:  

1. What does the `my_layout()` function do? 
2. Where are the colors for the regions defined? Can you change one of them? 
3. What are the rectangles colored by?  

If you have some extra time, try to change some of the settings in the script. 
