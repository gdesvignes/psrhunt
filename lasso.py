#!/usr/bin/env python

# Install
# On gentoo, emerge matplotlib


# Changes :
# 
# 12/04/09 : Automatic flag RFI
# 10/04/09 : Various modif for mkimposou
# 09/04/09 : Fullscreen window by default
# 18/03/09 : Add automatic backup every 2 min


# Lasso Libs
from matplotlib.lines import Line2D
#from matplotlib.nxutils import points_inside_poly
from matplotlib.collections import RegularPolyCollection

from matplotlib.pyplot import figure



# Definition of LASSO Class
# Adapted from Matplotlib examples lasso_widget
class Widget:
    """
    OK, I couldn't resist; abstract base class for mpl GUI neutral
    widgets
    """
    drawon = True
    eventson = True

class Lasso(Widget):
    def __init__(self, ax, xy, callback=None, useblit=True):
        self.axes = ax
        self.figure = ax.figure
        self.canvas = self.figure.canvas
        self.useblit = useblit
        if useblit:
            self.background = self.canvas.copy_from_bbox(self.axes.bbox)

        x, y = xy
        self.verts = [(x,y)]
        self.line = Line2D([x], [y], linestyle='-', color='black', lw=2)
        self.axes.add_line(self.line)
        self.callback = callback
        self.cids = []
        self.cids.append(self.canvas.mpl_connect('button_release_event', self.onrelease))
        self.cids.append(self.canvas.mpl_connect('motion_notify_event', self.onmove))

    def onrelease(self, event):
        if self.verts is not None:
            self.verts.append((event.xdata, event.ydata))
            if len(self.verts)>2:
                self.callback(self.verts)
        self.verts = None
        for cid in self.cids:
            self.canvas.mpl_disconnect(cid)

    def onmove(self, event):
        if self.verts is None: return
        if event.inaxes != self.axes: return
        if event.button!=3: return
        self.verts.append((event.xdata, event.ydata))

        self.line.set_data(zip(*self.verts))

        if self.useblit:
            self.canvas.restore_region(self.background)
            self.axes.draw_artist(self.line)
            self.canvas.blit(self.axes.bbox)
        else:
            self.canvas.draw_idle()
