import maya.cmds as cmds
import math

# Create a cylinder for the pendulum arm
arm = cmds.polyCylinder(r=0.1, h=2)[0]

# Create a sphere for the pendulum bob
bob = cmds.polySphere(r=0.3)[0]

# Move the bob to the end of the arm
cmds.move(0, -1, 0, bob)

# Group the arm and bob together
pendulum = cmds.group(arm, bob)

# Set the pivot point to the top of the arm
cmds.xform(pendulum, piv=(0, 1, 0))

# Create the animation
for i in range(1, 101):
    # Calculate the rotation angle
    angle = 45 * math.sin(i * math.pi / 50)
    
    # Set the rotation of the pendulum
    cmds.setAttr(pendulum + '.rotateZ', angle)
    
    # Set a keyframe at the current frame
    cmds.setKeyframe(pendulum, attribute='rotateZ', t=i)

# Play the animation
cmds.play(forward=True)