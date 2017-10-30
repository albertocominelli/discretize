import unittest
import os
import numpy as np
import discretize


def compare_meshes(mesh0, mesh1):

    # check some basic properties
    assert mesh0.nC == mesh1.nC , (
        'Number of cells not the same, {} != {}'.format(mesh0.nC, mesh1.nC)
    )

    assert (mesh0.x0 == mesh1.x0).all(), (
        'x0 different. {} != {}'.format(mesh0.x0, mesh1.x0)
    )

    assert (mesh0.nE == mesh1.nE)
    assert (mesh0.nF == mesh1.nF)
    assert (mesh0.nN == mesh1.nN)

    if hasattr(mesh0, 'vnC'):
        assert (mesh0.vnC == mesh1.vnC).all()
        assert (mesh0.vnE == mesh1.vnE).all()
        assert (mesh0.vnF == mesh1.vnF).all()
        assert (mesh0.vnN == mesh1.vnN).all()

    assert (mesh0.normals == mesh1.normals).all()
    assert (mesh0.tangents == mesh1.tangents).all()

    if hasattr(mesh0, 'h'):
        for i in range(len(mesh0.h)):
            assert (mesh0.h[i] == mesh1.h[i]).all(), (
                'mesh h[{}] different'.format(i)
            )

    # check edges, faces, volumes
    assert (mesh0.edge == mesh1.edge).all()
    assert (mesh0.area == mesh1.area).all()
    assert (mesh0.vol == mesh1.vol).all()

    # Tree mesh specific
    if hasattr(mesh0, '_cells'):
        assert (mesh0._cells == mesh1._cells)

    # curvi-specific
    if hasattr(mesh0, 'nodes'):
        for i in range(len(mesh0.nodes)):
            assert (mesh0.nodes[i] == mesh1.nodes[i]).all()


class TensorTest(unittest.TestCase):

    n = [4, 5, 9]
    x0 = [-0.5, -0.25, 0]

    def setUp(self):
        self.mesh = discretize.TensorMesh(self.n, x0=self.x0)

    def test_save_load(self):
        print('\nTesting save / load of Tensor Mesh ...')
        mesh0 = self.mesh
        f = mesh0.save()
        mesh1 = discretize.load_mesh(f)
        compare_meshes(mesh0, mesh1)
        os.remove(f)
        print('ok\n')

    def test_copy(self):
        print('\nTesting copy of Tensor Mesh ...')
        mesh0 = self.mesh
        mesh1 = mesh0.copy()
        compare_meshes(mesh0, mesh1)
        print('ok\n')

    def test_base_updates(self):
        with self.assertRaises(Exception):
            self.mesh._n = None

        # check that if h has been set, we can't mess up n
        with self.assertRaises(Exception):
            self.mesh._n = [6, 5, 9]

        # can't change dimensionality of a mesh
        with self.assertRaises(Exception):
            self.mesh._n = [4, 5]


class CylTest(unittest.TestCase):

    n = [4, 1, 9]

    def setUp(self):
        self.mesh = discretize.CylMesh(self.n, x0='00C')

    def test_save_load(self):
        print('\nTesting save / load of Cyl Mesh ...')
        mesh0 = self.mesh
        f = mesh0.save()
        mesh1 = discretize.load_mesh(f)
        compare_meshes(mesh0, mesh1)
        os.remove(f)
        print('ok\n')

    def test_copy(self):
        print('\nTesting copy of Cyl Mesh ...')
        mesh0 = self.mesh
        mesh1 = mesh0.copy()
        compare_meshes(mesh0, mesh1)
        print('ok\n')


class TreeTest(unittest.TestCase):

    def setUp(self):
        M = discretize.TreeMesh([8, 8])

        def refine(cell):
            xyz = cell.center
            dist = ((xyz - [0.25, 0.25])**2).sum()**0.5
            if dist < 0.25:
                return 3
            return 2

        M.refine(refine)
        M.number()

        self.mesh = M

    def test_save_load(self):
        print('\nTesting save / load of Tree Mesh ...')
        mesh0 = self.mesh
        f = mesh0.save()
        mesh1 = discretize.load_mesh(f)
        compare_meshes(mesh0, mesh1)
        os.remove(f)
        print('ok\n')

    def test_copy(self):
        print('\nTesting copy of Tree Mesh ...')
        mesh0 = self.mesh
        mesh1 = mesh0.copy()
        compare_meshes(mesh0, mesh1)
        print('ok\n')

    def test_base_updates(self):
        with self.assertRaises(Exception):
            self.mesh._n = None

        # check that if h has been set, we can't mess up n
        with self.assertRaises(Exception):
            self.mesh._n = [6, 5, 9]


class CurviTest(unittest.TestCase):

    def setUp(self):
        a = np.array([1, 1, 1])
        b = np.array([1, 2])
        c = np.array([1, 4])

        def gridIt(h): return [np.cumsum(np.r_[0, x]) for x in h]

        X, Y, Z = discretize.utils.ndgrid(gridIt([a, b, c]), vector=False)
        self.mesh = discretize.CurvilinearMesh([X, Y, Z])

    def test_save_load(self):
        print('\nTesting save / load of Curvi Mesh ...')
        mesh0 = self.mesh
        f = mesh0.save()
        mesh1 = discretize.load_mesh(f)
        compare_meshes(mesh0, mesh1)
        os.remove(f)
        print('ok\n')

    def test_copy(self):
        print('\nTesting copy of Curvi Mesh ...')
        mesh0 = self.mesh
        mesh1 = mesh0.copy()
        compare_meshes(mesh0, mesh1)
        print('ok\n')

    def test_base_updates(self):
        with self.assertRaises(Exception):
            self.mesh._n = None

        # check that if h has been set, we can't mess up n
        with self.assertRaises(Exception):
            self.mesh._n = [6, 5, 9]


if __name__ == '__main__':
    unittest.main()
