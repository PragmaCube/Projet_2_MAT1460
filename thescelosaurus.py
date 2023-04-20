import math
import parameters

class Thescelosaurus:
    def __init__(self, initial_conditions, acceleration):
        self.initial_angle = initial_conditions[0]
        self.initial_position = initial_conditions[1]
        self.angular_speed = initial_conditions[2]

        self.acceleration = acceleration

        self.angle = self.initial_angle
        self.position = self.initial_position

        self.speed = 0

        self.acceleration_phase = True

        self.rotation_base_pos = [0, 0]
        self.rotation_base_angle = 0

        self.rotation_radius = 0.5

        self.base_target_position = [0, 0]

        self.rotation_maneuvre = False
        self.rotation_maneuvre_angle = 0
        self.rotation_started = False
        self.turn = False
        self.rotation_finished = True

        self.base_pos_x = []
        self.base_pos_y = []

        self.angle_target = 0

        self.sin_way = 1
        self.cos_way = 1

    def getAngle(self):
        return self.angle

    def getSpeed(self):
        return self.speed

    def getAcceleration(self):
        return self.acceleration

    def getPosition(self):
        return self.position

    def turn(self, targeted_angle):
        if self.angle == targeted_angle:
            return True

        if self.angle + self.angular_speed > targeted_angle and self.angle < targeted_angle:
            self.angle = targeted_angle
            return True

        if self.angle > targeted_angle:
            self.angle -= self.angular_speed
            
        else:
            self.angle += self.angular_speed

        return False

    def errorEstimator(self, targeted_position, zone):
        return math.sqrt((targeted_position[0] - self.position[0]) ** 2 + (targeted_position[1] - self.position[1]) ** 2) < zone

    def isRotationFinished(self):
        return self.rotation_finished

    # way : droite --> 1, gauche --> -1
    def rotationMove(self, targeted_angle, way):
        self.angular_speed = self.speed / self.rotation_radius

        #if abs(targeted_angle - self.rotation_maneuvre_angle)

        #self.rotation_maneuvre_angle += way * math.Pi / 


        #self.position[0] = 
    # Targeted direction

    def getComplementaryAngle(self, angle):
        if angle > 0:
            return 2 * math.pi - angle

        return angle + 2 * math.pi

    def getSinSign(self, angle):
        if angle % (2 * math.pi) > 0 and angle % (2 * math.pi) < math.pi:
            return 1

        elif angle % math.pi == 0:
            return 0

        return - 1

    def getCosSign(self, angle):
        if angle % (2 * math.pi) > math.pi / 2 and angle % (2 * math.pi) < 3 * math.pi / 2:
            return 1

        elif (angle + math.pi / 2) % math.pi== 0:
            return 0

        return - 1

    def move(self, targeted_position):
        if self.base_target_position[0] == 0 and self.base_target_position[1] == 0 and self.speed == 0:
            self.base_target_position[0] = targeted_position[0]
            self.base_target_position[1] = targeted_position[1]

        elif self.base_target_position[0] != targeted_position[0] or self.base_target_position[1] != targeted_position[1]:
            self.rotation_maneuvre = True

        if self.errorEstimator(targeted_position, 0.1):
            self.position[0] = targeted_position[0]
            self.position[1] = targeted_position[1]

            return True
        
        targeted_angle = math.asin((targeted_position[1] - self.position[1]) / (math.sqrt((targeted_position[0] - self.position[0])** 2 + (targeted_position[1] - self.position[1]) ** 2)))
        print(f"{targeted_angle} | {self.getPosition()}")
        distance = math.sqrt(targeted_position[0] ** 2 + targeted_position[1] ** 2)

        if self.angle != targeted_angle and self.speed == 0:
            self.turn(targeted_angle)
            #return False

        #else:


        if self.speed < 13.8:
            self.speed += self.acceleration * parameters.running_speed

            if self.speed > 13.8:
                self.speed = 13.8

        if targeted_position[0] > self.position[0]:
            if targeted_position[1] > self.position[1]:
                self.position[0] += self.speed * parameters.running_speed * math.cos(self.angle)
                self.position[1] += self.speed * parameters.running_speed * math.sin(self.angle)

            else:
                self.position[0] += self.speed * parameters.running_speed * math.cos(self.angle)
                self.position[1] -= self.speed * parameters.running_speed * math.sin(self.angle)

        else:
            if targeted_position[1] > self.position[1]:
                self.position[0] -= self.speed * parameters.running_speed * math.cos(self.angle)
                self.position[1] += self.speed * parameters.running_speed * math.sin(self.angle)

            else:
                self.position[0] -= self.speed * parameters.running_speed * math.cos(self.angle)
                self.position[1] -= self.speed * parameters.running_speed * math.sin(self.angle)

        return False

    def uhh(self, targeted_angle, distance_from_velociraptor = 7, angle_of_velociraptor = 0, way = 0):
        if self.angle != targeted_angle:
            if abs(targeted_angle - self.angle) < 0.1:
                self.angle = targeted_angle

            elif self.angle > targeted_angle:
                self.angle -= self.angular_speed

            else:
                self.angle += targeted_angle

        if distance_from_velociraptor > 6:
            if self.speed < 13.8:
                self.speed += self.acceleration * parameters.running_speed

                if self.speed > 13.8:
                    self.speed = 13.8

            self.position[0] += self.speed * parameters.running_speed * math.cos((self.angle) + math.pi / 2)
            self.position[1] += self.speed * parameters.running_speed * math.sin((self.angle) + math.pi / 2)


    def move_complete(self, targeted_angle, distance_from_velociraptor = 7, angle_of_velociraptor = 0, way = 1):
        self.angular_speed = self.speed / self.rotation_radius

        trigger = False

        # On veut aller à un angle très loin de celui actuellement
        if not self.rotation_started and abs(targeted_angle - self.angle) >= math.pi and abs(targeted_angle):
            #self.angle_target = self.getComplementaryAngle(targeted_angle)
            self.angle_target = targeted_angle

            trigger = True

        elif not self.rotation_started:
            trigger = False
            self.angle_target = targeted_angle

        #print([targeted_angle - self.angle, self.getComplementaryAngle(self.angle) - self.angle])

        if self.angle != self.angle_target:
            if abs(self.angle_target - self.angle) < 0.3:
                self.angle = targeted_angle
                self.turn = False
                self.rotation_finished = True

            elif self.angle > self.angle_target:
                self.turn = True
                self.angle = self.angle - self.angular_speed * parameters.running_speed
                self.rotation_finished = False

            else:
                self.turn = True
                self.angle = self.angle + self.angular_speed * parameters.running_speed
                self.rotation_finished = False

        if trigger:
            self.cos_way = self.getCosSign(self.angle_target)
            self.sin_way = self.getSinSign(self.angle_target)

        if distance_from_velociraptor > 6:
            if self.speed < 13.8:
                self.speed += self.acceleration * parameters.running_speed

                if self.speed > 13.8:
                    self.speed = 13.8

            if not self.turn:
                self.rotation_started = False
                self.position[0] += self.speed * parameters.running_speed * math.cos(way * (self.angle) + math.pi / 2)
                self.position[1] += self.speed * parameters.running_speed * math.sin(way * (self.angle) + math.pi / 2)

            else:
                if not self.rotation_started:
                    if self.angle > self.angle_target:
                        self.rotation_base_pos[0] = self.position[0] - math.cos(way * math.pi + self.angle) * self.rotation_radius
                        self.rotation_base_pos[1] = self.position[1] - math.sin(way * math.pi + self.angle) * self.rotation_radius

                    else:
                        self.rotation_base_pos[0] = self.position[0] + math.cos(way * math.pi + self.angle) * self.rotation_radius
                        self.rotation_base_pos[1] = self.position[1] + math.sin(way * math.pi + self.angle) * self.rotation_radius

                    self.rotation_base_angle = self.angle
                    self.base_pos_x.append(self.rotation_base_pos[0])
                    self.base_pos_y.append(self.rotation_base_pos[1])

                    self.rotation_started = True

                else:
                    if self.angle > self.angle_target:
                        self.position[0] = self.rotation_base_pos[0] - self.rotation_radius * math.cos(self.angle)
                        self.position[1] = self.rotation_base_pos[1] - self.rotation_radius * math.sin(self.angle)

                    else:
                        self.position[0] = self.rotation_base_pos[0] + self.rotation_radius * math.cos(self.angle)
                        self.position[1] = self.rotation_base_pos[1] + self.rotation_radius * math.sin(self.angle)