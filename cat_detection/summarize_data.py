import pprint

with open('process_info.tsv') as f:
    with open('process_info_simple.tsv', 'w') as fw:
        for line in f.readlines():
            file, num_cat = line.split('\t')
            _, _, tag, filename = file.split('/')
            fw.write('\t'.join([tag, filename, num_cat]))

dic = {}
with open('process_info_simple.tsv') as f:
    for line in f.readlines():
        tag, filename, num_cat = line.rstrip().split('\t')
        num_cat = int(num_cat)
        dic[tag] = dic.get(tag, {"num_files": 0,
                                 "num_files_with_single_cat":0,
                                 "num_files_with_no_cat":0,
                                 "num_files_with_multiple_cats": 0})
        dic[tag]["num_files"] += 1
        if num_cat == 0:
            dic[tag]["num_files_with_no_cat"] += 1
        elif num_cat == 1:
            dic[tag]["num_files_with_single_cat"] += 1
        else:
            dic[tag]["num_files_with_multiple_cats"] += 1

pprint.pprint(dic)

with open('data_summary.tsv', 'w') as fw:
    fw.write('tag,\tnum_files\tnum_files_with_single_cat\tnum_files_with_multiple_cats\tnum_files_with_no_cat\n')
    for tag, nums in dic.items():
        fw.write(f'{tag}\t{nums["num_files"]}\t{nums["num_files_with_single_cat"]}\t{nums["num_files_with_multiple_cats"]}\t{nums["num_files_with_no_cat"]}\n')
    
