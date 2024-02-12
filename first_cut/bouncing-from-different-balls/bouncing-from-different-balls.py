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
    # Add a non-linear squash deformer to the ball
    squash_deformer, squash_handle = cmds.nonLinear(ball, type='squash', lowBound=-1, highBound=1)
    
    # Parent the deformer handle to the ball so it follows the ball's movement
    cmds.parent(squash_handle, ball)
    
    height = initial_height
    frame = start_frame
    while height > ground_position:  # Stop when the bounce height is very small
        # Set keyframe at peak
        cmds.setKeyframe(ball, attribute='translateY', v=height, t=frame)
        cmds.setKeyframe(squash_deformer, attribute='factor', v=0, t=frame)  # No squash or stretch

        # Set keyframe at ground contact
        cmds.setKeyframe(ball, attribute='translateY', v=ground_position, t=frame + bounce_duration / 2)
        cmds.setKeyframe(squash_deformer, attribute='factor', v=-0.3, t=frame + bounce_duration / 2)  # Squash
        
        # Break the tangents of the animation curve 
        cmds.keyTangent(ball, attribute='translateY', time=(frame + bounce_duration / 2, frame + bounce_duration / 2), inTangentType='linear', outTangentType='linear')
        cmds.keyTangent(squash_deformer, attribute='factor', time=(frame + bounce_duration / 2, frame + bounce_duration / 2), inTangentType='linear', outTangentType='linear')

        # Set keyframe at peak again
        cmds.setKeyframe(ball, attribute='translateY', v=height, t=frame + bounce_duration)
        cmds.setKeyframe(squash_deformer, attribute='factor', v=0, t=frame + bounce_duration)  # Stretch

        # Prepare for the next bounce
        height *= cor  # Each bounce reaches a percentage of the previous height
        frame += bounce_duration  # Move to the next time frame
        bounce_duration *= cor  # Each bounce takes a percentage of the previous durations

# Animate the basketball bouncing
animate_bounce(basketball, start_frame=1, initial_height=14, bounce_duration=12, cor=0.75, ground_position=0.9)

# Animate the football bouncing
animate_bounce(football, start_frame=1, initial_height=10, bounce_duration=12, cor=0.6, ground_position=0.71)

# Animate the ping pong ball bouncing
animate_bounce(pingpong, start_frame=1, initial_height=10, bounce_duration=12, cor=0.8, ground_position=0.285)