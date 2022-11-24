from camera import *
from projection import *

from objects_collection import *
from control import *
import json
import sys
from buttons import *


class SoftwareRender:
    def __init__(self):
        pg.init()
        self.RES = self.WIDTH, self.HEIGHT = 1920, 1080
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
        self.FPS = 60
        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        self.create_objects()
        self.plains_intersection = False

    def spawn_cube(self):
        self.objects.append(Cube(self, True, (0, 0, 0)))

    def spawn_tetrahedron(self):
        self.objects.append(Tetrahedron(self, True, (0, 0, 0)))

    def spawn_plain(self):
        self.objects.append(Plain(self, True, (0, 0, 0)))

    def destroy(self):
        for i in range(len(self.objects)):
            if self.objects[i].is_highlighted:
                self.objects.pop(i)
                return

    def plains_intersection_change_mode(self):
        self.plains_intersection = not self.plains_intersection

    def create_objects(self):
        self.camera = Camera(self, [0, 0, -30], True)
        self.projection = Projection(self)
        self.objects = []
        self.load_dump(self)
        self.camera.camera_rotate_scene_x(-math.pi / 4 * 0.1)
        self.buttons = [Button(50, 50, 70, 40, "cube", self.spawn_cube, self), Button(50, 100, 70, 50, "tetr", self.spawn_tetrahedron, self),
                        Button(50, 250, 100, 50, "destroy", self.destroy, self), Button(50, 150, 70, 50, "plain", self.spawn_plain, self),
                        Button(50, 950, 350, 50, "plains intersection OFF", self.plains_intersection_change_mode, self, new_message="plains intersection ON")]

    def update(self):
        self.screen.fill(pg.Color('darkslategray'))

        for btn in self.buttons:
            btn.check_click()
            btn.draw()
        Object3D.update(self, self.objects)
        Control.update(self, self.objects)
        Object3D.draw_objects(self, self.objects)

    def run(self):
        while True:
            self.clock.tick(self.FPS)
            self.update()

            for i in pg.event.get():
                if i.type == pg.QUIT:
                    self.make_dump()
                    sys.exit()
            pg.display.set_caption(str(self.clock.get_fps()))
            pg.display.update()

    def make_dump(self):
        data = {}
        for object in self.objects:
            if str(object) not in data:
                data[str(object)] = [object.get_data()]
            else:
                data[str(object)].append(object.get_data())

        with open("data.json", 'w') as f:
            json.dump(data, f)

    def load_dump(self, render):
        objects_dict = {"cube": Cube,
                        "plain": Plain,
                        "tetrahedron": Tetrahedron}

        with open("data.json") as f:
            data_str = f.readline()
            if data_str == "":
                return
            t = json.loads(data_str)

            for obj, info in t.items():
                for i in range(len(info)):
                    new_obj = objects_dict[obj](render, True, (0, 0, 0))
                    transform_matrix = info[i]['matrix']
                    verts = info[i]['vertexes']
                    new_obj.transform_matrix = np.array(list(map(np.array, transform_matrix)))
                    new_obj.vertexes = np.array(list(map(np.array, verts)))

                    self.objects.append(new_obj)


if __name__ == '__main__':
    app = SoftwareRender()
    app.run()
