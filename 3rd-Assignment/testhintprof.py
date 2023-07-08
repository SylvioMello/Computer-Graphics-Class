import sys
import random
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Control points
control_points = []
nodes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]


# Initialize window dimensions
width = 800
height = 600

# Mouse state variables
selected_index = -1
prev_mouse_x = 0
prev_mouse_y = 0

# Curve degree
degree = 1

# Base functions cache
base_functions_cache = {}

def draw_control_points():
    glEnable(GL_POINT_SMOOTH)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glColor3f(0.0, 0.0, 0.0)
    glPointSize(10.0)
    glBegin(GL_POINTS)
    for i, point in enumerate(control_points):
        glVertex2f(point[0], point[1])
        # Draw control point labels
        glRasterPos2f(point[0] + 10, point[1] - 10)
        for char in str(i):
            glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_10, ord(char))
    glEnd()

def draw_sample_curve():
    glEnable(GL_POINT_SMOOTH)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glColor4f(1.0, 0.0, 0.0, 0.2)
    glPointSize(3.0)
    glBegin(GL_POINTS)
    sample = sample_curve(control_points, degree)
    for point in sample:
        glVertex2f(point[0], point[1])
    glEnd()

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    gluOrtho2D(0, width, 0, height)
    draw_control_points()
    draw_sample_curve()
    glFlush()

def reshape(w, h):
    global width, height
    width, height = w, h
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, w, 0, h)

def mouse(button, state, x, y):
    global selected_index, prev_mouse_x, prev_mouse_y
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            # Check if a control point was clicked
            for i, point in enumerate(control_points):
                if abs(point[0] - x) <= 5 and abs(point[1] - (height - y)) <= 5:
                    selected_index = i
                    prev_mouse_x = x
                    prev_mouse_y = height - y
                    break
        elif state == GLUT_UP:
            selected_index = -1

def motion(x, y):
    global selected_index, prev_mouse_x, prev_mouse_y
    if selected_index >= 0:
        dx = x - prev_mouse_x
        dy = height - y - prev_mouse_y
        control_points[selected_index] = (
            control_points[selected_index][0] + dx,
            control_points[selected_index][1] + dy
        )
        prev_mouse_x = x
        prev_mouse_y = height - y
    glutPostRedisplay()

def sample_curve(pts, deg, step=0.01):
    n = len(pts)
    sample = []
    for u in frange(deg, n, step):
        sum_x, sum_y = 0, 0
        for k, p in enumerate(pts):
            w = compute_base_function(k, deg, u)
            sum_x += w * p[0]
            sum_y += w * p[1]
        sample.append((sum_x, sum_y))
    return sample

def compute_base_function(k, d, u):
    if (k, d) in base_functions_cache:
        return base_functions_cache[(k, d)]
    if d == 0:
        result = 1 if k <= u < k + 1 else 0
    else:
        Bk0 = compute_base_function(k, d - 1, u)
        Bk1 = compute_base_function(k + 1, d - 1, u)
        result = ((u - k) / (k + d - k)) * Bk0 + ((k + d + 1 - u) / (k + d + 1 - (k + 1))) * Bk1
    base_functions_cache[(k, d)] = result
    return result

def frange(start, stop, step):
    current = start
    while current <= stop:
        yield current
        current += step

def create_control_points():
    pts = []
    for i in range(6):
        x = 100 + ((width - 200) / 5) * i
        y = height / 2 + (random.random() - 0.5) * (height - 200)
        pts.append((x, y))
    return pts

def keyboard(key, x, y):
    global degree
    if key == b'D' or key == b'd':
        degree += 1 if key == b'D' else -1
        degree = max(1, degree)
        print(f"Degree changed to {degree}")
        clear_base_functions_cache()

def clear_base_functions_cache():
    global base_functions_cache
    base_functions_cache = {}


control_points = create_control_points()
glutInit(sys.argv)
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA)
glutInitWindowSize(width, height)
glutInitWindowPosition(100, 100)
glutCreateWindow("B-Spline Curve")
glutDisplayFunc(display)
glutReshapeFunc(reshape)
glutMouseFunc(mouse)
glutMotionFunc(motion)
glutKeyboardFunc(keyboard)
glClearColor(1.0, 1.0, 1.0, 0.0)
glutMainLoop()

