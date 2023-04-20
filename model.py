import velociraptor
import thescelosaurus
import math
import parameters
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib

class Model:
    def __init__(self, velo, thesce, running_time, use_both, video = [False, ""]):
        self.velo = velo[0]
        self.other_velo = velo[1]
        self.use_both = use_both

        self.iterations = 0

        self.thesce = thesce
        
        self.running_time = running_time

        self.video = video[0]

        if self.video:
            matplotlib.rcParams['animation.ffmpeg_path'] = video[1]

        self.velo_pos_x = []
        self.velo_pos_y = []
        self.other_velo_pos_x = []
        self.other_velo_pos_y = []

        self.thesce_pos_x = []
        self.thesce_pos_y = []

        self.distances = []
        self.other_distances = []
        self.max_time = 0

        self.angles = []

    def distance(self):
        return math.sqrt((self.thesce.getPosition()[0] - self.velo.getPosition()[0]) ** 2 + (self.thesce.getPosition()[1] - self.velo.getPosition()[1]) ** 2)

    def other_distance(self):
        return math.sqrt((self.thesce.getPosition()[0] - self.other_velo.getPosition()[0]) ** 2 + (self.thesce.getPosition()[1] - self.other_velo.getPosition()[1]) ** 2)

    def distance_velo(self):
        return math.sqrt((self.velo.getPosition()[0] - self.other_velo.getPosition()[0]) ** 2 + (self.velo.getPosition()[1] - self.other_velo.getPosition()[1]) ** 2) 

    def detection(self, minimum_distance):
        return self.distance() < minimum_distance

    def storeData(self):
        self.velo_pos_x.append(self.velo.getPosition()[0])
        self.velo_pos_y.append(self.velo.getPosition()[1])
        self.other_velo_pos_x.append(self.other_velo.getPosition()[0])
        self.other_velo_pos_y.append(self.other_velo.getPosition()[1])
        self.thesce_pos_x.append(self.thesce.getPosition()[0])
        self.thesce_pos_y.append(self.thesce.getPosition()[1])

    def plot(self):
        fig = plt.figure(figsize=(6, 6))
        plt.xlim([-20, 20])
        #plt.ylim([220, 260])
        line_blue, = plt.plot([], [], scaley=True, scalex=True, color="orange", linewidth=2)
        line_orange, = plt.plot([], [], scaley=True, scalex=True, color="blue", linewidth=2.4)

        if self.use_both:
            line_red, = plt.plot([], [], scaley=True, scalex=True, color="red", linewidth=2.4)

        legend = plt.legend([''], loc='lower left', handlelength = 0)
        legend.set_visible(False)

        def onclick(event):
            plt.close()

        cid = fig.canvas.mpl_connect('close_event', onclick)

        def animate(i):
            line_orange.set_data(self.velo_pos_x[0:8 * i], self.velo_pos_y[0:8 * i])

            if self.use_both:
                line_red.set_data(self.other_velo_pos_x[0:8 * i], self.other_velo_pos_y[0:8 * i])
            
            line_blue.set_data(self.thesce_pos_x[0:8 * i], self.thesce_pos_y[0:8 * i])

            legend.set_visible(True)
            legend.get_texts()[0].set_text(f"Distance 1 : {round(self.distances[8 * i], 3)}\nDistance 2 : {self.use_both * round(self.other_distances[8 * i], 3)}\nTemps        : {round(8 * i * parameters.running_speed, 3)}")
            fig.gca().autoscale_view()
            fig.gca().relim()
            plt.draw()

        if self.video:
            ani = FuncAnimation(fig, animate, frames = int(self.iterations / 8), interval = 2, repeat = False)

        plt.show()

        if self.video:
            ani.save("ligne_droite.mp4")

    def simulation(self):
        switch = False

        count = 0
        angle = self.thesce.getAngle()
        turn = False

        angles_ = [math.pi / 4,- math.pi / 2, - 2 * math.pi / 3]

        last_last_angle = 0
        self.angles = [math.pi / 2 for i in range(10)]
        other_angles = [- math.pi / 2 for i in range(10)]

        coef_1 = 1
        coef_2 = 1
                
        for i in range(self.running_time):
            self.iterations += 1
            self.distances.append(self.distance())
            self.other_distances.append(self.other_distance())
            
            if self.detection(70):
                switch = True

            if (self.distance() < 2 or (self.other_distance() < 2) and self.use_both) and not turn:
                angle += math.pi / 3
                turn = True
                count = 0

            if turn and count == 50:
                angle -= math.pi / 3

            if switch:
                self.thesce.move_complete(angle, 7, 0)

            # Cette partie permet de démontrer la faisabilité des rotations
            #if i == 50:
                #angle += 5 * math.pi / 6
                #self.thesce.move_complete(angle, 7, 0, 1)

            #if i == 110:
                #angle = - math.pi
                #self.thesce.move_complete(angle, 7, 0, 1)

            #if i == 170:
                #angle = - 3 * math.pi / 4
                #self.thesce.move_complete(angle, 7, 0, -1)

            #if i == 250:
                #angle = math.pi / 3
                #self.thesce.move_complete(angle, 7, 0, -1)

            if self.distance_velo() <= 2 and self.use_both:
                coef_1 = 0.96
                coef_2 = 1.04
            
            else:
                coef_1 = 1
                coef_2 = 1
            
            if self.thesce.getPosition()[1] > self.velo.getPosition()[1]: #or (self.thesce.getPosition()[1] > self.velo.getPosition()[1] and self.thesce.getPosition()[0] > self.velo.getPosition()[0]):
                self.angles.append(math.acos((self.thesce.getPosition()[0] - self.velo.getPosition()[0]) / (math.sqrt((self.thesce.getPosition()[0] - self.velo.getPosition()[0]) ** 2 + (self.thesce.getPosition()[1] - self.velo.getPosition()[1]) ** 2))) % (2 * math.pi))

                if self.velo.move_complete(self.angles[i] * coef_1, i * parameters.running_speed):
                    print([i * parameters.running_speed, self.velo.getSpeed(), self.thesce.getSpeed()])

            else:
                self.angles.append(- math.acos((self.thesce.getPosition()[0] - self.velo.getPosition()[0]) / (math.sqrt((self.thesce.getPosition()[0] - self.velo.getPosition()[0]) ** 2 + (self.thesce.getPosition()[1] - self.velo.getPosition()[1]) ** 2))) % (2 * math.pi))

                if self.velo.move_complete(self.angles[i] * coef_1, i * parameters.running_speed):
                    print([i * parameters.running_speed, self.velo.getSpeed(), self.thesce.getSpeed()])

            if self.use_both:
                if self.thesce.getPosition()[1] > self.other_velo.getPosition()[1]: #or (self.thesce.getPosition()[1] > self.velo.getPosition()[1] and self.thesce.getPosition()[0] > self.velo.getPosition()[0]):
                    other_angles.append(math.acos((self.thesce.getPosition()[0] - self.other_velo.getPosition()[0]) / (math.sqrt((self.thesce.getPosition()[0] - self.other_velo.getPosition()[0]) ** 2 + (self.thesce.getPosition()[1] - self.other_velo.getPosition()[1]) ** 2))) % (2 * math.pi))

                    if self.other_velo.move_complete(other_angles[i] * coef_2, i * parameters.running_speed):
                        print([i * parameters.running_speed, self.velo.getSpeed(), self.thesce.getSpeed()])

                else:
                    other_angles.append(- math.acos((self.thesce.getPosition()[0] - self.other_velo.getPosition()[0]) / (math.sqrt((self.thesce.getPosition()[0] - self.other_velo.getPosition()[0]) ** 2 + (self.thesce.getPosition()[1] - self.other_velo.getPosition()[1]) ** 2))) % (2 * math.pi))

                    if self.other_velo.move_complete(other_angles[i] * coef_2, i * parameters.running_speed):
                        print([i * parameters.running_speed, self.velo.getSpeed(), self.thesce.getSpeed()])

            if self.distance() < 0.69 or (self.other_distance() < 0.69 and self.use_both):
                self.plot()
                self.max_time = i
                return [i * parameters.running_speed]
                
            self.storeData()

        self.plot()

        return i * parameters.running_speed

