# GenEpi-BioTrain - Virtual Training 07 - Phylogenetics and alignments
All data used in the GenEpi-BioTrain Virtual Training 7 session on march 19-20, 2024

## Access the exercises
The exercises are available here:  
[Exercise session 1](./practicals_s1_alignment)  
[Exercise session 2](practicals_s1_phylo.md)

## Data used in this training and how to aquire it 
 
### Download metadata and genome assemblies: 
 
These data can be acquired in three different ways: 
 
1. Clone the github repository containing all the data for the exercises at once. The github repository is found at https://github.com/ssi-dk/GenEpi-BioTrain_Virtual_Training_7 and can be cloned using
    ```sh
    git clone git@github.com:ssi-dk/GenEpi-BioTrain_Virtual_Training_7.git 
    ```

2. Download the data from the EVA webpage for the session under [Session 1 -> exercises](https://eva.ecdc.europa.eu/mod/folder/view.php?id=31001)

3. Download the data for each exercise at the start of the exercise using wget. This is included in instructions for each exercise. 

### Download raw read files (optional and only used in one optional step in the practicals)
Raw read files used in exercises are too large to be hosted on EVA or github and will have to be downloaded from ENA.  
If you want to download read data for the exercises, run the following lines: 
>**Note:** this will take a while and the files are rather large!  
```sh
mkdir -p data
cd data
wget https://github.com/ssi-dk/GenEpi-BioTrain_Virtual_Training_7/raw/main/fastq_ftp_paths.txt 
mkdir reads 
cd reads 
while read line; do wget "$line"; done <../fastq_ftp_paths.txt; 
cd ..
``` 
This will create a folder named “reads”, download a text file named `fastq_ftp_paths.txt` containing the paths to fastq-files on ENA, and download those files into the “reads” folder. 

### Overview of data used for the exercises: 
 
#### 16s_sequences.fasta 
Nucleotide sequences of the v3-v4 region of the 16s rRNA gene from 14 bacterial isolates from different species  
 
Can be downloaded from EVA under [Session 1 -> Exercise](https://eva.ecdc.europa.eu/mod/folder/view.php?id=31001)

Or using: 
```sh
mkdir 16s_data; cd 16s_data
wget https://github.com/ssi-dk/GenEpi-BioTrain_Virtual_Training_7/raw/main/16s_data/16s_sequences.fasta  
cd ..
```
#### assemblies.tar.gz 
Draft assemblies for 22 Listeria monocytogenes isolates that have been part of an outbreak investigation. 
The assemblies have been generated from paired end Illumina Nextseq reads using spades in `--carefull` mode. Contigs <200 bp or <10x kmer coverage have been removed from the assemblies. 
 
Can be downloaded from EVA under [Session 1 -> Exercise](https://eva.ecdc.europa.eu/mod/folder/view.php?id=31001)
 
Or using wget on the command line to download from github: 
```sh
wget "https://github.com/ssi-dk/GenEpi-BioTrain_Virtual_Training_7/raw/main/assemblies.tar.gz" 
```
To unzip the file use 
```sh
tar -xf assemblies.tar.gz 
```
This should create a folder named “assemblies” containing 22 fasta files. 
 
#### fastq_ftp_pathts.txt 
A text file containing the paths to fastq files hosted by ENA. See “download raw read files” above. 

#### Metadata
The metadata folder contains 3 files with metadata. One main file called `metadata.tsv` and two more used as templates for tree annotation in [iTOL](https://itol.embl.de)  

These files can be downloaded from EVA under [Session 2 -> Exercise](https://eva.ecdc.europa.eu/mod/folder/view.php?id=31101)

Or using wget on the command line to download from github: 
```sh
mkdir metadata
cd metadata
wget https://raw.githubusercontent.com/ssi-dk/GenEpi-BioTrain_Virtual_Training_7/main/metadata/metadata.tsv
wget https://raw.githubusercontent.com/ssi-dk/GenEpi-BioTrain_Virtual_Training_7/main/metadata/dataset_color_gradient_template.txt
wget https://raw.githubusercontent.com/ssi-dk/GenEpi-BioTrain_Virtual_Training_7/main/metadata/dataset_color_strip_template.txt
cd ..
```
#### Precomputed core SNP and tree files
Three files are provided so that exercises can be completed also without completing previous exercises. These are: 
- `core.aln`: A precomputed core SNP file as produced by `snippy`
- `core_stripped.filtered_polymorphic_sites.fasta`: A precomputed core SNP file with recombination removed using `gubbins`
- `ML_iqtree.treefile.nwk`: A precomputed maximum likelihood tree file produced using `iqtree`.  

These files can be downloaded from EVA under [Session 2 -> Exercise](https://eva.ecdc.europa.eu/mod/folder/view.php?id=31101)

Or using wget on the command line to download from github: 
```sh
mkdir -p data; cd data
wget https://raw.githubusercontent.com/ssi-dk/GenEpi-BioTrain_Virtual_Training_7/main/data/core.aln
wget https://raw.githubusercontent.com/ssi-dk/GenEpi-BioTrain_Virtual_Training_7/main/data/core_stripped.filtered_polymorphic_sites.fasta
wget https://raw.githubusercontent.com/ssi-dk/GenEpi-BioTrain_Virtual_Training_7/main/data/ML_iqtree.treefile.nwk
cd ..
```
