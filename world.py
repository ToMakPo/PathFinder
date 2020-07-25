from __future__ import annotations

from tkinter import Tk, Canvas, Event
from numpy import random as np_rand

from my_globals import *
from node import *

METER = 10
LANE_WIDTH = METER * 2
PATH_COLOR = '#656565'
ACTIVE_COLOR = '#858585'


class World:
    def __init__(self, title: str = 'Path Finder', width: int = 1000, height: int = 800, seed: int = -1):
        self.root = Tk()
        self.root.title(title)
        self.canvas: Canvas = Canvas(self.root)
        self.canvas.pack()

        self.rand: np_rand = np_rand

        self.width = -1
        self.height = -1
        self.set_size(width, height)

        self.seed: int = -1
        self.active_seed: int = -1
        self.set_seed(seed)

        self.path_nodes: {int: Node} = {}
        self.paths: {int: Path} = {}

        self.creating_new_path = False
        self.circle = None
        self.line = None
        self.last_node = None

        self.route_start = None
        self.route_end = None

        self.built = False

    def set_seed(self, seed: int = None):
        if seed is not None:
            self.seed = seed

        if self.seed == -1:
            self.active_seed = np_rand.randint(0, MAX32)
        else:
            self.active_seed = clamp(self.seed)
        self.built = False

    def set_size(self, width: int = None, height: int = None):
        if width is not None:
            self.width = clamp(width, 100)
        if height is not None:
            self.height = clamp(height, 100)
        self.built = False

    def add_path_node(self, u, v) -> PathNode:
        while True:
            id = self.rand.randint(0, MAX32)
            if id not in self.path_nodes:
                node = PathNode(id, u, v)
                self.path_nodes[id] = node
                self.built = False
                return node

    def add_path(self, node1: PathNode, node2: PathNode) -> (Path, Path):
        while True:
            id = self.rand.randint(0, MAX32)
            if id not in self.paths:
                path1 = Path(id, node1, node2)
                node1.paths[id] = path1

                path2 = Path(id, node2, node1)
                node2.paths[id] = path2

                self.paths[id] = (path1, path2)
                return path1, path2

    def get_node_at(self, x, y) -> Node:
        for node in self.path_nodes.values():
            if node.x == x and node.y == y:
                return node

    def get_nodes_near(self, x, y, distance):
        for node in self.path_nodes.values():
            if node.get_distance((x, y)) <= distance:
                yield node

    def get_nearest_path_node(self, point) -> Node:
        nearest: PathNode = None
        max_distance = MAX32
        point = get_xy(point)
        for node in self.path_nodes.values():
            distance = node.get_distance_from(point)
            if distance < max_distance:
                max_distance = distance
                nearest = node
        return nearest

    def build(self):
        if not self.built:
            self.canvas.destroy()
            self.canvas = Canvas(self.root, width=self.width, height=self.height, background="#DDDDDD")
            self.canvas.pack()

            def make_paths():
                # draw paths
                for path in self.paths.values():
                    x1, y1 = path[0].node1
                    x2, y2 = path[1].node1
                    self.canvas.create_line(x1, y1, x2, y2, width=LANE_WIDTH * 2, fill=PATH_COLOR)

            def make_lines():
                # draw lines
                for path in self.paths.values():
                    n1: PathNode = path[0].node1
                    n2: PathNode = path[1].node1

                    a1 = n1.get_angle_from(n2)
                    a2 = n2.get_angle_from(n1)
                    o1 = n1.get_point(a1, LANE_WIDTH * (1.75 if len(n1.paths) > 2 else 0))
                    o2 = n2.get_point(a2, LANE_WIDTH * (1.75 if len(n2.paths) > 2 else 0))
                    if len(n1.paths) > 2:
                        o1_1 = o1.get_point(a1 - 90, LANE_WIDTH)
                        o1_2 = o1.get_point(a1 + 90, LANE_WIDTH)
                        self.canvas.create_line(*o1_1, *o1_2, width=METER * 0.2, fill='white', dash=(1, 1))
                    if len(n2.paths) > 2:
                        o2_1 = o2.get_point(a2 - 90, LANE_WIDTH)
                        o2_2 = o2.get_point(a2 + 90, LANE_WIDTH)
                        self.canvas.create_line(*o2_1, *o2_2, width=METER * 0.2, fill='white', dash=(1, 1))

                    self.canvas.create_line(*o1, *o2, width=METER * 0.1, fill='white', dash=(10, 5))

            def make_nodes():
                # draw nodes
                for node in self.path_nodes.values():
                    x1 = node.x - LANE_WIDTH
                    y1 = node.y - LANE_WIDTH
                    x2 = node.x + LANE_WIDTH
                    y2 = node.y + LANE_WIDTH
                    self.canvas.create_oval(x1, y1, x2, y2, fill=PATH_COLOR, width=0, activefill=ACTIVE_COLOR,
                                            tag="path_node")

                def start_new(event):
                    mouse = Node(event.x, event.y)
                    self.last_node = self.get_nearest_path_node(mouse)
                    self.creating_new_path = True
                    coords = *(self.last_node - LANE_WIDTH), *(self.last_node + LANE_WIDTH)
                    self.canvas.create_oval(*coords, fill=ACTIVE_COLOR, width=0)
                    self.line = self.canvas.create_line(*self.last_node, *mouse, width=LANE_WIDTH * 2,
                                                        fill=ACTIVE_COLOR)
                    coords = *(mouse - LANE_WIDTH), *(mouse + LANE_WIDTH)
                    self.circle = self.canvas.create_oval(*coords, fill=ACTIVE_COLOR, width=0, tag='new_node')

                def drag(event):
                    if self.creating_new_path:
                        mouse = Node(event.x, event.y)
                        self.canvas.coords(self.line, *self.last_node, *mouse)
                        self.canvas.coords(self.circle, *(mouse - LANE_WIDTH), *(mouse + LANE_WIDTH))

                def place_new(event):
                    self.creating_new_path = False
                    mouse = Node(event.x, event.y)
                    nearest = self.get_nearest_path_node(mouse)
                    if mouse.get_distance_from(nearest) > LANE_WIDTH:
                        new_node = self.add_path_node(event.x / METER, event.y / METER)
                        self.add_path(self.last_node, new_node)
                    else:
                        self.add_path(self.last_node, nearest)

                    self.built = False
                    self.draw()

                def on_hover(event: Event):
                    mouse = Node(event.x, event.y)
                    # nearest = self.get_nearest_path_node(mouse)

                def on_leave(event):
                    mouse = Node(event.x, event.y)
                    # nearest = self.get_nearest_path_node(mouse)

                self.canvas.tag_bind('path_node', '<Enter>', on_hover)
                self.canvas.tag_bind('path_node', '<Leave>', on_leave)
                self.canvas.tag_bind('path_node', '<Button-1>', start_new)
                self.canvas.tag_bind('new_node', '<Button-1>', place_new)
                self.canvas.bind('<Motion>', drag)

            make_paths()
            make_nodes()
            make_lines()
            self.draw_route()

    def draw(self):
        self.build()

    def draw_route(self, start: PathNode = None, end: PathNode = None):
        if start is not None:
            self.route_start = start
        if end is not None:
            self.route_end = end

        if self.route_start is not None and self.route_end is not None:
            route: Route = self.route_start.find_shortest_route(self.route_end)
            path_width = LANE_WIDTH / 3
            radius = path_width / 2
            path_color = '#BADA55'

            cnt = len(route.nodes)
            n1 = a1 = o1 = 0
            for n in range(cnt):
                if n == 0:
                    n1 = route.nodes[n]
                    n2 = route.nodes[n + 1]
                    a1 = get_angle(n1, n2)
                    o1 = get_point(get_point(n1, a1, METER), a1 - 90, LANE_WIDTH / 2)
                    self.canvas.create_oval(*o1-radius, *o1+radius, fill=path_color, width=0)
                elif n < cnt - 1:
                    n1 = route.nodes[n]
                    n2 = route.nodes[n + 1]
                    a0 = a1
                    a2 = get_angle(n1, n2)
                    a1 = (a0 + a2) / 2
                    o0 = o1
                    o1 = get_point(n1, a1 - 90, LANE_WIDTH / 2)
                    self.canvas.create_oval(*o1-radius, *o1+radius, fill=path_color, width=0)
                    self.canvas.create_line(*o0, *o1, fill=path_color, width=path_width)
                else:
                    n1 = route.nodes[n]
                    a0 = a1
                    o0 = o1
                    o1 = get_point(n1, a0 - 90, LANE_WIDTH / 2)
                    self.canvas.create_oval(*o1-radius, *o1+radius, fill=path_color, width=0)
                    self.canvas.create_line(*o0, *o1, fill=path_color, width=path_width)


if __name__ == '__main__':
    world = World(width=1720, height=1400)
    g = 5
    points = [[5*g, 5*g], [20*g, 5*g], [5*g, 15*g], [20*g, 15*g], [15*g, 25*g], [30*g, 20*g], [30*g, 25*g]]
    node_list = [world.add_path_node(*point) for point in points]
    pairs = [[0, 1], [0, 2], [1, 3], [2, 3], [2, 4], [3, 4], [3, 5], [4, 6], [5, 6]]
    paths = [world.add_path(*[node_list[pair[0]], node_list[pair[1]]]) for pair in pairs]
    # [print(path[0].node1.id, path[0].node2.id) for path in paths]
    # [print(node) for node in node_list]
    # route = node_list[0].find_shortest_route(node_list[-1])
    world.draw()
    world.draw_route(node_list[0], node_list[-1])
    world.root.mainloop()
