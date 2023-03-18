import snaphot

archivos = snaphot.snapshot
for h in archivos:
    for piece in archivos[h]:
        print(piece.id)
