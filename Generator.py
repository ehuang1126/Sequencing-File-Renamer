import csv
import ipywidgets as widgets

def generate_csv(base, genes, amp, oligos, clones, output_path, append=False): 
    """    
    generates a csv to output_path to organize sequencing prep based on inputs.
    base: string for base data (ex: date of genotyping, etc.)
    
    Args: 
        base: string
        genes: ['gene1', 'gene2',...]
        amp: [['1_2', '3_4'],['5_6', '7_8'], ...] 2D list. len(amp) == len(genes). 
        oligos: [[[1, 2, 3], [4, 5, 6]], [[1, 3, 5], [2, 4, 6]], ...] 
            3D list. len(oligos)==len(amp)==len(genes). 
            len(oligos[i]) == len(amp[i]). 
            oligos[i][j] == list of oligos for amp[i][j] for gene[i]. 
        clones: list for which clones for each set of oligos. aka how many templates used. 
        output_path: path for csv file to write to.
        append: will append data to an existing csv. default false. 
        
    Returns:
        nx2 matrix of indexes and final files names
    """
    
    assert len(amp) == len(genes)
    assert len(oligos)==len(amp)
    for i in range(len(oligos)):
        assert len(oligos[i]) == len(amp[i])
    
    header = ['base', 'index', 'gene', 'amp', 'oligos', 'clones']
    matrix = []
    index = 1
    for i in range(len(genes)): 
        for j in range(len(amp[i])): 
            for k in range(len(oligos[i][j])):
                for l in clones:
                    matrix.append([base, index, genes[i], amp[i][j], oligos[i][j][k], l])
                    index += 1
                
    edit = "a" if append else "w"
    csv_file = open(output_path, edit)
    csvwriter = csv.writer(csv_file)
    if not append: 
        csvwriter.writerow(header)
    csvwriter.writerows(matrix)
    csv_file.close()
    
    ret_mat = []
    for row in matrix:
        ret_mat.append([row[1],
                    base+'_'+row[2]+'_amp_'+row[3]+'_seq_'+str(row[4])+'_clone_'+str(row[5])])
    
    return ret_mat
            
    
def write_naming_csv(csv_path, matrix, append=False): 
    """
    writes naming matrix to csv
    """
    
    csv_file = open(csv_path, "a" if append else "w")
    csvwriter = csv.writer(csv_file)
    csvwriter.writerow(["index", "name"])
    csvwriter.writerows(matrix)
    csv_file.close()
    