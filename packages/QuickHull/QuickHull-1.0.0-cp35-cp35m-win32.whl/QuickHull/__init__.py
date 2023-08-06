'''
    QuickHull
'''

from typing import Tuple, List

try:
    from QuickHull import hull

except ImportError:
    pass


__all__ = ['quick_hull']


if False:
    def hull_quick_hull(*args) -> Tuple[List[Tuple[float, float, float]], List[Tuple[int, int, int]]]:
        '''
            hull_quick_hull
        '''

    hull.quick_hull = hull_quick_hull


def quick_hull(points, ccw=True):
    '''
        Create a convex hull of 3D points.

        Args:
            points (tuple): Points as 3-tuples: (x, y, z)
            ccw (bool): The triangles orientation, counter clockwise by default.

        Returns:
            tuple: vertices and triangles

        Example:

            Example input and output::

                points = [
                    (0.0, 0.0, 0.0),
                    (0.0, 1.0, 0.0),
                    (0.1, 0.1, 0.1),
                    (0.2, 0.1, 0.4),
                    (0.1, 0.4, 0.2),
                    (0.3, 0.1, 0.2),
                    (0.0, 0.0, 1.0),
                    (1.0, 0.0, 0.0),
                ]

                vertices, triangles = QuickHull.quick_hull(points)

                # The output will be:

                vertices = [
                    (0.0, 1.0, 0.0),
                    (0.0, 0.0, 1.0),
                    (1.0, 0.0, 0.0),
                    (0.0, 0.0, 0.0),
                ]

                triangles = [
                    (0, 2, 1),
                    (1, 2, 3),
                    (2, 0, 3),
                    (0, 1, 3),
                ]

            Merging output::

                points = [
                    (0.0, 0.0, 0.0),    # A
                    (0.0, 0.0, 1.0),    # B
                    (0.0, 1.0, 0.0),    # C
                    (1.0, 0.0, 0.0),    # D
                ]

                vertices, triangles = QuickHull.quick_hull(points)
                triangle_vertices = [(vertices[a], vertices[b], vertices[c]) for a, b, c in triangles]

                # The output will be:

                triangle_vertices = [
                    ( (0.0, 1.0, 0.0), (1.0, 0.0, 0.0), (0.0, 0.0, 1.0) ),    # C, D, B
                    ( (0.0, 0.0, 1.0), (1.0, 0.0, 0.0), (0.0, 0.0, 0.0) ),    # B, D, A
                    ( (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 0.0) ),    # D, C, A
                    ( (0.0, 1.0, 0.0), (0.0, 0.0, 1.0), (0.0, 0.0, 0.0) ),    # C, B, A
                ]
    '''

    return hull.quick_hull(tuple(points), ccw)
