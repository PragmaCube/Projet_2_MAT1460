import parameters
import math

class Velociraptor:
    def __init__(self, initial_conditions, acceleration):
        self.initial_angle = initial_conditions[0]
        self.initial_position = initial_conditions[1]
        self.angular_speed = initial_conditions[2]

        self.acceleration = acceleration

        self.angle = self.initial_angle
        self.position = self.initial_position

        self.speed = 0

        self.acceleration_phase = True

        self.time_since_max_speed = 0
        self.rest = False
        self.time_stamp = 0
        self.acceleration_time = 0
        self.deceleration_finished = False
        self.deceleration_phase = False
        self.rotation_radius = 1.5
        self.rotation_started = False
        self.rotation_finished = False
        self.angle_target = 0

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

    def move(self, targeted_position, elapsed_time):

        if self.errorEstimator(targeted_position, 0.69):
            self.position[0] = targeted_position[0]
            self.position[1] = targeted_position[1]

            return True
        
        targeted_angle = math.asin((targeted_position[1] - self.position[1]) / (math.sqrt((targeted_position[0] - self.position[0])** 2 + (targeted_position[1] - self.position[1]) ** 2)))
        #print(targeted_angle)
        distance = math.sqrt(targeted_position[0] ** 2 + targeted_position[1] ** 2)

        if self.angle != targeted_angle:
            self.turn(targeted_angle)
            #return False

        if self.speed < 16.8 and not self.deceleration_phase and not self.rest:
            self.speed += self.acceleration * parameters.running_speed

            if self.speed >= 16.8:
                self.speed = 16.8
                self.acceleration_time = elapsed_time

        if self.speed == 16.8:
            self.time_since_max_speed += parameters.running_speed

        if self.time_since_max_speed >= 15 + self.acceleration_time:
            if not self.deceleration_phase:
                self.time_since_max_speed = 0
                self.deceleration_phase = True

        elif self.deceleration_phase:
            self.speed -= 2 * self.acceleration * parameters.running_speed

            if self.speed <= 0:
                self.speed = 0
                self.deceleration_phase = False
                self.deceleration_finished = True
                self.time_stamp = elapsed_time
                self.rest = True
                
        elif elapsed_time - self.time_stamp >= 15 + self.acceleration_time:
            self.deceleration_finished = False
            self.rest = True

        if not self.rest:
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

    def move_complete(self, targeted_angle, elapsed_time):
        self.angular_speed = self.speed / 1.5
        
        if not self.rotation_started and abs(targeted_angle - self.angle) >= math.pi and abs(targeted_angle):
            #self.angle_target = self.getComplementaryAngle(targeted_angle)
            self.angle_target = targeted_angle

        elif not self.rotation_started:
            self.angle_target = targeted_angle

        if self.angle != self.angle_target:
            if abs(self.angle_target - self.angle) < 0.1:
                self.angle = targeted_angle
                self.turn = False
                self.rotation_finished = True

            elif self.angle > self.angle_target:
                self.turn = True
                self.angle -= self.angular_speed * parameters.running_speed
                self.rotation_finished = False

            else:
                self.turn = True
                self.angle += self.angular_speed * parameters.running_speed
                self.rotation_finished = False

        if self.speed < 16.7:
            self.speed += self.acceleration * parameters.running_speed

            if self.speed > 16.7:
                self.speed = 16.7
                self.acceleration_time = elapsed_time

        if self.speed == 16.7:
            self.time_since_max_speed += parameters.running_speed

        if self.time_since_max_speed >= 15 + self.acceleration_time:
            if not self.deceleration_phase:
                self.time_since_max_speed = 0
                self.deceleration_phase = True

        elif self.deceleration_phase:
            self.speed -= 2 * self.acceleration * parameters.running_speed

            if self.speed <= 0:
                self.speed = 0
                self.deceleration_phase = False
                self.deceleration_finished = True
                self.time_stamp = elapsed_time
                self.rest = True
                
        elif elapsed_time - self.time_stamp >= 15 + self.acceleration_time:
            self.deceleration_finished = False
            self.rest = True

        if not self.rest:
            self.position[0] += self.speed * parameters.running_speed * math.cos(self.angle)
            self.position[1] += self.speed * parameters.running_speed * math.sin(self.angle)