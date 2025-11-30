import math

class SvgTurtle:
    def __init__(self, width=400, height=400):
        self.width = width
        self.height = height
        self.x = width / 2
        self.y = height / 2
        self.heading = 0  # 0 points right, 90 points up
        self.pen_down = True
        self.color = "black"
        self.lines = []
        self.background_color = "white"

    def bgcolor(self, color):
        self.background_color = color

    def pencolor(self, color):
        self.color = color
    
    def color(self, color):
        self.pencolor(color)

    def penup(self):
        self.pen_down = False

    def pendown(self):
        self.pen_down = True

    def forward(self, distance):
        rad = math.radians(self.heading)
        new_x = self.x + distance * math.cos(rad)
        new_y = self.y - distance * math.sin(rad) # SVG y-axis is down, but standard turtle is up. 
        # Wait, standard turtle: 0 is right, 90 is up.
        # SVG: x increases right, y increases down.
        # So if heading is 0 (right): x + dist, y same. Correct.
        # If heading is 90 (up): x same, y - dist. Correct.
        
        if self.pen_down:
            self.lines.append({
                "x1": self.x, "y1": self.y,
                "x2": new_x, "y2": new_y,
                "color": self.color
            })
        
        self.x = new_x
        self.y = new_y

    def backward(self, distance):
        self.forward(-distance)

    def right(self, angle):
        self.heading -= angle

    def left(self, angle):
        self.heading += angle
    
    def goto(self, x, y):
        # Turtle coordinates are usually centered at 0,0
        # SVG coordinates are 0,0 at top-left.
        # We need to map turtle (0,0) to (width/2, height/2)
        svg_x = x + self.width / 2
        svg_y = self.height / 2 - y
        
        if self.pen_down:
             self.lines.append({
                "x1": self.x, "y1": self.y,
                "x2": svg_x, "y2": svg_y,
                "color": self.color
            })
        self.x = svg_x
        self.y = svg_y

    def save(self, filename):
        svg_content = f'<svg width="{self.width}" height="{self.height}" xmlns="http://www.w3.org/2000/svg" style="background-color:{self.background_color}">\n'
        for line in self.lines:
            svg_content += f'  <line x1="{line["x1"]}" y1="{line["y1"]}" x2="{line["x2"]}" y2="{line["y2"]}" stroke="{line["color"]}" stroke-width="2" />\n'
        svg_content += '</svg>'
        
        with open(filename, "w") as f:
            f.write(svg_content)
        print(f"Saved SVG to {filename}")
