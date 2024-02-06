import maya.cmds as cmds

# Create a sphere for the basketball
basketball = cmds.polySphere(r=1)[0]  # Basketball

# Position the sphere above the ground
cmds.move(0, 10, 0, basketball)  # Increased height to 10

# Adjust pivot to the bottom of the sphere
cmds.xform(basketball, piv=(0, -1, 0))

# Create a sphere for the football
football = cmds.polySphere(r=0.7)[0]  # Football

# Position the sphere above the ground
cmds.move(5, 10, 0, football)  # Increased height to 10 and separation to 5

# Adjust pivot to the bottom of the sphere
cmds.xform(football, piv=(0, -0.7, 0))

# Create a sphere for the ping pong ball
pingpong = cmds.polySphere(r=0.3)[0]  # Ping pong ball

# Position the sphere above the ground
cmds.move(10, 10, 0, pingpong)  # Increased height to 10 and separation to 10

# Adjust pivot to the bottom of the sphere
cmds.xform(pingpong, piv=(0, -0.3, 0))

# Define a function to animate a series of bounces
def animate_bounce(ball, start_frame, initial_height, bounce_duration, cor, ground_position):
    height = initial_height
    frame = start_frame
    while height > ground_position:  # Stop when the bounce height is very small
        # Set keyframe at peak
        cmds.setKeyframe(ball, attribute='translateY', v=height, t=frame)
        cmds.setKeyframe(ball, attribute='scaleX', v=1, t=frame)
        cmds.setKeyframe(ball, attribute='scaleY', v=1, t=frame)
        
        # Set keyframe at ground contact
        cmds.setKeyframe(ball, attribute='translateY', v=ground_position, t=frame + bounce_duration / 2)
        cmds.setKeyframe(ball, attribute='scaleX', v=1.3, t=frame + bounce_duration / 2)  # Squash
        cmds.setKeyframe(ball, attribute='scaleY', v=0.7, t=frame + bounce_duration / 2)  # Squash
        
        # Set keyframe at peak again
        cmds.setKeyframe(ball, attribute='translateY', v=height, t=frame + bounce_duration)
        cmds.setKeyframe(ball, attribute='scaleX', v=1, t=frame + bounce_duration)  # Stretch
        cmds.setKeyframe(ball, attribute='scaleY', v=1, t=frame + bounce_duration)  # Stretch
        
        # Prepare for the next bounce
        height *= cor  # Each bounce reaches a percentage of the previous height
        frame += bounce_duration  # Move to the next time frame

# Animate the basketball bouncing
animate_bounce(basketball, start_frame=1, initial_height=14, bounce_duration=50, cor=0.75, ground_position=0.9)

# Animate the football bouncing
animate_bounce(football, start_frame=1, initial_height=10, bounce_duration=50, cor=0.6, ground_position=0.71)

# Animate the ping pong ball bouncing
animate_bounce(pingpong, start_frame=1, initial_height=10, bounce_duration=50, cor=0.8, ground_position=0.285)