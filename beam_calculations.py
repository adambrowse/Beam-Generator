from math import pi

# Find the second moment of area for a given geometry
def second_moment_area(width, cross_section):
    if cross_section == "square":
        area = width**2
        return (width**4)/12, area
    elif cross_section == "circle":
        area = pi*(width/2)**2
        return(pi*width**4)/4, area
    elif cross_section == "I-beam":
        d = width/5
        height = width
        width = width - 2*d
        area = 2*d*height + width*d
        return(2*d*height**3 + width*d**3)/12, area
    else:
        return -1

# Find maximum allowable force on beam
def f_max(sigma_y, I, L, c):
    # Find maximum force applicable
    return (sigma_y*I)/(L*c)

# Find tip deflection at F_max
def max_tip_deflection(F, E, I, L):
    return (F*L**3)/(3*E*I)
