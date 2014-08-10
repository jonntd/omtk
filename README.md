# Open MayaToolKit

Omtk is a suite of production pipeline tools for maya.
The goal of the project is to develop pythonic solution to traditional problems/tasks in maya.
Omtk is lightweight and unintrusive to other pipelines.

### omtk.rigging.autorig
An node-base autorig that store itself in a network of maya nodes.
```
# ex: creating a basic biped rig
from pymel import core as pymel
from omtk.rigging import autorig

rig = autorig.Create()
rig.AddPart(autorig.Arm(pymel.ls('jnt_arm_l_*')))
rig.AddPart(autorig.Arm(pymel.ls('jnt_arm_r_*')))
rig.AddPart(autorig.FK(pymel.ls('jnt_spine')))
rig.AddPart(autorig.FK(pymel.ls('jnt_chest')))
rig.AddPart(autorig.FK(pymel.ls('jnt_neck')))
rig.AddPart(autorig.FK(pymel.ls('jnt_head')))
rig.Build()
```
### omtk.libs.libSerialization
A set of tools that serialize/deserialize python objects in various formats (maya nodes, json, yaml, xml, etc)

### omtk.rigging.formulaParser
A lightweight programming language that parse math formulas to utility nodes.
This is done by defining lots of new operators.
Currently, supported operators are: add (+), substract (-), multiply (*), divide (/), pow (^), distance (~), equal (=), not_equal (!=), bigger (>), bigger_or_equal (>=), smaller (<) and smaller_or_equal (<=).
```
# ex: creating a bell-curve type squash
import math
from omtk.rigging import formulaParser
loc, locs = pymel.polysphere()
stretch = loc.sy
squash = formulaParser.parse("1 / (e^(x^2))", e=math.e, x=stretch)
pymel.connectAttr(squash, loc.sx)
pymel.connectAttr(squash, loc.sz)
```
