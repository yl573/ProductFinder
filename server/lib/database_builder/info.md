# Reading csv files

Each store has 3 files, 
products.csv, aisles.csv and store.json

### products.csv:
Name
Alias
X Coordinate (relative to origin)
Y Coordinate (relative to origin)
Height (from floor)
Aisle Nodes (node numbers, space separated)

products.csv can have other columns, which will be ignored

The following might make thing easier when recording:

Distance Along Shelf (from the left of the planogram)
X Shelf
Y Shelf
Shelf Orientation

### nodes.csv:
Index
Coordinate (relative to origin, which is arbitrarily defined)
Connected nodes (node numbers, space separated)

### store.json:
{
    Name
    QR Codes [
        {
            Transform (relative transform from store origin, [x, y, z, rx, ry, rz, rw])
        }
    ]
}