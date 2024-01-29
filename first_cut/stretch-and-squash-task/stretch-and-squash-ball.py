import maya.cmds as cmds

# Set the initial position of the ball
start_pos = 10
end_pos = 0
ball = cmds.polySphere(r=1, sx=20, sy=20, ax=(0, 1, 0), cuv=2, ch=1)[0]

# Set the total frames for the animation
total_frames = 24 * 5  # 24 fps * 5 seconds
extra_frames = 24 * 2  # 24 fps * 2 seconds for the exaggeration phase

# Set the keyframes for the ball's position
for i in range(0, total_frames + extra_frames, 10):  # Set a keyframe every 4 frames
    time = i
    # Calculate the current position of the ball
    if time < total_frames:
        pos = start_pos - ((start_pos - end_pos) * (time / float(total_frames))**2)
    else:
        pos = end_pos
    # Set the ball's position at this frame
    cmds.setKeyframe(ball, attribute='translateY', v=pos, t=time)

    # Calculate the squash and stretch
    if pos > end_pos + 1:
        # The ball is in the air, so stretch it along the Y axis
        stretch = 1 + (time / float(total_frames))  # Gradually increase the stretch from 1 to 2
        cmds.setKeyframe(ball, attribute='scaleY', v=stretch, t=time)
        cmds.setKeyframe(ball, attribute='scaleX', v=1/stretch, t=time)
        cmds.setKeyframe(ball, attribute='scaleZ', v=1/stretch, t=time)
    else:
        # The ball is on the ground, so squash it along the X axis
        if time < total_frames:
            squash = 1 + ((total_frames - time) / float(total_frames))  # Gradually decrease the squash from 2 to 1
        else:
            # Exaggerate the squash for 2 seconds, then return to initial state
            exaggeration_factor = 2  # Change this to stretch more or less
            squash = 1 + exaggeration_factor * ((total_frames + extra_frames - time) / float(extra_frames))
        cmds.setKeyframe(ball, attribute='scaleY', v=1/squash, t=time)
        cmds.setKeyframe(ball, attribute='scaleX', v=squash, t=time)
        cmds.setKeyframe(ball, attribute='scaleZ', v=squash, t=time)