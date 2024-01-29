import maya.cmds as cmds

# Create a sphere
ball = cmds.polySphere(r=1, name='ball')[0]

# Set initial position
cmds.setAttr(ball + '.translateY', 20)  # Start from a higher position

# Set keyframes for the ball's Y position to simulate falling and bouncing
# The ball will fall to the ground over the course of 1 second (24 frames at 24 fps)
# Then it will bounce 4 times over the next 9 seconds (216 frames)
fall_time = 45
bounce_times = [fall_time, fall_time + 54, fall_time + 108, fall_time + 162, fall_time + 216]
bounce_heights = [10, 8, 6, 4, 2]

# Set keyframe for the start of the fall
cmds.setKeyframe(ball, attribute='translateY', time=0, value=20)
# Set keyframe for the end of the fall
cmds.setKeyframe(ball, attribute='translateY', time=fall_time, value=0)

for i in range(len(bounce_times) - 1):
    # Set keyframe for when the ball hits the ground
    cmds.setKeyframe(ball, attribute='translateY', time=bounce_times[i], value=0)
    # Set keyframe for the peak of the bounce
    peak_time = (bounce_times[i] + bounce_times[i+1]) / 2
    cmds.setKeyframe(ball, attribute='translateY', time=peak_time, value=bounce_heights[i+1])

# Set the final keyframe for when the ball hits the ground
cmds.setKeyframe(ball, attribute='translateY', time=bounce_times[-1], value=0)

# Set keyframes for the ball's X position to simulate forward motion
# The ball will move steadily in the X direction over the course of the animation
cmds.setKeyframe(ball, attribute='translateX', time=0, value=0)
cmds.setKeyframe(ball, attribute='translateX', time=240, value=10)

# Set keyframes for the ball's scale to simulate squash and stretch
# The ball will squash when it hits the ground and stretch in the air
for time in bounce_times:
    cmds.setKeyframe(ball, attribute='scaleY', time=time, value=0.8)  # Squash
    cmds.setKeyframe(ball, attribute='scaleY', time=time+30, value=1.5)  # Stretch
    cmds.setKeyframe(ball, attribute='scaleX', time=time, value=1.2)  # Squash
    cmds.setKeyframe(ball, attribute='scaleX', time=time+30, value=0.8)  # Stretch
    
# Set the final keyframes for the ball's scale to return to initial size
cmds.setKeyframe(ball, attribute='scaleY', time=bounce_times[-1]+30, value=1)  # Return to initial Y scale
cmds.setKeyframe(ball, attribute='scaleX', time=bounce_times[-1]+30, value=1)  # Return to initial X scale
