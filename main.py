import sys
import random
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QCheckBox, QVBoxLayout, QLabel, QScrollArea, QHBoxLayout, QGridLayout, QWidget, QOpenGLWidget, QFrame
from PyQt5.QtCore import pyqtSignal
from OpenGL.GL import *
from cross_section_calculations import *
from data import *
from beam_calculations import *


class SidePanel(QWidget):
    filterChanged = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        # Label for materials
        materials_label = QLabel("Materials")
        layout.addWidget(materials_label)

        # Create boxes for each material
        self.material_check_boxes = {}
        for material in materials.keys():
            check_box = QCheckBox(material.capitalize())
            check_box.setCheckable(True)
            check_box.setChecked(True)
            layout.addWidget(check_box)
            self.material_check_boxes[material] = check_box
            check_box.stateChanged.connect(self.update_viewer)

        # Label for cross sections
        cross_sections_label = QLabel("Cross Sections")
        layout.addWidget(cross_sections_label)

        # Create boxes for each cross section
        self.cross_section_check_boxes = {}
        cross_sections = ["square", "circle", "I-beam"]
        for cross_section in cross_sections:
            check_box = QCheckBox(cross_section.capitalize())
            check_box.setCheckable(True)
            check_box.setChecked(True)
            layout.addWidget(check_box)
            self.cross_section_check_boxes[cross_section] = check_box
            check_box.stateChanged.connect(self.update_viewer)

        # Label for properties
        properties_label = QLabel("Properties")
        layout.addWidget(properties_label)
        
        # Create boxes for each beam property
        self.properties_check_boxes = {}
        properties = ["index", "width", "length", "volume", "mass", "cost", "maximum force", "maximum deflection"]
        for property in properties:
            check_box = QCheckBox(property.capitalize())
            check_box.setCheckable(True)
            layout.addWidget(check_box)
            self.properties_check_boxes[property] = check_box
            check_box.clicked.connect(self.limit_property_checkboxes)

        # Add a button
        self.plot_button = QPushButton("Plot Data")
        layout.addWidget(self.plot_button)
        self.plot_button.clicked.connect(self.plot_data)
        self.plot_button.setEnabled(False)
        
        self.setLayout(layout)
    
    def update_viewer(self):
        filtered_data = [beam for beam in data if
                        beam["material"] in self.checked_materials() and
                        beam["cross_section"] in self.checked_cross_sections()]
        self.filterChanged.emit(filtered_data)

    def checked_materials(self):
        return [material for material, checkbox in self.material_check_boxes.items() if checkbox.isChecked()]

    def checked_cross_sections(self):
        return [cross_section for cross_section, checkbox in self.cross_section_check_boxes.items() if checkbox.isChecked()]

    def limit_property_checkboxes(self):
        checked_boxes = [checkbox for checkbox in self.properties_check_boxes.values() if checkbox.isChecked()]
        if len(checked_boxes) > 2:
            last_checked_box = checked_boxes[-1]
            last_checked_box.setChecked(False)
        
        checked_boxes_count = sum(checkbox.isChecked() for checkbox in self.properties_check_boxes.values())
        self.plot_button.setEnabled(checked_boxes_count >= 2)

    def plot_data(self):
        new_list = []

        filtered_data = [beam for beam in data if
            beam["material"] in self.checked_materials() and
            beam["cross_section"] in self.checked_cross_sections()]

        # Filter the beam_properties
        indexes = [beam["index"]-1 for beam in filtered_data]
        print(indexes)
        filtered_beam_properties = [beam_properties[index] for index in indexes]

        print(filtered_data)
        print(filtered_beam_properties)

        # Merge dictionaries
        for data_item, properties_item in zip(filtered_data, filtered_beam_properties):
            combined_dict = {**data_item, **properties_item}
            new_list.append(combined_dict)

        # Fetch data
        checked_properties = [property for property, checkbox in self.properties_check_boxes.items() if checkbox.isChecked()]

        property_x, property_y = checked_properties

        x_data = [beam[property_x] for beam in new_list]
        y_data = [beam[property_y] for beam in new_list]

        # Create plot
        plt.scatter(x_data, y_data)
        plt.xlabel(property_x.replace(' ', '_').capitalize())
        plt.ylabel(property_y.replace(' ', '_').capitalize())
        plt.title(f'{property_x.capitalize()} vs {property_y.capitalize()} Plot')
        plt.show()


class BeamViewer(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWidgetResizable(True)

        inner_widget = QWidget()
        self.layout = QGridLayout(inner_widget)
        self.setWidget(inner_widget)

        self.beam_widgets = []
        self.filtered_data = []

        # Generate N beams
        for i in range(21):
            data.append(self.beam_generator(i+1))

        # Add beam widgets
        self.add_beam_widgets(data)

    def add_beam_widgets(self, beams):
        for i, beam in enumerate(beams):
            beam_info = BeamInfo(beam)
            self.beam_widgets.append(beam_info)
            self.layout.addWidget(beam_info, i // 3, i % 3)

    def beam_generator(self, i):
        width = random.uniform(0.2, 0.4)
        length = random.uniform(1, 5)
        material = random.choice(list(materials.keys()))
        cross_section = random.choice(["square", "circle", "I-beam"])

        return {"index": i, "width": width, "length": length, "material": material, "cross_section": cross_section}

    def update_viewer_with_filtered_data(self, filtered_data):
        self.filtered_data = filtered_data
        self.update_view()

    def update_view(self):
        visible_indices = []
        for beam_widget in self.beam_widgets:
            beam_widget.hide()

        # Show beam widgets for filtered data and collect visible indices
        for beam in self.filtered_data:
            index = beam["index"] - 1
            visible_indices.append(index)
            self.beam_widgets[index].show()

        # Place visible widgets together
        row, col = 0, 0
        for i, beam_widget in enumerate(self.beam_widgets):
            if i in visible_indices:
                self.layout.addWidget(beam_widget, row, col)
                col += 1
                if col >= 3:
                    col = 0
                    row += 1


class BeamInfo(QFrame):
    def __init__(self, beam, parent=None):
        super().__init__(parent)
        self.beam = beam

        self.setMaximumHeight(225)

        # Calculate and record beam properties
        self.get_beam_properties()

        properties = self.format_beam_properties(beam_properties[-1])

        fact_sheet = QLabel(properties, self)
        beam_image = Beam(beam)

        layout = QHBoxLayout(self)
        layout.addWidget(beam_image)
        layout.addWidget(fact_sheet)
        self.setLayout(layout)

        # Set a border around layout
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.setStyleSheet("QFrame { border: 1px solid gray; }")
    
    def get_beam_properties(self):
        width = self.beam["width"]
        length = self.beam["length"]
        cross_section = self.beam["cross_section"]
        material = self.beam["material"]

        # Get properties of beam
        sigma_y = materials[material]["sigma_y"]
        E = materials[material]["E"]
        density = materials[material]["density"]
        cost_per_m3 = materials[material]["cost"]
        I, area = second_moment_area(width, cross_section)

        # Input properties
        volume = area * length
        mass = density * volume
        cost = volume * cost_per_m3
        max_force = f_max(sigma_y, I, length, width/2)
        delta = max_tip_deflection(max_force, E, I, length)

        beam_properties.append({"volume": volume, "mass": mass, "cost": cost, "maximum force": max_force, "maximum deflection": delta})

    def format_beam_properties(self, beam_properties):
        formatted_properties = ""
        for property_name, property_value in self.beam.items():
            if isinstance(property_value, str):
                formatted_properties += f"{property_name.capitalize()}: {property_value}\n"
            else:
               formatted_properties += f"{property_name.capitalize()}: {property_value:.2g}\n"


        for property_name, property_value in beam_properties.items():
            formatted_properties += f"{property_name.capitalize()}: {property_value:.2g}\n"
        
        return formatted_properties


class Beam(QOpenGLWidget):
    def __init__(self, beam, parent=None):
        super().__init__(parent)
        self.beam = beam
        self.setMinimumSize(200, 200)
        self.setMaximumSize(200, 200)

    def initializeGL(self):
        # Initialize the lighting
        glClearColor(0, 0, 0, 1)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glEnable(GL_CULL_FACE)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE)

        # Disable lighting
        glDisable(GL_LIGHTING)

        # Set the initial rotation
        glRotatef(90, 0, -0.5, 1)

    def resizeGL(self, width, height):
        # Set the viewport and projection matrix
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect_ratio = width / height
        glOrtho(-aspect_ratio, aspect_ratio, -1, 1, -1, 1)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        super().paintGL()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.draw_beam()

    def draw_beam(self):
        glTranslatef(0, 0, 0)
        glLineWidth(3.0)
 
        # Define dimensions and colours
        set_length = 2
        scale = self.beam["length"]/set_length
        width = self.beam["width"]/scale
        length = set_length
        cross_section = self.beam["cross_section"]
        material = self.beam["material"]
        colour = materials[material]["colour"]

        # Define the shape given the cross section and the dimensions
        cross_section_data = get_cross_section(width, length, cross_section)
        vertices = cross_section_data[cross_section]["vertices"]
        faces = cross_section_data[cross_section]["faces"]
        
        # Draw the faces of the shape
        glColor3f(*colour)
        for face in faces:
            glBegin(GL_POLYGON)
            for vertex_index in face:
                glVertex3fv(vertices[vertex_index])
            glEnd()

        # Highlight the edges
        glColor3f(1, 1, 1)
        for face in faces:
            glBegin(GL_LINES)
            for i, vertex_index in enumerate(face):
                glVertex3fv(vertices[vertex_index])
                if i == len(face) - 1:
                    glVertex3fv(vertices[face[0]])
                else:
                    glVertex3fv(vertices[face[i + 1]])
            glEnd()
        

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Make the app
        self.setWindowTitle('Generative beam analysis tool')
        self.setGeometry(100, 100, 1600, 800)

        # Create the central widget
        central_widget = QWidget()
        central_layout = QHBoxLayout()
        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)

        # Create the Side Panel
        side_panel = SidePanel()
        central_layout.addWidget(side_panel)
        side_panel.setMinimumWidth(int(self.width() * 0.2))

        # Create the Beam Viewer
        beam_viewer = BeamViewer()
        central_layout.addWidget(beam_viewer)
        beam_viewer.setMinimumWidth(int(self.width() * 0.8))

        # Connect signals and slots
        side_panel.filterChanged.connect(beam_viewer.update_viewer_with_filtered_data)


# Call the app
app = QApplication(sys.argv)

# Create the main window
main_window = MainWindow()
main_window.show()

# Let's go!
sys.exit(app.exec_())