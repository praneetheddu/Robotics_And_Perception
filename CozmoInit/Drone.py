import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps, Angle

def drone(robot: cozmo.robot.Robot):
    robot.set_lift_height(0.0, accel=10.0, max_speed=10.0, duration=0.0, in_parallel=False, num_retries=0).wait_for_completed()
    lookaround = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
    cubes = robot.world.wait_until_observe_num_objects(num=1, object_type=cozmo.objects.LightCube, timeout=60)
    lookaround.stop()

    print("cube identified")
    current_action = robot.pickup_object(cubes[0], num_retries=1)
    current_action.wait_for_completed()
    robot.say_text("yeeeeee", play_excited_animation=True, use_cozmo_voice=True, 
        duration_scalar=1.0, voice_pitch=0.0, in_parallel=True, num_retries=0).wait_for_completed()
    if current_action.has_failed:
        code, reason = current_action.failure_reason
        result = current_action.result
        print("Pickup Cube failed: code=%s reason='%s' result=%s" % (code, reason, result))
        return
    action = robot.drive_straight(distance_mm(100), speed_mmps(50))
    action.wait_for_completed()
    robot.set_lift_height(0.0, accel=10.0, max_speed=10.0, duration=0.0, in_parallel=False, num_retries=0).wait_for_completed()
    action = robot.drive_straight(distance_mm(-100), speed_mmps(50))
    action.wait_for_completed()

def order(robot: cozmo.robot.Robot): # Call this function once the robot sees the order object
    #Drive in a circle. Need to test out to change the configurations to 10cm radius
    lSpeed = 20.0
    rSpeed = 50.0
    l_acc  = 10.0
    r_acc = 10.0
    robot.drive_wheels(lSpeed, rSpeed, l_wheel_acc=None, r_wheel_acc=None, duration=19.3).wait_for_completed() #take out wait for completed if necessary

def inspection(robot: cozmo.robot.Robot): #Call this once the robot sees the inspection obeject
    for turns in range (0,4):
        robot.set_lift_height(0.0, accel=10.0, max_speed=10.0, duration=0.0, in_parallel=False, num_retries=0).wait_for_completed()
        action = robot.drive_straight(distance_mm(100), speed_mmps(250))
        robot.set_lift_height(1.0, accel=10.0, max_speed=10.0, duration=2.0, in_parallel=True, num_retries=0).wait_for_completed()
        action.wait_for_completed()
        action = robot.drive_straight(distance_mm(100), speed_mmps(250))
        robot.set_lift_height(0.0, accel=10.0, max_speed=10.0, duration=2.0, in_parallel=True, num_retries=0).wait_for_completed()
        action.wait_for_completed()
        robot.turn_in_place(degrees(90), in_parallel=False, num_retries=0, speed=degrees(90), 
            accel=None, angle_tolerance=None, is_absolute=False).wait_for_completed()

cozmo.run_program(inspection)