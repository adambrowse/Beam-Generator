# Carries data of all calculated beams
data = []

# Carries relevant data for calculated beams
filtered_data = []

# Description of the materials
materials = {
    "aluminium": {"colour": (0.3, 0.3, 0.3), "cost": 5100, "density": 2710, "E": 70000000000, "sigma_y": 300000000},
    "steel": {"colour": (0.1, 0.3, 0.5), "cost": 2420, "density": 7850, "E": 200000000000, "sigma_y": 500000000},
    "iron": {"colour": (0.8, 0.2, 0.2), "cost": 450, "density": 7800, "E": 210000000000, "sigma_y": 50000000},
}

# Answer sheet
beam_properties = []

