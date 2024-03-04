import subprocess
import os

path='/mounts/Users/student/yehao/public_html/data/Taxi1500-c_v2.0/'

# This is our shell command, executed by Popen.
files = os.listdir(path)
all_languages = set([x[:3] for x in files])

print(len(all_languages))

with open('lan_file_size.tsv', 'w') as myfile:
    for language in all_languages:
        lan_file = {}

        p = subprocess.Popen(f"wc -l /mounts/Users/student/yehao/public_html/data/Taxi1500-c_v2.0/{language}* ", stdout=subprocess.PIPE, shell=True)
        pbc_sizes = p.communicate()[0].decode("utf-8").split('\n')
        #size_dict = {el.split()[1]:el.split()[0] for el in pbc_sizes[:-2]}

        total_size_list = pbc_sizes

        total_size=[]
        for el in total_size_list:
            if len(el) != 0:
                if el.split()[1] != 'total':
                    total_size.append(el)
        

        size_dict = {el.split()[1]:float(el.split()[0]) for el in total_size}

        sorted_size = sorted(size_dict.items(), key=lambda x: x[1], reverse=True)


        lan_file[language] = sorted_size[0][0]


        print(lan_file)
        line = ('\t').join([language, sorted_size[0][0]])
        myfile.write(line+'\n')
        
    print('Succeed!!!')
  

  