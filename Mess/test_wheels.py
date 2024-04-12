from picar import front_wheels, back_wheels
import picar

picar.setup()
bw = back_wheels.Back_Wheels()
fw = front_wheels.Front_Wheels()
bw.speed = 0
OT_t1_1 = 3
OT_t1_2 = 4

if OT_t1_1 > OT_t1_2:
    # move robot straight ahead
    fw.turn(90+30)
    bw.speed = 30
    for i in range(200):
        bw.backward()
    bw.stop()
else:
    # move robot to the right 
    fw.turn(90-30) # turn the front wheels to the right
    bw.speed = 30
    for i in range(500):
        bw.backward()
    bw.stop()
    fw.turn(90)