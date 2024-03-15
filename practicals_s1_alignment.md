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
conda env create -f alignment.env.yaml
conda env create -f phylo.env.yaml
```
Important: Create a subfolder within the repo folder for each tool you are running on the command line, so the output of each tool is in its own folder. 

## Exercise 1: Needleman-Wunsch algorithm
![Needelmann-Wunsch substitution matrix](https://github.com/ssi-dk/GenEpi-BioTrain_Virtual_Training_7/raw/main/imgs/NWsubst_model.png)  
Gap penalty = -2
![Needelmann-Wunsch exercise](https://github.com/ssi-dk/GenEpi-BioTrain_Virtual_Training_7/raw/main/imgs/NWexercise.png)  

## Exercise 2: Multiple Sequence Alignment with mafft and muscle
Use the environment `alignment`  
Align the sequences found in data/16S/16s_sequences.fasta using mafft and muscle from command line

If you don't have them available yet, download the sequences using:
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



## Exercise 3: BLAST
For this exercise we will use the Listeria assemblies found in assemblies.tar.gz

If you have not already downloaded and extracted these, either download the tar-file from EVA or from github using
```sh
wget https://github.com/ssi-dk/GenEpi-BioTrain_Virtual_Training_7/raw/main/data/assemblies.tar.gz
```

You can extract the assemblies using

```sh
tar -xf assemblies.tar.gz
```

This will create a folder named “assemblies” with genome assemblies for 22 isolates. Have a look at the first one with
```sh
less assemblies/SRR27240806.fasta
```

We will use blast to identify the v3-v4 region of the 16s rRNA gene in this assembly. For that we will need a reference sequence.  
If you have not already downloaded this, do so using
```sh
wget https://github.com/ssi-dk/GenEpi-BioTrain_Virtual_Training_7/raw/main/data/16s_data/16s_v3_v4_reference.fasta
```

have a look at the file 
```sh
less 16s_v3_v4_reference.fasta
```

Use the environment `alignment` 

First check out the blast help file

```sh
blastn -h
```

Now we'll use blast to identify the 16s v3-v4 region in one of our isolates. For that we will use the v3-v4 reference sequence fasta file as query and the assembly fasta file as subject. Output the data to a file.

```sh
blastn -query 16s_v3_v4_reference.fasta -subject assemblies/SRR27240806.fasta -out SRR27240806_16s_blast.txt
```
Have a look at the output

```sh
less SRR27240806_16s_blast.txt
```

Now do the same blast, but with a more programmatic-friendly tab separated output

```sh
blastn -query 16s_v3_v4_reference.fasta -subject assemblies/SRR27240806.fasta -out SRR27240806_16s_blast.tsv -outfmt 6
```
And have a look

```sh
less SRR27240806_16s_blast.tsv
```

Again with a programmatic friendly output, but this time we want to output specific information. Like the exact DNA sequence of the subject match and the length of the input sequence

```sh
blastn -query 16s_v3_v4_reference.fasta -subject assemblies/SRR27240806.fasta -out SRR27240806_16s_blast_2.tsv -outfmt "6 qseqid sseqid length qlen pident sseq"
```
And have a look at the output again

```sh
less SRR27240806_16s_blast_2.tsv
```


We can also blast multiple query sequences at once. Let us try with all the different 16s sequences we aligned earlier.

```sh
blastn -query 16s_sequences.fasta -subject assemblies/SRR27240806.fasta -out SRR27240806_16s_all_blast.txt
```
And have a look at the output again

```sh
less SRR27240806_16s_all_blast.txt
```


BLAST is fast with a small data set like a single bacterial genome, but with large subject sequences it can get computationally heavy.
By building a pre-indexed database that can be passed with the -db option, rather than parsing a subject sequence with the -subject option, you can speed up your blast search.
Additionaly, it is easy to include data from multiple genomes in our database, so we can identify sequences in multiple isolates with a single blast search.

We want to create a blast database containing the genomes of all 22 isolates in the assemblies folder. To do this, we first have to combine (or in computer-speak "concatenate"), all our assemblies into a single fasta file.

To do this, use:
```sh
cat assemblies/*.fasta > Listeria_assemblies.fasta
```

We can now create a blast database from this file.
First create a folder for your database:
```sh
mkdir blast_DB
```

And then make the database using
```sh
makeblastdb -hash_index -in Listeria_assemblies.fasta -out blast_DB/Listeria_assemblies -dbtype nucl
```

Have a look at the files in the "blast_DB" folder
```sh
ls -l blast_DB
```

We can now query the reference 16s sequence against all the assemblies at once
```sh
blastn -query 16s_v3_v4_reference.fasta -db blast_DB/Listeria_assemblies -out Listeria_16s_blast.txt
```

And have a look at the output
```sh
less Listeria_16s_blast
```


## Exercise 4: Core genome alignment and SNP analysis

Use a screen so you can have the job running in the background: 
```sh
screen
```

Use the environment `alignment`  
```sh
. activate alignment
```

Run Snippy on the 22 assembly files in `assemblies/`

```sh
mkdir snippy
cd snippy
for f in ../assemblies/*.fasta; do n=$(basename $f); n=${n/.fasta}; snippy --outdir $n --ctgs ${f} --reference  ../assemblies/SRR27240806.fasta; done
```
When it's running, you can detach the screen using `Ctrl+a`, followed by `d` to return to your original terminal window.  
To get back into the screen, use `screen -r`  
> Note: For running snippy on raw reads (which is much more reliable but takes a bit longer):  
> ```sh
> for f in ../reads/SRR272408*_R1*; do n=$(basename $f); snippy --outdir ${n/_R1*} --R1 $(dirname ${f})/${n} --R2 $(dirname ${f})/${n/_R1*}_R2.fastq.gz --reference ../assemblies/SRR27240806.fasta; done
> ```
When snippy is done, you need to create the core-genome using:  
```sh
snippy-core --ref SRR27240806/ref.fa SRR27240806 SRR27240807 SRR27240808 SRR27240809 SRR27240810 SRR27240811 SRR27240812 SRR27240813 SRR27240814 SRR27240815 SRR27240816 SRR27240817 SRR27240818 SRR27240819 SRR27240820 SRR27240821 SRR27240822 SRR27240823 SRR27240824 SRR27240825 SRR27240826 SRR27240827
```

and finally you can exit the screen: 
```sh
exit
```

