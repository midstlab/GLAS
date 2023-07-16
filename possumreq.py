import requests
import os
import multiprocessing


def send_possum_req_helper(ligand, protein, destination):
    url = 'https://possum.cbrc.pj.aist.go.jp/PoSSuM/report_k.php'
    form_data = {
        'params[0]': protein,
        'params[1]': ligand,
        'params[2]': 'Any',
        'params[3]': 'Any',
        'params[4]': '1',
        'params[5]': '1',
        'params[6]': 0.78,
        'params[7]': 7,
        'params[8]': 500,
        'params[9]': True,
        'params[10]': True,
        'params[11]': True,
        'params[12]': False,
        'params[13]': False,
        'params[14]': '1',
        'button': "Download results as a text file",
    }
    response = requests.post(url, data=form_data)

    with open(destination + "/" + protein + '.txt', 'w') as f:
        f.write(response.text)
    return destination


def send_possum_req(ligand_dict, destination, processes):
    num_cores = processes
    dest_root = destination
    if ligand_dict:
        print("Downloading...")
        pool = multiprocessing.Pool(num_cores)
        results = []
        for key in ligand_dict:
            destination = dest_root + "/" + key
            arr = [f for f in os.listdir(dest_root + "/" + key) if not f.startswith('.')]
            for element in ligand_dict[key]:
                if element + ".txt" not in arr:
                    result = pool.apply_async(send_possum_req_helper, (key, element, destination))
                    results.append(result)

        # Wait for all processes to finish
        pool.close()
        pool.join()
    print("Downloaded Successfully!")
    for key in ligand_dict:
        directory = dest_root + "/" + key # replace with the actual path to your folder
        for filename in os.listdir(directory):
            if filename.endswith('.txt'):  # check if the file is a text file
                file_path = os.path.join(directory, filename)
                with open(file_path, 'r') as f:
                    file_content = f.readlines()
                    if len([line for line in file_content if line.startswith("#")]) == 1:  # check if there's only one line starting with "#"
                        os.remove(file_path)  # delete the file

    return dest_root #modified used to be destination
