import maya.cmds as cmds

# Create a sphere for the basketball
basketball = cmds.polySphere(r=1)[0]  # Basketball

# Position the sphere above the ground
cmds.move(0, 10, 0, basketball)  # Increased height to 10

# Adjust pivot to the bottom of the sphere
cmds.xform(basketball, piv=(0, -1, 0))

# Create a squash deformer for the basketball
basketball_squash = cmds.nonLinear(basketball, type='squash', lowBound=-1, highBound=1)

# Create a bend deformer for the basketball
basketball_bend = cmds.nonLinear(basketball, type='bend', lowBound=-1, highBound=1)

# Repeat the process for the football and ping pong ball
football = cmds.polySphere(r=0.7)[0]  # Football
cmds.move(5, 10, 0, football)  # Increased height to 10 and separation to 5
cmds.xform(football, piv=(0, -0.7, 0))
football_squash = cmds.nonLinear(football, type='squash', lowBound=-1, highBound=1)
football_bend = cmds.nonLinear(football, type='bend', lowBound=-1, highBound=1)

pingpong = cmds.polySphere(r=0.3)[0]  # Ping pong ball
cmds.move(10, 10, 0, pingpong)  # Increased height to 10 and separation to 10
cmds.xform(pingpong, piv=(0, -0.3, 0))
pingpong_squash = cmds.nonLinear(pingpong, type='squash', lowBound=-1, highBound=1)
pingpong_bend = cmds.nonLinear(pingpong, type='bend', lowBound=-1, highBound=1)

# Define a function to animate a series of bounces
def animate_bounce(ball, squash, bend, start_frame, initial_height, bounce_duration, cor, ground_position):
    height = initial_height
    frame = start_frame
    while height > ground_position:  # Stop when the bounce height is very small
        # Set keyframe at peak
        cmds.setKeyframe(ball, attribute='translateY', v=height, t=frame)
        cmds.setKeyframe(squash, attribute='factor', v=0, t=frame)  # No squash at peak
        cmds.setKeyframe(bend, attribute='curvature', v=0, t=frame)  # No bend at peak
        
        # Set keyframe at ground contact
        cmds.setKeyframe(ball, attribute='translateY', v=ground_position, t=frame + bounce_duration / 2)
        cmds.setKeyframe(squash, attribute='factor', v=0.3, t=frame + bounce_duration / 2)  # Exaggerated squash at ground contact
        cmds.setKeyframe(bend, attribute='curvature', v=0.1, t=frame + bounce_duration / 2)  # Bend at ground contact
        
        # Set keyframe at peak again
        cmds.setKeyframe(ball, attribute='translateY', v=height, t=frame + bounce_duration)
        cmds.setKeyframe(squash, attribute='factor', v=0, t=frame + bounce_duration)  # No squash at peak
        cmds.setKeyframe(bend, attribute='curvature', v=0, t=frame + bounce_duration)  # No bend at peak
        
        # Prepare for the next bounce
        height *= cor  # Each bounce reaches a percentage of the previous height
        frame += bounce_duration  # Move to the next time frame

# Animate the basketball bouncing
animate_bounce(basketball, basketball_squash, basketball_bend, start_frame=1, initial_height=10, bounce_duration=50, cor=0.75, ground_position=0.9)

# Animate the football bouncing
animate_bounce(football, football_squash, football_bend, start_frame=1, initial_height=10, bounce_duration=50, cor=0.6, ground_position=0.71)

# Animate the ping pong ball bouncing
animate_bounce(pingpong, pingpong_squash, pingpong_bend, start_frame=1, initial_height=10, bounce_duration=50, cor=0.9, ground_position=0.285)