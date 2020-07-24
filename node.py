from world.world import *


def get_xy(point):
    if isinstance(point, Node):
        return point.get_xy()
    elif isinstance(point, dict) and 'x' in point and 'y' in point:
        return point['x'], point['y']
    elif (isinstance(point, tuple) or isinstance(point, list)) and len(point) >= 2:
        return point[:2]
    else:
        return point, point


def get_distance_from(point1, point2):
    x1, y1 = get_xy(point1)
    x2, y2 = get_xy(point2)

    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def get_radians_from(point1, point2, from0to2=False):
    x1, y1 = get_xy(point1)
    x2, y2 = get_xy(point2)

    radians = math.atan2(x2 - x1, y2 - y1) / math.pi

    if from0to2:
        return 2 + radians if radians < 0 else radians
    else:
        return radians


def get_angle_from(point1, point2, from0to360=False):
    return round(get_radians_from(point1, point2, from0to360) * 180, 8)


def get_point(point1, angle, distance) -> Node:
    radians = math.radians(angle)
    x = point1.x + (distance * math.sin(radians))
    y = point1.y + (distance * math.cos(radians))
    return Node(x, y)


class Node:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def get_xy(self):
        return self.x, self.y

    def get_distance_from(self, other):
        return get_distance_from(self, other)

    def get_radians_from(self, other, from0to2=False):
        return get_radians_from(self, other, from0to2)

    def get_angle_from(self, other, from0to360=False):
        return get_angle_from(self, other, from0to360)

    def get_point(self, angle, distance) -> Node:
        return get_point(self, angle, distance)

    def __add__(self, other):
        x1, y1 = get_xy(self)
        x2, y2 = get_xy(other)
        return Node(x1 + x2, y1 + y2)

    def __sub__(self, other):
        x1, y1 = get_xy(self)
        x2, y2 = get_xy(other)
        return Node(x1 - x2, y1 - y2)

    def __mul__(self, other):
        x1, y1 = get_xy(self)
        x2, y2 = get_xy(other)
        return Node(x1 * x2, y1 * y2)

    def __truediv__(self, other):
        x1, y1 = get_xy(self)
        x2, y2 = get_xy(other)
        return Node(x1 / x2, y1 / y2)

    def __floordiv__(self, other):
        x1, y1 = get_xy(self)
        x2, y2 = get_xy(other)
        return Node(x1 // x2, y1 // y2)

    def __mod__(self, other):
        x1, y1 = get_xy(self)
        x2, y2 = get_xy(other)
        return Node(x1 % x2, y1 % y2)

    def __pow__(self, power, modulo=None):
        return Node(self.x ** power, self.y ** power)

    def __round__(self, n=None):
        x, y = get_xy(self)
        return Node(round(x, n), round(y, n))

    def __eq__(self, other):
        x1, y1 = get_xy(self)
        x2, y2 = get_xy(other)
        return x1 == x2, y1 == y2

    def __ne__(self, other):
        x1, y1 = get_xy(self)
        x2, y2 = get_xy(other)
        return x1 != x2, y1 != x2

    def __gt__(self, other):
        x1, y1 = get_xy(self)
        x2, y2 = get_xy(other)
        return x1 > x2, y1 > y2

    def __ge__(self, other):
        x1, y1 = get_xy(self)
        x2, y2 = get_xy(other)
        return x1 >= x2, y1 >= y2

    def __lt__(self, other):
        x1, y1 = get_xy(self)
        x2, y2 = get_xy(other)
        return x1 < x2, y1 < y2

    def __le__(self, other):
        x1, y1 = get_xy(self)
        x2, y2 = get_xy(other)
        return x1 <= x2, y1 <= y2

    def __contains__(self, item):
        return item in (self.x, self.y)

    def __len__(self):
        return 2

    def __or__(self, other):
        x1, y1 = get_xy(self)
        x2, y2 = get_xy(other)
        return x1 == x2 or y1 == y2

    def __and__(self, other):
        x1, y1 = get_xy(self)
        x2, y2 = get_xy(other)
        return x1 == x2 and y1 == y2

    def __xor__(self, other=None):
        x1, y1 = get_xy(self)
        x2, y2 = get_xy(other)
        return Node(round(x1, x2), round(y1, y2))

    def __iter__(self):
        return zip([self.x, self.y])

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __repr__(self):
        return f'Node({self.x}, {self.y})'


class PathNode(Node):
    def __init__(self, id: int, u: int, v: int):
        self.id = id
        self.u = u
        self.v = v
        self.x = u * METER
        self.y = v * METER
        self.paths = []

    def __repr__(self):
        ids = f'[{self.id}]' if self.id != -1 else ""
        return f'Node{ids}({self.x}, {self.y})'


class Path:
    def __init__(self, id: int, node1: PathNode, node2: PathNode):
        self.id = id
        self.node1 = node1
        self.node2 = node2

    def get_xy(self):
        angle = self.node1.get_angle_from(self.node2)
        x1, y1 = self.node1.get_point(angle - 90, METER / 2)
        x2, y2 = self.node2.get_point(angle - 90, METER / 2)
        return x1, y1, x2, y2

    def get_angle(self, from0to360=False):
        return get_angle_from(self.node1, self.node2, from0to360)

    def __str__(self):
        return f'({str(self.node1)}, {str(self.node2)})'

    def __repr__(self):
        ids = f'[{self.id}]' if self.id != -1 else ""
        return f'Path{ids}({self.node1.x}, {self.node1.y}, {self.node2.x}, {self.node2.y})'
