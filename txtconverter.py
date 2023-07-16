import os
import xlsxwriter


def txt_to_excel(destination):
    arr = os.listdir(destination)
    str_txt = ".txt"
    final_dest = os.path.join(destination, "ExcelFiles")

    for txt_file in arr:
        if str_txt in txt_file:
            name = txt_file[:4]
            file_object = open(os.path.join(destination, txt_file), "r")
            if not os.path.exists(os.path.join(final_dest, name + ".xlsx")):
                with open(os.path.join(final_dest, name + ".xlsx"), "a+") as c:
                    print(f"{name}.txt file converted to xlsx file!")

                workbook = xlsxwriter.Workbook(os.path.join(final_dest, name + ".xlsx"))
                worksheet = workbook.add_worksheet("structure")
                header = "structure1"
                worksheet.set_header(header)

                line_list = file_object.readlines()
                count = len(line_list)

                a = 0
                new_row = []
                pdbid, hetcode, uniprot = "", "", ""

                for num in range(0, count):
                    line = line_list[num]
                    newline = line.split(":") if ":" in line else line.split(" ")

                    if line[0] == "#":
                        split_line = line.split("|")[1:]
                        worksheet.write_row(a, 0, split_line)
                        a += 1
                        if a == 1:
                            for i in range(len(split_line)):
                                new_row.append("")
                            new_row[0] = pdbid
                            new_row[1] = hetcode
                            new_row[9] = uniprot
                            worksheet.write_row(a, 0, new_row)
                            a += 1
                    elif newline[0] == "PDB ID":
                        pdbid = newline[1].strip("\n").strip(" ")
                    elif newline[0] == "HET code":
                        hetcode = newline[1].strip("\n").strip(" ")
                    elif newline[0] == "UniProt ID":
                        uniprot = newline[1].strip("\n").strip(" ")

                workbook.close()

    print("Directory is completed")
    return final_dest


