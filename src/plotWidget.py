import pyqtgraph as pg


class PlotWidget(pg.GraphicsLayoutWidget ):
    def __init__(self, af):
        super(PlotWidget,self).__init__()
        #app = pg.mkQApp("Plotting Example")
        #mw = QtGui.QMainWindow()
        #mw.resize(800,800)

        # win = pg.GraphicsLayoutWidget(show=True, title="Basic plotting examples")
        # win.resize(1000,600)
        # win.setWindowTitle('pyqtgraph example: Plotting')

        # Enable antialiasing for prettier plots
        #self.setConfigOptions(antialias=True)
        self.af = af
        self.label = pg.LabelItem(justify='right')
        self.addItem(self.label)

        self.p1 = self.addPlot(title="Multiple curves",row=1, col=0)
        self.p1.plot(af.c["cl"],x=af.c["alpha"], pen=(0,255,0), name="cl curve")
        self.p1.plot(af.c["cd"],x=af.c["alpha"], pen=(255,0,0), name="cd curve")
        self.p1.plot(af.c["cm"],x=af.c["alpha"], pen=(255,255,0), name="cm curve")
        self.vLine = pg.InfiniteLine(angle=90, movable=False)
        self.p1.addItem(self.vLine, ignoreBounds=True)
        self.vb = self.p1.vb
        self.proxy = pg.SignalProxy(self.p1.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved)

    def mouseMoved(self, evt):
        pos = evt[0]  ## using signal proxy turns original arguments into a tuple
        if self.p1.sceneBoundingRect().contains(pos):
            mousePoint = self.vb.mapSceneToView(pos)
            index = int(mousePoint.x())
            #if index > 0 and index < len(data1):
                #label.setText("<span style='font-size: 12pt'>x=%0.1f,   <span style='color: red'>y1=%0.1f</span>,   <span style='color: green'>y2=%0.1f</span>" % (mousePoint.x(), data1[index], data2[index]))
            try:
                self.label.setText("<span style='font-size: 12pt'>alpha=%0.1f,  \
                                    <span style='color: green'>cl=%0.5f</span>, \
                                    <span style='color: red'>cd=%0.5f</span>,  \
                                    <span style='color: yellow'>cm=%0.5f</span>" % (mousePoint.x(), self.af.c["cl"][self.af.getIndexByAngle( mousePoint.x() )], self.af.c["cd"][self.af.getIndexByAngle(mousePoint.x())], self.af.c["cm"][self.af.getIndexByAngle(mousePoint.x() )] )  )
                self.vLine.setPos(mousePoint.x())
            except TypeError:
                return
            #hLine.setPos(mousePoint.y())

    

