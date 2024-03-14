# Practical: Genome alignments
## Overview 
Exercise: Fill out the Needleman-Wunsch algorithm matrix (on a handout)  
Exercise: Make a multi sequence alignment using muscle and mafft
Exercise: Get familiar with the blastn command  
Exercise: Run MLST  
Exercise: Run a core-genome SNP analysis using snippy

## Before you start
All required files for the practicals are deposited in the github repo [github.com/ssi-dk/GenEpi-BioTrain_Virtual_Training_7](https://github.com/ssi-dk/GenEpi-BioTrain_Virtual_Training_7).  
To get started, clone this repo to your computer.  
```sh
cd <your preferred location>
git clone https://github.com/ssi-dk/GenEpi-BioTrain_Virtual_Training_7.git
cd GenEpi-BioTrain_Virtual_Training_7
```
To have the required tools installed on your computer, use `conda` with the provided environment `.yaml` files:
```sh
conda install -c bioconda -c conda-forge -f alignment.env.yaml
conda install -c bioconda -c conda-forge -f phylo.env.yaml
```
Important: Create a subfolder within the repo folder for each tool you are running on the command line, so the output of each tool is in its own folder. 

## Exercise 1: Needleman-Wunsch algorithm
![Needelmann-Wunsch substitution matrix](./imgs/NWsubst_model.png)  
Gap penalty = -2
![Needelmann-Wunsch exercise](./imgs/NWexercise.png)  

## Exercise 2: Multiple Sequence Alignment with mafft and muscle
Use the environment `alignment`  
Align the sequences found in data/16S/16s_sequences.fasta using mafft and muscle from command line

To download sequences use:
```sh
wget https://github.com/ssi-dk/GenEpi-BioTrain_Virtual_Training_7/raw/main/data/16s_data/16s_sequences.fasta
```
Have a look at the file
```sh
less 16s_sequences.fasta
```


Check MAFFT helper

```sh
mafft -h
```

Run MAFFT to align the sequences in 16s_sequences.fasta

```sh
mafft 16s_sequences.fasta > 16s_sequences_mafft_alignment.fasta
```

Check MUSCLE helper

```sh
muscle -h
```

Run MUSCLE to align the sequences in 16s_sequences.fasta

```sh
muscle -align 16s_sequences.fasta -output 16s_sequences_muscle_alignment.fasta
```



## Exercise 3: blastn
Use blastn to identify the 16s rRNA gene in one of the spades assemblies found in `data/spades_assemblies`  
Use the environment `alignment`  
```sh
blastn -h
```
Use 16s_sequences.fasta as query input and one of the assembly fasta files as subject input

## Exercise 4: MLST

Use the environment `alignment`  

Perform in-silico MLST on all the spades assemblies in `data/spades_assemblies_careful`

Note: You can use `*` to select multiple files or folders for mlst.

## Exercise 5: Core genome alignment and SNP analysis

Use a screen so you can have the job running in the background: 
```sh
screen
```

Use the environment `alignment`  
```sh
. activate alignment
```

Run Snippy on the 23 assembly files in `assemblies/`

```sh
mkdir snippy
cd snippy
for f in ../assemblies/*.fasta; do n=$(basename $f); n=${n/.fasta}; snippy --outdir $n --ctgs ${f} --reference  ../assemblies/SRR27240806.fasta; done
```
When it's running, you can detach the screen using `Ctrl+A`, followed by `D` to return to your original terminal window.  
To get back into the screen, use `screen -r`  
> Note: For running snippy on raw reads (which is much more reliable but takes a bit longer):  
> ```sh
> for f in ../reads/SRR272408*_R1*; do n=$(basename $f); snippy --outdir ${n/_R1*} --R1 $(dirname ${f})/${n} --R2 $(dirname ${f})/${n/_R1*}_R2.fastq.gz --reference ../assemblies/SRR27240806.fasta; done
> ```
When snippy is done, you need to create the core-genome using:  
```sh
snippy-core --ref SRR27240806/ref.fa SRR*/
```

and finally you can exit the screen: 
```sh
exit
```

