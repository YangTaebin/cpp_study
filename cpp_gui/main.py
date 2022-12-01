import sys, math, copy
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QPainter, QPen, QIcon
from PyQt5.QtCore import Qt, QRect

G = 6.67384
dt = 0.1
width, height = 1500, 1000
real_height = height + 40
collis = True
circle_grow_speed = 0.5
circle_maketick = 50
label_width, label_height = 50, 20
check_dist = True
check_vel = True
doppler = False

class GravitiSimulation(QWidget):
    properties = []
    accels = []
    velos = []
    posis = []
    n = 0
    forces = {}
    circles = []
    cnt = 0

    def __init__(self, posis, velos, properties, n):
        super().__init__()
        self.initUI()
        self.circles = []
        self.cnt = 0
        self.labels = {}
        if len(properties) == len(posis) == len(velos) == n:

            self.properties = properties
            self.posis = posis
            self.velos = velos
            self.n = n
            if check_dist:
                for i in range(self.n):
                    for j in range(i + 1, self.n):
                        r_x, r_y = self.posis[i][0] - self.posis[j][0], self.posis[i][1] - self.posis[j][1]
                        r = ((r_x ** 2) + (r_y ** 2)) ** (1 / 2)
                        label = QLabel(str(r), self)
                        label.setGeometry(QRect(int((self.posis[i][0] + self.posis[j][0]) / 2 - (label_width / 2)),
                                                int((self.posis[i][1] + self.posis[j][1]) / 2 - (label_height / 2)),
                                                label_width, label_height))
                        label.setAlignment(Qt.AlignCenter)
                        label.setText(str(r))
                        label.setStyleSheet("font-weight: bold;color:#FF0000;")
                        self.labels[str(i) + ":" + str(j)] = label
            self.init_cal()
        else:
            print("input data length not matched")
            return None

    def initUI(self):
        self.setGeometry((1920-width)//2,(1080-height)//2,width, height)
        self.setWindowTitle("Gravity N-Body simulation")
        self.setWindowIcon(QIcon("icon.png"))

    def init_cal(self):
        self.accels = []
        for i in range(self.n):
            self.accels.append((0.0, 0.0))
            for j in range(i+1, self.n):
                self.forces[str(i) + ":" + str(j)] = 0

    def sim(self):
        if check_dist:
            for i in range(self.n):
                for j in range(i + 1, self.n):
                    label = self.labels[str(i) + ":" + str(j)]
                    label.move(int((self.posis[i][0] + self.posis[j][0]) / 2 - (label_width / 2)),
                               int((self.posis[i][1] + self.posis[j][1]) / 2 - (label_height / 2)))

        self.cnt += 1
        if self.cnt % circle_maketick == 0:
            if check_dist:
                for i in range(self.n):
                    for j in range(i + 1, self.n):
                        r_x, r_y = self.posis[i][0] - self.posis[j][0], self.posis[i][1] - self.posis[j][1]
                        r = ((r_x ** 2) + (r_y ** 2)) ** (1 / 2)
                        label = self.labels[str(i) + ":" + str(j)]
                        label.setText(str(round(r,2)))
            self.cnt = 0
            self.create_circle()

        self.init_cal()

        self.cal_nowtick()

        self.circle_cal()

        self.update()

    def create_circle(self):
        for i in range(self.n):
            if doppler:
                r = self.properties[i][1]
                if r < 1: r = 1
                self.circles.append((self.posis[i][0], self.posis[i][1], r, self.properties[i][3]))

    def circle_cal(self):
        i = 0
        while i <len(self.circles):
            if self.circles[i][2] > self.circles[i][3]:
                self.circles.pop(i)
            else:
                self.circles[i] = (self.circles[i][0], self.circles[i][1], self.circles[i][2] + circle_grow_speed, self.circles[i][3])
                i += 1

    def roshu(self, a, b):
        dens_a = self.properties[a][0] / ((4/3)*math.pi*((self.properties[a][1]/2)**3))
        dens_b = self.properties[b][0] / ((4/3)*math.pi*((self.properties[b][1]/2)**3))
        d_a = 1.26*((dens_a/dens_b)**(1/3))*(self.properties[a][1]/2)
        d_b = 1.26*((dens_b/dens_a)**(1/3))*(self.properties[b][1]/2)
        return d_a, d_b

    def collision(self,a,b):
        m_a, m_b = self.properties[a][0], self.properties[b][0]
        vel_a, vel_b = self.velos[a], self.velos[b]
        vel_tot = ((m_a*vel_a[0]+m_b*vel_b[0])/(m_a+m_b), (m_a*vel_a[1]+m_b*vel_b[1])/(m_a+m_b))
        m_tot = m_a + m_b
        r_tot = self.properties[a][1] + self.properties[b][1]
        pos_tot = ((self.posis[a][0]+self.posis[b][0])/2, (self.posis[a][1]+self.posis[b][1])/2)
        self.velos[a] = vel_tot
        self.properties[a] = (m_tot, int(r_tot), self.properties[a][2], self.properties[a][3])
        self.posis[a] = pos_tot
        self.properties.pop(b)
        self.velos.pop(b)
        self.posis.pop(b)
        self.accels.pop(b)
        if check_dist:
            for i in range(self.n):
                for j in range(i+1, self.n):
                    if i==b or j==b:
                        self.labels[str(i) + ":" + str(j)].clear()
        self.n -= 1

    def cal_nowtick(self):
        collision = []
        for i in range(self.n):
            for j in range(i+1, self.n):
                r_x, r_y = self.posis[i][0]-self.posis[j][0], self.posis[i][1]-self.posis[j][1]
                r = ((r_x**2) + (r_y**2))**(1/2)
                d_i, d_j = self.roshu(i,j)
                if max(d_i,d_j) >= r and collis:
                    collision.append((i,j))
                force = G*self.properties[i][0]*self.properties[j][0]/(r**2)
                force_x, force_y = force*r_x/r, force*r_y/r
                self.accels[i] = (self.accels[i][0]-force_x/self.properties[i][0], self.accels[i][1]-force_y/self.properties[i][0])
                self.accels[j] = (self.accels[j][0] + force_x/self.properties[j][0], self.accels[j][1]+force_y/self.properties[j][0])

        for i in range(self.n):
            self.velos[i] = (self.velos[i][0] + self.accels[i][0] * dt, self.velos[i][1] + self.accels[i][1] * dt)
            self.posis[i] = (self.posis[i][0] + self.velos[i][0] * dt, self.posis[i][1] + self.velos[i][1] * dt)

        for a in collision:
            self.collision(a[0],a[1])


    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        qp.setPen(QPen(Qt.black, 1))
        for circle in self.circles:
            qp.drawEllipse(QRect(int(circle[0] - circle[2] / 2), int(circle[1] - circle[2] / 2), int(circle[2]), int(circle[2])))

        if check_dist:
            qp.setPen(QPen(Qt.black, 1))
            for i in range(self.n):
                for j in range(i+1, self.n):
                    qp.drawLine(self.posis[i][0],self.posis[i][1],self.posis[j][0],self.posis[j][1])

        qp.setPen(QPen(Qt.black, 2))
        for i in range(self.n):
            r = self.properties[i][1]
            if r < 1: r = 1
            if check_vel:
                qp.drawLine(self.posis[i][0]+self.velos[i][0]*5, self.posis[i][1]+self.velos[i][1]*5, self.posis[i][0], self.posis[i][1])
            qp.setBrush(self.properties[i][2])
            qp.drawEllipse(QRect(int(self.posis[i][0]-(r/2)), int(self.posis[i][1]-(r/2)), int(r), int(r)))
        qp.end()
        self.sim()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = GravitiSimulation([(width/2-550,height/2),(width/2, height/2), (width/2-520,height/2), (width/2-200, height/2)], [(0,2.3), (0,-(10*2.3+0.5*3.7+5*4)/500), (0, 3.7), (0, 4)], [(10, 20, Qt.blue, 300), (500, 109, Qt.red, 700), (0.5, 5, Qt.gray, 200), (5, 10, Qt.yellow, 200)], 4)
    ex.show()
    sys.exit(app.exec_())