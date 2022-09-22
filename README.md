# Sequencing-File-Renamer
## Evan Huang, Swinburne Lab, UC Berkeley

The purpose of this program is to make submissions to sequencing smoother and to organize the files. If you number your sequencing samples simply from 1, 2, 3...n this program can rename them using a reference csv. 

This renamer program renames all files in a directory of sequencing data based on a user-inputted reference csv. It will make a copy of the renamed data with a copy of the original data. Note this program will not work with versions of Python older than 3.8. 

[Renamer Setup Guide](https://docs.google.com/document/d/1nstSoI9pFRei7pu8AAqdtOgbb1B34kcdZqy_U5lsKfM/edit?usp=sharing)

The Generator is a program meant to help with organization for sequencing and is meant to work with the renamer. It organizes samples based on genes, amplicons, sequencing oligos, and clones. This data is saved in 2 .csv files: 1 containing all of the data for each sample, and another containing the samples' compiled names to be used in the Renamer program. 