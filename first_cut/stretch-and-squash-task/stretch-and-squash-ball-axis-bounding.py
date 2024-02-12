import maya.cmds as cmds

def create_ball_and_rig():
    """Create a sphere and a group to act as the rig for the ball."""
    ball = cmds.polySphere(r=1, name='ball')[0]
    rig = cmds.group(empty=True, name='ball_rig')
    cmds.parent(ball, rig)
    ball_center = cmds.xform(ball, query=True, worldSpace=True, rotatePivot=True)
    cmds.xform(rig, worldSpace=True, pivots=ball_center)
    return ball, rig, ball_center

def apply_squash_deformer(rig):
    """Apply the 'squash' deformer to the rig."""
    squash = cmds.nonLinear(rig, type='squash')
    cmds.parent(squash[1], rig)
    return squash

def set_initial_position(rig):
    """Set initial position of the rig."""
    cmds.setAttr(rig + '.translateY', 20)
    cmds.setAttr(rig + '.translateX', -10)

def move_squash_pivot(squash, ball_center):
    """Move the pivot point of the squash deformer to the bottom of the ball."""
    cmds.xform(squash[0], worldSpace=True, pivots=[ball_center[0], ball_center[1]-1, ball_center[2]])

def set_falling_and_bouncing_keyframes(rig, squash, bounce_times, bounce_heights, squash_factors):
    """Set keyframes for the rig's Y position to simulate falling and bouncing."""
    fall_time = 45 * 0.8 * 0.25
    cmds.setKeyframe(rig, attribute='translateY', time=0, value=20)
    cmds.setKeyframe(rig, attribute='translateY', time=fall_time, value=0)
    cmds.setKeyframe(squash[0], attribute='factor', time=0, value=0)
    cmds.setKeyframe(squash[0], attribute='factor', time=fall_time, value=0)

    for i in range(len(bounce_times) - 1):
        peak_time = (bounce_times[i] + bounce_times[i+1]) / 2
        cmds.setKeyframe(rig, attribute='translateY', time=bounce_times[i], value=0)
        cmds.setKeyframe(rig, attribute='translateY', time=peak_time, value=bounce_heights[i+1])
        cmds.setKeyframe(squash[0], attribute='factor', time=bounce_times[i], value=squash_factors[i])
        cmds.setKeyframe(squash[0], attribute='factor', time=peak_time, value=0)
        cmds.keyTangent(squash[0], attribute='factor', time=(bounce_times[i - 1],), inTangentType='linear', outTangentType='linear')

    cmds.setKeyframe(rig, attribute='translateY', time=bounce_times[-1], value=0)
    cmds.setKeyframe(squash[0], attribute='factor', time=bounce_times[-1], value=squash_factors[-1])
    cmds.setKeyframe(squash[0], attribute='factor', time=bounce_times[-1] + 45*0.8*0.25, value=0)

def set_forward_movement_keyframes(rig):
    """Set keyframes for the rig's X position to simulate forward movement."""
    cmds.setKeyframe(rig, attribute='translateX', time=0, value=-10)
    cmds.setKeyframe(rig, attribute='translateX', time=240, value=10)

def set_rotation_keyframes(rig, bounce_times, rotation_amount):
    """Set keyframes for the rig's rotation to simulate rotation during the falling and in-air phases."""
    for i in range(len(bounce_times) - 1):
        peak_time = (bounce_times[i] + bounce_times[i+1]) / 2
        cmds.setKeyframe(rig, attribute='rotateZ', time=bounce_times[i], value=i*rotation_amount)
        cmds.setKeyframe(rig, attribute='rotateZ', time=peak_time, value=(i+0.5)*rotation_amount)
    cmds.setKeyframe(rig, attribute='rotateZ', time=bounce_times[-1], value=(len(bounce_times)-1)*rotation_amount)

def set_continued_movement_and_rotation_keyframes(rig, bounce_times, rotation_amount):
    """Set keyframes for the rig to continue moving and rotating after the last bounce."""
    end_time = bounce_times[-1] + 45*0.8*0.25
    cmds.setKeyframe(rig, attribute='translateX', time=end_time, value=15)
    cmds.setKeyframe(rig, attribute='rotateZ', time=end_time, value=(len(bounce_times)-1)*rotation_amount - 45)

def main():
    bounce_times = [45 * 0.8 * 0.25 * i for i in range(1, 6)]
    bounce_heights = [10, 8, 6, 4, 2]
    squash_factors = [-0.3, 0.3, -0.3, 0.3, -0.3]
    rotation_amount = -90

    ball, rig, ball_center = create_ball_and_rig()
    squash = apply_squash_deformer(rig)
    set_initial_position(rig)
    move_squash_pivot(squash, ball_center)
    set_falling_and_bouncing_keyframes(rig, squash, bounce_times, bounce_heights, squash_factors)
    set_forward_movement_keyframes(rig)
    set_rotation_keyframes(rig, bounce_times, rotation_amount)
    set_continued_movement_and_rotation_keyframes(rig, bounce_times, rotation_amount)

if __name__ == "__main__":
    main()