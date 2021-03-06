# -*- coding: utf-8 -*-
# vispy: gallery 30
# -----------------------------------------------------------------------------
# Copyright (c) 2015, Vispy Development Team. All Rights Reserved.
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
"""
Simple use of SceneCanvas to display a cube with an arcball camera.
"""
import sys

from vispy import scene

canvas = scene.SceneCanvas(keys='interactive', size=(800, 600), show=True)

# Set up a viewbox to display the cube with interactive arcball
view = canvas.central_widget.add_view()
cube = scene.visuals.Cube(edge_color='k', parent=view.scene)
view.camera = 'arcball'
view.camera.fov = 30.

if __name__ == '__main__' and sys.flags.interactive == 0:
    canvas.app.run()
