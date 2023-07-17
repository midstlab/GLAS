from multiprocessing import Pool
import multiprocessing
import time
import os
from txtconverter import txt_to_excel
from postpossum import post_possum
from align import align
from query_pdb import process_ligands
from possumreq import send_possum_req

def take_input():
    """
    Take user input for ligands, destination folder, and other settings.
    Returns a tuple containing input values.
    """

    # Get the destination folder
    destination = input("Enter a path to save required files (leave empty for the current directory): ").strip()
    if not destination:
        destination = os.getcwd()

    # Get ligands
    print("Enter the ligands' letter codes separated by commas.")
    ligands_input = input("Example: 'ABC, DEF, GHI': ").strip()
    ligands = [ligand.strip() for ligand in ligands_input.split(",")]

    # Create folders for ligands if they don't exist
    for ligand in ligands:
        ligand_folder = os.path.join(destination, ligand, "ExcelFiles", "ResultFiles", "AlignedResults")
        try:
            os.makedirs(ligand_folder, exist_ok=True)
        except:
            print("Warning: Folder already exist!")

    # Get the maximum RMSD value
    max_RMSD = input("Enter the maximum RMSD value (leaving empty means no limit): ").strip()
    if not max_RMSD:
        max_RMSD = "10"

    # Get the number of processes
    num_cores = multiprocessing.cpu_count()
    print(f"Total number of cores of your machine: {num_cores}")

    while True:
        num_processes_str = input("Enter the number of cores you want to use for the operation: ").strip()
        if not num_processes_str.isdigit() or int(num_processes_str) < 1:
            print("Error: Please enter a valid number.")
            continue
        num_processes = 2 * int(num_processes_str)
        break

    # Get the clean option
    clean = False
    while True:
        clean_input = input("Do you want to exclude other ligands in your result? (Y/N): ").strip().lower()
        if clean_input == "y":
            clean = True
            break
        elif clean_input == "n":
            clean = False
            break
        else:
            print("Invalid input. Please enter 'Y' or 'N'.")

    # Get the ligand of interest option
    isLigandOfInterest = False
    print("Not using the ligand of interest may increase the number of proteins related to your ligand.")
    print("For more information: https://www.rcsb.org/docs/exploring-a-3d-structure/ligands")

    while True:
        loi_input = input("Do you want to use the ligand of interest search feature of PDB? (Y/N): ").strip().lower()
        if loi_input == "y":
            isLigandOfInterest = True
            break
        elif loi_input == "n":
            isLigandOfInterest = False
            break
        else:
            print("Invalid input. Please enter 'Y' or 'N'.")

    return ligands, destination, clean, max_RMSD, isLigandOfInterest, num_processes
def process_excel_file(params):
    """
    Helper function to process Excel files using post_possum.
    """
    
    i, destination, ligand, clean = params
    post_possum(i, destination, ligand, clean)

def process_aligned_file(params):
    """
    Helper function to process aligned files using align.
    """
    i, destination = params
    align(i, destination)

def measure_duration(step_name, start_time, end_time, file):
    duration = end_time - start_time
    file.write(f"{step_name} Duration: {duration:.2f} seconds\n")

def main(ligands, destination, clean, max_RMSD, isLigandOfInterest, numberOfProcesses, file, start_pipeline):
    """
    Main function to execute the pipeline of operations.
    """
    start_pdb = time.time()
    # Query PDB for ligand information
    prodict = process_ligands(ligands, isLigandOfInterest)
    end_pdb = time.time()
    measure_duration("PDB Data Collection", start_pdb, end_pdb, file)
    
    start_possum = time.time()
    # Submit the query results to POSSUM
    destination = send_possum_req(prodict, destination, numberOfProcesses)
    end_possum = time.time()
    measure_duration("POSsUM Data Collection", start_possum, end_possum, file)
    
    start_conversion = time.time()
    #destination = destination[:len(destination) - 3] modified used to be uncommented
    if destination.endswith("/")==False: #new line!!!
        destination = destination + "/" #new line!!!
    print(destination)
    for ligand in ligands:
        destination_to_excel = destination + ligand
        # Convert the POSSUM results to Excel files
        destination_to_excel = txt_to_excel(destination_to_excel)
    end_conversion = time.time()
    measure_duration("TXT to Excel Conversion", start_conversion, end_conversion, file)

    # Process Excel files and aligned files using post_possum and align functions
    start_processing = time.time()
    for key in prodict:
        alignment_destination = destination + key + "/ExcelFiles"
        # Process Excel files using post_possum
        excel_files = [f for f in os.listdir(alignment_destination) if f.endswith(".xlsx")]
        post_possum_params = [(i, alignment_destination, key, clean) for i in excel_files]

        with Pool(numberOfProcesses) as p:
            try:
                p.map(process_excel_file, post_possum_params)
            except:
                file.write("Excel file already exists!")
                #print("Excel file already exists!")
        # Process aligned files using align
        aligned_files = [f for f in os.listdir(alignment_destination) if f.endswith(".xlsx")]
        align_params = [(i, alignment_destination) for i in aligned_files]
        file.write("Alignment starts for: ", key)
        #print("Alignment starts for: ", key)
        with Pool(numberOfProcesses) as p:
            p.map(process_aligned_file, align_params)
    end_processing = time.time()
    measure_duration("Data Processing and Alignment", start_processing, end_processing, file)
    file.close()
    overall_duration = time.time() - start_pipeline
    file.write("Pipeline Duration: {:.2f} seconds".format(overall_duration))
    #print("Pipeline Duration: {:.2f} seconds".format(overall_duration))
if __name__ == "__main__":
    file = open("logs.txt", "w")
    start_pipeline = time.time()
    ligand, destination, clean, max_RMSD, isLigandOfInterest, numberOfProcesses = take_input()
    main(ligand, destination, clean, max_RMSD, isLigandOfInterest, numberOfProcesses, file, start_pipeline)


