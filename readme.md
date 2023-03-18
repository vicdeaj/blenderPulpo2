# para instalar gspread en blender:
http://www.codeplastic.com/2019/03/12/how-to-install-python-modules-in-blender/

# loadFiles carga todos los archivos en blender, hace falta:
    1. todas las piezas del pulpo descargadas en piezas_pulpo (organizadas por carpeta = hoja excel)
    2. snapshot dee las piezas en snaphot.py (generado con genSnaphot.py )

# distribucion piezas en la matriz:
    1. Eje x: piezas de la misma hoja
    2. Eje y: piezas en distintas hojas
    3. Eje z: piezas en la misma hoja, cada una de las repeticiones

# run from terminal with output in /tmp/output/image.png
blender myscene.blend --background --python colorPainterAndRender.py
