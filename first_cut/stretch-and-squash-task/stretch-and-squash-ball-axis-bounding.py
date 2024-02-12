import maya.cmds as cmds

# Create a sphere
ball = cmds.polySphere(r=1, name='ball')[0]

# Create a group to act as the rig for the ball
rig = cmds.group(empty=True, name='ball_rig')

# Add the ball to the rig
cmds.parent(ball, rig)

# Get the center of the ball
ball_center = cmds.xform(ball, query=True, worldSpace=True, rotatePivot=True)

# Set the pivot point of the rig to the center of the ball
cmds.xform(rig, worldSpace=True, pivots=ball_center)

# Apply the 'squash' deformer to the rig
squash = cmds.nonLinear(rig, type='squash')

# Parent the deformer handle to the rig so it follows the rig's movement
cmds.parent(squash[1], rig)

# Set initial position
cmds.setAttr(rig + '.translateY', 20)  # Start from a higher position
cmds.setAttr(rig + '.translateX', -10)  # Start from a more negative X position

# Move the pivot point of the squash deformer to the bottom of the ball
cmds.xform(squash[0], worldSpace=True, pivots=[ball_center[0], ball_center[1]-1, ball_center[2]])

# Set keyframes for the rig's Y position to simulate falling and bouncing
fall_time = 45 * 0.8 * 0.25
bounce_times = [fall_time, fall_time + 54*0.8*0.25, fall_time + 108*0.8*0.25, fall_time + 162*0.8*0.25, fall_time + 216*0.8*0.25]
bounce_heights = [10, 8, 6, 4, 2]

# Set keyframe for the start of the fall
cmds.setKeyframe(rig, attribute='translateY', time=0, value=20)
# Set keyframe for the end of the fall
cmds.setKeyframe(rig, attribute='translateY', time=fall_time, value=0)

# Set keyframe for the start and end of the animation for the 'squash' deformer's factor attribute
cmds.setKeyframe(squash[0], attribute='factor', time=0, value=0)  # No squash at the start
cmds.setKeyframe(squash[0], attribute='factor', time=fall_time, value=0)  # No squash at the end

# Define squash factors for each bounce
squash_factors = [-0.3, 0.3, -0.3, 0.3, -0.3]

for i in range(len(bounce_times) - 1):
    # Set keyframe for when the rig hits the ground
    cmds.setKeyframe(rig, attribute='translateY', time=bounce_times[i], value=0)
    # Set keyframe for the peak of the bounce
    peak_time = (bounce_times[i] + bounce_times[i+1]) / 2
    cmds.setKeyframe(rig, attribute='translateY', time=peak_time, value=bounce_heights[i+1])

    # Set keyframes for the 'squash' deformer's factor attribute to create the 'squash' effect
    cmds.setKeyframe(squash[0], attribute='factor', time=bounce_times[i], value=squash_factors[i])  # Full squash
    cmds.setKeyframe(squash[0], attribute='factor', time=peak_time, value=0)  # No squash

    # Break the tangents of the deformer's factor attribute at the keyframes where the ball hits the ground
    cmds.keyTangent(squash[0], attribute='factor', time=(bounce_times[i],), inTangentType='linear', outTangentType='linear')

# Set the final keyframe for when the rig hits the ground
cmds.setKeyframe(rig, attribute='translateY', time=bounce_times[-1], value=0)
cmds.setKeyframe(squash[0], attribute='factor', time=bounce_times[-1], value=squash_factors[-1])  # Full squash

# Set keyframe for the 'squash' deformer's factor attribute to return to original shape at the end of the animation
cmds.setKeyframe(squash[0], attribute='factor', time=bounce_times[-1] + 45*0.8*0.25, value=0)  # No squash at the end

# Set keyframes for the rig's X position to simulate forward movement
cmds.setKeyframe(rig, attribute='translateX', time=0, value=-10)
cmds.setKeyframe(rig, attribute='translateX', time=240, value=10)

# Set keyframes for the rig's rotation to simulate rotation during the falling and in-air phases
rotation_amount = -90  # Amount of rotation in degrees
for i in range(len(bounce_times) - 1):
    # Set keyframe for rotation at the start of the fall
    cmds.setKeyframe(rig, attribute='rotateZ', time=bounce_times[i], value=i*rotation_amount)
    # Set keyframe for rotation at the peak of the bounce
    peak_time = (bounce_times[i] + bounce_times[i+1]) / 2
    cmds.setKeyframe(rig, attribute='rotateZ', time=peak_time, value=(i+0.5)*rotation_amount)

# Set the final keyframes for the rig's rotation
cmds.setKeyframe(rig, attribute='rotateZ', time=bounce_times[-1], value=(len(bounce_times)-1)*rotation_amount)

# Set keyframes for the rig to continue moving after the last bounce
end_time = bounce_times[-1] + 45*0.8*0.25 # Adjusted end_time to account for the last bounce
cmds.setKeyframe(rig, attribute='translateX', time=end_time, value=15)  # Continue moving in the X direction

# Set keyframes for the rig to continue rotating after the last bounce
cmds.setKeyframe(rig, attribute='rotateZ', time=end_time, value=(len(bounce_times)-1)*rotation_amount - 45)  # Continue rotating in the -Z direction