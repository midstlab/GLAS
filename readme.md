# GLAS: A Tool for Grouping Ligand Alignment Sites

GLAS is a tool developed by researchers at Sabancı University for grouping ligand alignment sites. It aims to streamline and optimize the design of genetically encoded fluorescent biosensors (GEFBs), which are vital tools in nanobiotechnology. GEFBs link fluorescent signal measurements to conformational changes in proteins upon ligand binding, thus providing valuable insights into cellular processes and potential contaminants in nature.

## Overview

The design of nano-biosensors has emerged as a central issue targeted by both biological and materials scientists. GLAS assists this design process by searching the protein data bank to find suitable candidates for the sensing domains in genetically encoded bionanosensor design. The tool implements a comprehensive analysis of protein-ligand interactions and leverages advanced methodologies for efficient data gathering and processing.

## Implementation

GLAS is implemented in Python and uses multiple libraries, including Multiprocessing, OS, Pandas, Beautiful Soup, and JSON. It is designed for Linux/Unix-based systems and utilizes APIs for direct access to the Protein Data Bank, thus bypassing conventional web scraping methods.

## Key Features

- **Data Collection:** GLAS retrieves data from the Protein Data Bank and POSsUM using APIs and HTML requests. It discards empty result files from POSsUM to ensure data integrity. GLAS also leverages multiprocessing to distribute computational tasks across multiple CPU cores, enhancing processing efficiency.
- **Removal of Duplicate Protein Structures:** GLAS removes identical proteins from the PoSSuM results to streamline the experimental process. It obtains amino acid sequences for different chains of the same protein from UniProt, compares these sequences, and retains only the representative protein for downstream analysis. This process ensures the appropriate identification and retention of the most relevant and representative chain among those with identical protein sequences.
- **Binding Site Alignment:** GLAS provides a clear visualization of aligned residues and facilitates the identification of conserved residues within the protein binding sites. It processes the aligned residues provided in the PoSSuM format and forms the binding site sequence, listing the resulting binding sites one by one in a text file.

## Performance

GLAS emphasizes performance optimization for efficient and timely execution of the analysis. During the data collection phase, GLAS uses API calls and HTML requests, significantly reducing the processing time. GLAS further improves its performance by exploiting multiprocessing capabilities, allowing efficient workload distribution across the available CPU cores.

## Applications

GLAS is readily available for download and further inspection on GitHub. Its open-source nature ensures a high degree of accessibility and transparency for the broader scientific community. Its Python-based design not only ensures ease of implementation but also broadens the project's accessibility to a diverse set of researchers. The tool is structured as a series of Python scripts that can be executed on most operating systems, and all dependencies are explicitly listed to replicate the development environment and facilitate ease of use.

## Conclusion

GLAS is designed meticulously to ensure wide applicability, ease of use, and scope for future enhancements. This approach empowers researchers from diverse disciplines to utilize and contribute to the development of the project, thus fostering a collaborative, innovative atmosphere conducive to scientific advancement.

## Funding

Research reported in this publication is supported by the Scientific and Technological Research Council of Turkey (grant number 121Z329).

## Conflict of Interest

The authors declare no conflict of interest.

For more detailed information, please refer to the supplementary information available online.

You can access the GLAS tool at https://github.com/midstlab/GLAS.

# Installation

The following steps provide a guideline on how to install and run GLAS:

## Prerequisites

The GLAS tool requires Python 3.6 or later to run. Python can be downloaded and installed from [here](https://www.python.org/downloads/). 

To check your current Python version, open a terminal window and type:

```
python --version
```

You also need pip (Python's package installer). It is already installed if you are using Python 2 >=2.7.9 or Python 3 >=3.4. If not, you can install pip by following the guidelines [here](https://pip.pypa.io/en/stable/installation/).

## Installing GLAS

1. **Clone the Repository:** Clone the GLAS repository from GitHub to your local machine. Open a terminal window, navigate to your desired directory, and run the following command:

   ```
   git clone https://github.com/midstlab/GLAS.git
   ```
   
2. **Navigate to the Project Directory:** Use the terminal to navigate into the cloned project's directory:

   ```
   cd GLAS
   ```

3. **Install the Required Libraries:** GLAS requires various Python libraries. These libraries are listed in the requirements.txt file. To install these libraries, run the following command in the terminal:

   ```
   pip install -r requirements.txt
   ```

   If you're using a version of Python 3, you might need to use `pip3` instead of `pip`.

4. **Run the Program:** Finally, to run the GLAS tool, use the following command:

   ```
   python main.py
   ```
   
   Or, if you're using Python 3, you might need to use `python3` instead of `python`.

Congratulations! You've now installed and run the GLAS tool. Refer to the GLAS documentation on the GitHub page for detailed usage instructions.

Please note that these instructions assume a general familiarity with using the terminal/command-line interface. If you're using a different interface, the commands may vary slightly.