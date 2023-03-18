from dataclasses import dataclass
import snaphot
import gspread

gc = gspread.service_account()
sh = gc.open("3DPrinterPartyMadrid2023_Reto")

hojas = ["TA", "TB", "TC", "TD", "TE", "BASE", "H3", "H4", "H5","H6","H7","H8", "H9","H10","H11","BOCA" ]
@dataclass
class Archivo:
    nombre:str
    id:str
    status:str

def get_pieces(spreadheetName):
    worksheet = sh.worksheet(spreadheetName)
    archievesName_list = worksheet.get("B20:B200")
    statusName_list = worksheet.get("E20:E200")
    archivos = []
    for i in range(len(archievesName_list)):
        name = archievesName_list[i][0]
        try:
            if (len(statusName_list[i])) > 0:
                status = statusName_list[i][0]
            else:
                status = "null"
        except IndexError:
            status = "null"

        id = name+str(i)

        archivos.append(Archivo(name, id, status))


    return archivos

def getDocumento():

    archivos = {}
    for hoja in hojas:
        archivos[hoja] = get_pieces(hoja)
    return archivos

if __name__ == "__main__":
    archivos = snaphot.snapshot
    for h in archivos:
        print(archivos[h])

