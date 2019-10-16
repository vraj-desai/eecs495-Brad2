import turtle

# coordinate representation of sensor locations and angle of measurement
# camera located at 0, 0
# max sensor measurement is 400cm
# drawing view scaled down x2
s1_x, s1_y, s1_a = -50, 0, 225
s2_x, s2_y, s2_a = -25, 0, 270
s3_x, s3_y, s3_a = 25, 0, 270
s4_x, s4_y, s4_a = 50, 0, 315
hcsr04_range = 200
obstacle_range = 50

def calculate_object_position(t, x, y, a, d):
    """Calculates coordinates of object given the sensor coordinates,
       angle, and the distance measurement."""
    original_x, original_y = t.pos()
    t.penup()
    t.setposition(x, y)
    t.seth(a)
    t.forward(d)
    object_x, object_y = t.pos()
    t.setposition(original_x, original_y)
    return object_x, object_y


def draw_object(t, x, y, d):
    """Draws sensed object as a dot. Objects considered obstacles
       are drawn in red."""
    t.penup()
    t.setposition(x, y)
    if d < obstacle_range:
        t.color("red")
    t.pendown()
    t.dot(10)
    t.penup()
    t.color("black")


def draw_objects(t, d1, d2, d3, d4):
    """Draws all objects."""
    x1, y1 = calculate_object_position(t, s1_x, s1_y, s1_a, d1)
    x2, y2 = calculate_object_position(t, s2_x, s2_y, s2_a, d2)
    x3, y3 = calculate_object_position(t, s3_x, s3_y, s3_a, d3)
    x4, y4 = calculate_object_position(t, s4_x, s4_y, s4_a, d4)
    draw_object(t, x1, y1, d1)
    draw_object(t, x2, y2, d2)
    draw_object(t, x3, y3, d3)
    draw_object(t, x4, y4, d4)
    draw_line_from_sensor(t, s1_x, s1_y, s1_a, d1)
    draw_line_from_sensor(t, s2_x, s2_y, s2_a, d2)
    draw_line_from_sensor(t, s3_x, s3_y, s3_a, d3)
    draw_line_from_sensor(t, s4_x, s4_y, s4_a, d4)


def draw_line_from_sensor(t, x, y, a, d):
    """Draws a line along the sensor's measurement path."""
    t.penup()
    t.setposition(x, y)
    t.seth(a)
    t.pendown()
    if d < obstacle_range:
        t.color("red")
    else:
        t.color("blue")
    t.forward(d)
    t.penup()
    t.color("black")


def draw_measurement_boundary(t, bound):
    """Draws a boundary representing the area of sensor measurement."""
    t.penup()
    t.setposition(s1_x, s1_y)
    s1max_x, s1max_y = calculate_object_position(t, s1_x, s1_y, s1_a, bound)
    t.pendown()
    t.goto(s1max_x, s1max_y)
    s2max_x, s2max_y = calculate_object_position(t, s2_x, s2_y, s2_a, bound)
    t.pendown()
    t.goto(s2max_x, s2max_y)
    s3max_x, s3max_y = calculate_object_position(t, s3_x, s3_y, s3_a, bound)
    t.pendown()
    t.goto(s3max_x, s3max_y)
    s4max_x, s4max_y = calculate_object_position(t, s4_x, s4_y, s4_a, bound)
    t.pendown()
    t.goto(s4max_x, s4max_y)
    t.goto(s4_x, s4_y)
    t.penup()


if __name__ == '__main__':
    """Main function."""
    s = turtle.Screen()
    t = turtle.Turtle()
    t.ht()
    # draw boundaries for max sensor measurement and obstacle detection
    draw_measurement_boundary(t, hcsr04_range)
    draw_measurement_boundary(t, obstacle_range)
    # draw sensed objects
    draw_objects(t, 100, 103, 50, 20)
    turtle.getscreen()._root.mainloop()