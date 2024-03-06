from math import sin, cos, pi

# Pre-determined vertex placement for the cross-section options
def get_cross_section(width, length, cross_section):
    d = width/5
    width = width/2
    length = length/2

    cross_section_data = {
        "circle": {"vertices": [], "faces": []},

        "square": {"vertices": [
            # Back face
            [-width, -width, -length],  # 0
            [width, -width, -length],  # 1
            [width, width, -length],  # 2
            [-width, width, -length],  # 3
            
            # Front face
            [-width, -width, length],  # 4
            [width, -width, length],  # 5
            [width, width, length],  # 6
            [-width, width, length],  # 7
        ],
        "faces": [
            [0, 1, 2, 3], # Back face
            [4, 5, 6, 7], # Front face
            [3, 2, 6, 7], # Right face
            [0, 1, 5, 4], # Left face
            [2, 1, 5, 6], # Top face
            [0, 3, 7, 4], # Bottom face
        ]},
        
        "I-beam": {"vertices": [
            # Back face
            [-width, -width, -length], # 0
            [width, -width, -length], # 1
            [width, d-width, -length], # 2
            [d/2, d-width, -length], # 3
            [d/2, width-d, -length], # 4
            [width, width-d, -length], # 5
            [width, width, -length], # 6
            [-width, width, -length], # 7
            [-width, width-d, -length], # 8
            [-d/2, width-d, -length], # 9
            [-d/2, d-width, -length], # 10
            [-width, d-width, -length], # 11

            # Front face
            [-width, -width, length], # 12
            [width, -width, length], # 13
            [width, d-width, length], # 14
            [d/2, d-width, length], # 15
            [d/2, width-d, length], # 16
            [width, width-d, length], # 17
            [width, width, length], # 18
            [-width, width, length], # 19
            [-width, width-d, length], # 20
            [-d/2, width-d, length], # 21
            [-d/2, d-width, length], # 22
            [-width, d-width, length] # 23
        ],
        "faces": [
            [3, 4, 9, 10], # Back face middle part
            [5, 6, 7, 8], # Back face left part
            [0, 1, 2, 11], # Back face right part
            [15, 16, 21, 22], # Front face middle part
            [17, 18, 19, 20], # Front face left part
            [12, 13, 14, 23], # Front face right part

            # Caps
            [5, 6, 18, 17],
            [1, 2, 14, 13],
            [7, 8, 20, 19],
            [0, 11, 23, 12],

            # Insides
            [4, 5, 17, 16],
            [2, 3, 15, 14],
            [3, 4, 16, 15],
            [9, 8, 20, 21],
            [11, 10, 22, 23],
            [10, 9, 21, 22],

            # Flat sides
            [7, 6, 18, 19], # Left face
            [0, 1, 13, 12], # Right face
        ]}
    }

    if cross_section == "circle":
        calculate_circle_geometry(width, length, 40, cross_section_data)

    return cross_section_data

def calculate_circle_geometry(width, length, num_sides, cross_section_data):
    # Calculate the coordinates of the vertices along the circumference
    for i in range(num_sides):
        angle = 4 * pi * i / num_sides
        x = cos(angle) * width
        y = sin(angle) * width
        cross_section_data["circle"]["vertices"].append((x, y, length))
        cross_section_data["circle"]["vertices"].append((x, y, -length))

        cross_section_data["circle"]["faces"].append((i, i+1, i+3, i+2))

    # Do the front and back panel
    cross_section_data["circle"]["faces"].append([])
    cross_section_data["circle"]["faces"].append([])
    for i in range(len(cross_section_data["circle"]["vertices"])):
        if i % 2 == 0:
            cross_section_data["circle"]["faces"][-2].append(i)
        else:
            cross_section_data["circle"]["faces"][-1].append(i)
