import os
import shutil
import csv
import re
import ipywidgets as widgets

def read_csv(csv_path): 
    """ helper function to read reference csv. make sure csv has a header row """
    csv_file = open(csv_path)
    csvreader = csv.reader(csv_file)
    next(csvreader)
    matrix = []
    for row in csvreader: 
        matrix.append(row)
    csv_file.close()
    
    # check csv in correct format
    assert len(matrix) > 0
    assert len(matrix[0]) >= 2
    
    return matrix

def renamer(ref_csv, input_path, output_path, suffix, prepend=False, make_folders=False, clone_id="clone", reference_map=''): 
    
    # support both .ab1 and .seq files
    both=False
    if suffix == 'both': 
        both = True
        renamer(ref_csv, input_path, output_path, '.ab1', prepend)
        suffix = '.seq'
        
        
    # add period to front of suffix if not added by user
    if suffix[0] != '.': 
        suffix = '.' + suffix
        
    
    names_ref = read_csv(ref_csv)
    
    # make output dir if doesn't already exist
    if not os.path.isdir(output_path): 
        os.mkdir(output_path)
        
    # make a copy of original directory and put it in output path (for safekeeping purposes)
    copy_data_path = output_path + "/data_copy"
    if not os.path.exists(copy_data_path): 
        os.mkdir(copy_data_path)
    shutil.copytree(input_path, copy_data_path, dirs_exist_ok=True)
    
    # get all genotyping files and their indices
    input_dir_raw = os.listdir(input_path)
    ab_files = [x for x in input_dir_raw if x[-len(suffix):] == suffix]
    ab_file_indices = [int(re.findall('-\d+', x)[0][1:]) for x in ab_files]
    
    # get corresponding name for each file based on index and suffix, not including the suffix in the return value
    def findName(ab_file_index): 
        for i in names_ref: 
            if len(i[0]) > 0 and len(i[1]) > 0 and int(i[0]) == ab_file_index: 
                if i[1][-len(suffix):] == suffix: 
                    return i[0] + "_" + i[1][:-len(suffix)]
                else: 
                    return i[0] + "_" + i[1]
        raise Exception("cannot find index in csv")
    
    # copy and rename each file using reference csv
    for i in range(len(ab_file_indices)):
        new_path = shutil.copy2(input_path+"/"+ab_files[i], output_path)
        new_name_raw = findName(ab_file_indices[i])
        if not prepend: 
            new_name = f"{output_path}/{new_name_raw}{suffix}"
            
        else: 
            new_name = f"{output_path}/{new_name_raw}_{ab_files[i]}"
        os.rename(src=new_path, dst=new_name)
        
    # separate files into folders based on clone names
    if make_folders: 
        if both: 
            clone_move(clone_id, output_path, '.ab1', reference_map)
            clone_move(clone_id, output_path, '.seq', reference_map)
        else: 
            clone_move(clone_id, output_path, suffix, reference_map)
    
def clone_move(clone_id, merged_files, suffix, reference_map): 
    """
    helper function to create folders and organize files
    """
    clone_numbers = []
    for file in os.listdir(merged_files): 
        if suffix in file: 
            split = re.split('_|\.', file)
            index_fish = split.index(clone_id)
            individual_in_file = split[index_fish+1]
            if individual_in_file not in clone_numbers:
                clone_numbers.append(individual_in_file)
    clone_numbers.sort()
    file_identifier = [suffix]
    for ind in clone_numbers: 
        path_individual = merged_files+'/'+clone_id+'_'+str(ind)
        if not os.path.exists(path_individual): 
            os.mkdir(path_individual)
        if len(reference_map) > 0:  
            shutil.copy2(reference_map, path_individual)
        for file in os.listdir(merged_files):
            for temp in file_identifier:
                if temp in file:
                    split = re.split('_|\.', file)
                    index_fish = split.index(clone_id)
                    individual_in_file = split[index_fish+1]
                    if individual_in_file==str(ind):
                        src = merged_files + '/' + file
                        dst = path_individual
                        shutil.copy2(src, dst)
        