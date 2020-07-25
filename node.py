from __future__ import annotations

from world import *


def get_xy(point):
    if isinstance(point, Node):
        return point.get_xy()
    elif isinstance(point, dict) and 'x' in point and 'y' in point:
        return point['x'], point['y']
    elif (isinstance(point, tuple) or isinstance(point, list)) and len(point) >= 2:
        return point[:2]
    else:
        return point, point


def get_distance(point1, point2):
    x1, y1 = get_xy(point1)
    x2, y2 = get_xy(point2)

    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


# def get_radians(point1, point2, from0to2=False):
#     x1, y1 = get_xy(point1)
#     x2, y2 = get_xy(point2)
#
#     radians = math.atan2(x2 - x1, y2 - y1) / math.pi
#
#     if from0to2:
#         return 2 + radians if radians < 0 else radians
#     else:
#         return radians

def get_radians(point1, point2, from0to2=False):
    x1, y1 = get_xy(point1)
    x2, y2 = get_xy(point2)

    radians = math.atan2(x2 - x1, y2 - y1) / math.pi

    if from0to2:
        return 2 + radians if radians < 0 else radians
    else:
        return radians


def get_angle(point1, point2, from0to360=False):
    return round(get_radians(point1, point2, from0to360) * 180, 8)


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
        return get_distance(self, other)

    def get_radians_from(self, other, from0to2=False):
        return get_radians(self, other, from0to2)

    def get_angle_from(self, other, from0to360=False):
        return get_angle(self, other, from0to360)

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
        return x1 == x2 and y1 == y2

    def __ne__(self, other):
        x1, y1 = get_xy(self)
        x2, y2 = get_xy(other)
        return x1 != x2 and y1 != x2

    def __gt__(self, other):
        x1, y1 = get_xy(self)
        x2, y2 = get_xy(other)
        return x1 > x2 and y1 > y2

    def __ge__(self, other):
        x1, y1 = get_xy(self)
        x2, y2 = get_xy(other)
        return x1 >= x2 and y1 >= y2

    def __lt__(self, other):
        x1, y1 = get_xy(self)
        x2, y2 = get_xy(other)
        return x1 < x2 and y1 < y2

    def __le__(self, other):
        x1, y1 = get_xy(self)
        x2, y2 = get_xy(other)
        return x1 <= x2 and y1 <= y2

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

    def __hash__(self):
        return self.x, self.y

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __repr__(self):
        return f'Node({self.x}, {self.y})'


class PathNode(Node):
    def __init__(self, id: int, u: int, v: int):
        super().__init__(u * METER, v * METER)
        self.id = id
        self.u = u
        self.v = v
        self.paths = {}

    def find_shortest_route(self, target: PathNode) -> Route:
        all_nodes = [self]
        new_nodes = [self]
        routes = {'start': {}, 'end': {}}

        while len(new_nodes):
            old_nodes = new_nodes.copy()
            new_nodes.clear()
            for node in old_nodes:
                for path in node.paths.values():
                    route = path.find_route(target)

                    if route.start not in routes['start']:
                        routes['start'][route.start] = {route.end: route}
                    else:
                        routes['start'][route.start][route.end] = route

                    if route.end not in routes['end']:
                        routes['end'][route.end] = {route.start: route}
                    else:
                        routes['end'][route.end][route.start] = route

                    if route.end not in all_nodes:
                        all_nodes.append(route.end)
                        new_nodes.append(route.end)

        def update_chart(node: PathNode, distance=None, previous: PathNode = None, have_visited=None):
            if node in chart:
                if distance is not None:
                    chart[node]['distance'] = distance
                if previous is not None:
                    chart[node]['previous'] = previous
                if node in unvisited and have_visited is not None and have_visited:
                    del unvisited[node]
            else:
                info = {'distance': distance, 'previous': previous}
                chart[node] = info
                unvisited[node] = info

        chart = {}
        unvisited = {}

        def next():
            return sorted(unvisited.items(), key=lambda x: x[1]['distance'])[0][0]

        update_chart(self, 0)
        [update_chart(node, MAX32) for node in all_nodes[1:]]

        while len(unvisited):
            node = next()
            for route in routes['start'][node].values():
                old_dist = chart[route.end]['distance']
                new_dist = chart[route.start]['distance'] + route.length
                if new_dist < old_dist:
                    update_chart(route.end, new_dist, route.start)
            update_chart(node, have_visited=True)

        def join_routes(route1: Route, route2: Route):
            if route1 is None and route2 is None:
                return None
            if route1 is None:
                return route2
            if route2 is None:
                return route1

            if route1.end == route2.start:
                route1.end = route2.end
                route1.nodes = route1.nodes + route2.nodes[1:]
                route1.length += route2.length
            elif route1.start == route2.end:
                route1.start = route2.start
                route1.nodes = route2.nodes + route1.nodes[1:]
                route1.length += route2.length
            return route1

        previous: PathNode = target
        info = chart[previous]
        shortest: Route = None
        while info['previous'] is not None:
            current: Route = routes['start'][info['previous']][previous]
            shortest = join_routes(shortest, current)
            previous = info['previous']
            info = chart[previous]

        return shortest

    def __repr__(self):
        ids = f'[{self.id}]' if self.id != -1 else ""
        return f'PathNode{ids}({self.x}, {self.y})'

    def __hash__(self):
        return self.id if self.id != -1 else super().__hash__()


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
        return get_angle(self.node1, self.node2, from0to360)

    @property
    def length(self):
        return self.node1.get_distance_from(self.node2)

    def __str__(self):
        return f'({str(self.node1)}, {str(self.node2)})'

    def __repr__(self):
        ids = f'[{self.id}]' if self.id != -1 else ""
        return f'Path{ids}({self.node1.x}, {self.node1.y}, {self.node2.x}, {self.node2.y})'

    def find_route(self, target: PathNode, route: Route = None):
        if route is None:
            route = Route(self)
        else:
            route.add_path(self)

        if self.node2 == target:
            return route

        count = len(route.end.paths)

        if count == 2:
            for id, path in route.end.paths.items():
                if id != self.id:
                    route = path.find_route(target, route)
        return route


class Route:
    def __init__(self, path: Path):
        if path is not None:
            self.start: PathNode = path.node1
            self.end: PathNode = path.node2
            self.length = path.length
            self.nodes = [path.node1, path.node2]

    def add_path(self, path: Path):
        self.end = path.node2
        self.length += path.length
        self.nodes.append(path.node2)

    def __len__(self):
        return len(self.nodes)

    def __repr__(self):
        return f'Route(start:{self.start}, end:{self.end}, length:{self.length}, nodes:{len(self.nodes)})'

    def __str__(self):
        return f'({self.start}, {self.end})'
