"""DBForward controller."""




from controller import Robot

##Initialize the total time steops
TIME_STEP = 64


##Initialize the robot object
robot = Robot()


#--------------------methods------------------------------

#Initialize the rotational motors
def init_wheels(wheel_names):
    wheels = []    
    for i in range(len(wheel_names)):
        wheels.append(robot.getDevice(wheelsNames[i]))
        wheels[i].setPosition(float('inf'))
        wheels[i].setVelocity(0.0)
    return wheels

#Initialize the sensors    
def init_sensors(sensor_names):
    sensors = []
    for i in range(len(sensor_names)):
        sensors.append(robot.getDevice(sensor_names[i]))
        sensors[i].enable(TIME_STEP)
    return sensors

#Initialize the linear motors that control legs    
def init_legs(leg_names):
    legs = []
    for i in range(len(leg_names)):
        legs.append(robot.getDevice(legNames[i]))
    return legs


#Set the speed of the rotational motors
def setSpeed(speed,wheels):
    for i in range(len(wheels)):
        wheels[i].setVelocity(speed)

        
# Simulation Class control the mode of going up-stairs and 
# down-stairs.   
class runSim(object):

    def __init__(self, mode):

        self.mode = mode
        
    def getMode(self):
        return self.mode
        
    def setMode(self,newMode):
        self.mode = newMode
        
    # Algorithms for going up-stairs
    def upStair(self):
    
        onstage = False
        # Pre-measued the position of the legs when going up-stairw
        position = 0.1
           
        if ds[0].getValue() < 600 or ds[1].getValue() < 600:
           
           leg[0].setPosition(position)
           leg[1].setPosition(position)
           
        if ps[0].getValue() > 0.05 or ps[1].getValue() > 0.05:
           if ds[2].getValue() < 600 or ds[3].getValue() < 600:
              leg[2].setPosition(position)
              leg[3].setPosition(position)
              
        if ps[2].getValue() > 0.05 or ps[3].getValue() > 0.05:
           if ds[4].getValue() < 600 or ds[5].getValue() < 600:
              leg[4].setPosition(position)
              leg[5].setPosition(position)
              
        if ps[4].getValue() > 0.05 or ps[5].getValue()>0.05: 
           if ds[6].getValue() < 600:
              leg[6].setPosition(position)
           elif ds[7].getValue() <600:
              leg[7].setPosition(position)
        
        # Check whether all legs landed on a stair and re-set them
        # Uopdate the current mode of the robot.
        if ps[6].getValue() > 0.05 and ps[7].getValue()>0.05:
           if dsf[6].getValue() < 600 and dsf[7].getValue() < 600:
              onstage = True
              if self.mode == "Up":
                 self.mode = "Down"
    
        if onstage:
           for l in leg:
               l.setPosition(0)
               
    def downStair(self):
          offstage = False
          # Pre-measued the position of the legs when going down-stairs
          lposition = -0.1
          for a in dsf:
             a.enable(TIME_STEP)

          if dsf[0].getValue() > 900:
             leg[0].setPosition(lposition)
          elif dsf[1].getValue() > 900:
             leg[1].setPosition(lposition)
             
          if ps[0].getValue() < -0.05 or ps[1].getValue() < -0.05:

             if dsf[2].getValue() > 900:
                leg[2].setPosition(lposition)
                leg[6].setPosition(lposition-0.05)

             elif dsf[3].getValue() > 900:
                leg[3].setPosition(lposition)
                leg[7].setPosition(lposition-0.05)

          if ps[2].getValue() < -0.05 or ps[3].getValue() < -0.05:

             if dsf[4].getValue() > 600:
                leg[4].setPosition(lposition)
                leg[6].setPosition(0)
             elif dsf[5].getValue() > 600:
                leg[5].setPosition(lposition)
                leg[7].setPosition(0)
          if ps[4].getValue() < -0.05 or ps[5].getValue() < -0.05:

             if dsf[6].getValue() > 600:
                leg[6].setPosition(lposition)
             elif dsf[7].getValue() > 600:
                leg[7].setPosition(lposition) 
                 
          if ps[6].getValue() < -0.05 and ps[7].getValue() < -0.05:
             if dsf[6].getValue() < 300 and dsf[7].getValue() < 300:
                offstage = True
          if offstage:
             for l in leg:
                 l.setPosition(0)
        
##--------------------main functions----------------------

# Get the names of the front-facing distance sensors
dsNames = ['ds_left1','ds_right1'
          ,'ds_left2','ds_right2'
          ,'ds_left3','ds_right3'
          ,'ds_left4','ds_right4']
# Get the names of the floor-facing distance sensors          
dsfNames = ['ds_left1f','ds_right1f'
          ,'ds_left2f','ds_right2f'
          ,'ds_left3f','ds_right3f'
          ,'ds_left4f','ds_right4f']
# Get the names of rotational motors
wheelsNames = ['wheel1L', 'wheel2L', 'wheel3L', 'wheel4L',
               'wheel1R', 'wheel2R', 'wheel3R', 'wheel4R']
# Get the name of the linear motors             
legNames = ['L1','R1',
            'L2','R2',
            'L3','R3',
            'L4','R4']
# Get the names of the position sensors        
psNames = ['l1_ps','r1_ps'
          ,'l2_ps','r2_ps'
          ,'l3_ps','r3_ps'
          ,'l4_ps','r4_ps']
          

#Initialize all the components 
wheels = init_wheels(wheelsNames)
ds = init_sensors(dsNames)
dsf = init_sensors(dsfNames)
leg = init_legs(legNames)
ps = init_sensors(psNames)

#Set the initial speed and the positions for rotational motors and the linear motors
position = 0
speed = 3
mode = 'None'

#Initualize simulation controller object
rs = runSim(mode)
while robot.step(TIME_STEP) != -1:
    
    setSpeed(speed,wheels)

    
    if ds[0].getValue() < 1000 or ds[1].getValue() < 1000:
       mode = "Up"
       #Update the mode after going up-stairs
       rs.setMode(mode)
    if rs.getMode() =="Up":
       rs.upStair()
       mode = rs.getMode()
    else:
       rs.downStair()

