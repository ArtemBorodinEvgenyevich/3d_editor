import unittest

from main import SoftwareRender
from objects_collection import *


EPS = 1e-6


class Tests(unittest.TestCase):
    def project(self, render, vertexes):
        projected = vertexes @ render.camera.camera_matrix()
        projected = projected @ render.projection.projection_matrix
        projected /= projected[:, -1].reshape(-1, 1)
        projected[(projected > 2) | (projected < -2)] = 0
        projected = projected @ render.projection.to_screen_matrix
        projected = projected[:, :2]
        return projected

    def test_point_in_face_on_plane(self):
        render = SoftwareRender()
        self.vertexes = np.array([[-1, -1, -1, 1], [-1, 1, -1, 1], [1, 1, -1, 1], [1, -1, -1, 1],
                                  [-1, -1, 1, 1], [-1, 1, 1, 1], [1, 1, 1, 1], [1, -1, 1, 1]])

        self.faces = np.array([[0, 1, 2, 3], [0, 1, 5, 4], [0, 4, 7, 3], [3, 2, 6, 7],
                               [1, 5, 6, 2], [4, 5, 6, 7]])

        projection_vertexes = self.project(render, self.vertexes)

        projected_point = self.project(render, np.array([[0, 0, -1, 1]]))

        self.assertEqual(Object3D.check_point_in_face_on_plane(Vector2(*projected_point[0]),
                                                               [projection_vertexes[vert_num] for vert_num in
                                                                self.faces[0]]), True)

    def test_edges_intersetion(self):
        render = SoftwareRender()
        self.vertexes1 = np.array([[-1, -1, -1, 1], [-1, 1, -1, 1], [1, 1, -1, 1], [1, -1, -1, 1]])
        self.vertexes2 = np.array([[-1, -1, -1, 1], [-1, 1, -1, 1], [1, 1, -1, 1], [1, -1, -1, 1]])
        for i in range(4):
            self.vertexes2[i] += [2, 2, 0, 0]

        projection_vertexes1 = self.project(render, self.vertexes1)
        projection_vertexes2 = self.project(render, self.vertexes2)

        self.assertEqual(Object3D.check_edges_intersection(projection_vertexes1, projection_vertexes2), True)

    def test_two_faces_on_plane(self):
        vertexes1 = np.array([[0, 0], [0, 1], [1, 1], [1, 0]])
        vertexes2 = np.array([[0, 0], [5, 6], [6, 6], [6, 5]])

        self.assertEqual(Object3D.check_edges_intersection(vertexes1, vertexes2), True)

    def test_get_face_equation(self):
        vertexes = np.array([[5, 5, 67], [5, 6, 45], [6, 6, 12]])
        res = Object3D.get_face_equation(vertexes)
        ans = [-33, -22, -1.0, 342]

        for i in range(4):
            if abs(res[i] - ans[i]) > EPS:
                self.assertFalse(None)
        self.assertTrue(True)

    def test_check_face_camera_the_same_side_in_camera_space(self):
        render = SoftwareRender()
        self.vertexes = np.array([[-1, -1, -1, 1], [-1, 1, -1, 1], [1, 1, -1, 1], [1, -1, -1, 1],
                                  [-1, -1, 1, 1], [-1, 1, 1, 1], [1, 1, 1, 1], [1, -1, 1, 1]])

        self.faces = np.array([[0, 1, 2, 3], [0, 1, 5, 4], [0, 4, 7, 3], [3, 2, 6, 7],
                               [1, 5, 6, 2], [4, 5, 6, 7]])

        face1 = self.faces[0]
        face2 = self.faces[5]
        P_vertexes = np.array([self.vertexes[i] for i in face1])
        Q_vertexes = np.array([self.vertexes[i] for i in face2])

        self.assertEqual(
            Object3D.check_face_camera_same_side_in_camera_space(Q_vertexes @ render.camera.camera_matrix(),
                                                                 P_vertexes @ render.camera.camera_matrix()), False)

    def test_two_faces_the_same_equation(self):
        render = SoftwareRender()
        plain1 = Plain(render, True, (0, 0, 0))
        plain2 = Plain(render, True, (0, 100, 47))

        equation1 = Object3D.get_face_equation(plain1.vertexes)
        equation2 = Object3D.get_face_equation(plain2.vertexes)

        self.assertEqual(equation1, equation2)
