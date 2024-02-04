import maya.cmds as cmds

# Create a sphere for the basketball
basketball = cmds.polySphere(r=1)[0]  # Basketball

# Position the sphere above the ground
cmds.move(0, 10, 0, basketball)  # Increased height to 10

# Create a sphere for the football
football = cmds.polySphere(r=0.7)[0]  # Football

# Position the sphere above the ground
cmds.move(5, 10, 0, football)  # Increased height to 10 and separation to 5

# Create a sphere for the ping pong ball
pingpong = cmds.polySphere(r=0.3)[0]  # Ping pong ball

# Position the sphere above the ground
cmds.move(10, 10, 0, pingpong)  # Increased height to 10 and separation to 10

# Define a function to animate a series of bounces
def animate_bounce(ball, start_frame, initial_height, bounce_duration, cor):
    height = initial_height
    frame = start_frame
    while height > 0.1:  # Stop when the bounce height is very small
        # Set keyframe at peak
        cmds.setKeyframe(ball, attribute='translateY', v=height, t=frame)
        
        # Set keyframe at ground contact
        cmds.setKeyframe(ball, attribute='translateY', v=0, t=frame + bounce_duration / 2)
        
        # Set keyframe at peak again
        cmds.setKeyframe(ball, attribute='translateY', v=height, t=frame + bounce_duration)
        
        # Prepare for the next bounce
        height *= cor  # Each bounce reaches a percentage of the previous height
        frame += bounce_duration  # Move to the next time frame

# Animate the basketball bouncing
animate_bounce(basketball, start_frame=1, initial_height=10, bounce_duration=50, cor=0.75)

# Animate the football bouncing
animate_bounce(football, start_frame=1, initial_height=10, bounce_duration=50, cor=0.6)

# Animate the ping pong ball bouncing
animate_bounce(pingpong, start_frame=1, initial_height=10, bounce_duration=50, cor=0.9)