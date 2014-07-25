from abaqus import *
from abaqusConstants import *
from caeModules import *
from driverUtils import executeOnCaeStartup

executeOnCaeStartup()
openMdb(pathName='C:\\Users\\tbrosse\\.openmdao\\gui\\projects\\Stent\\ark_stent.cae')

#----------------------------------------------------------------------------
#                                   script names.
#----------------------------------------------------------------------------
model_name='Model-1'
part_name='Ark_stent'
solid_extrude_name='Solid extrude-1'
step_name='Step-1'
job_name='Job-1'
odb_name=job_name+'.odb'
output_file='output.txt'

#----------------------------------------------------------------------------
#                                     mesh size.
#----------------------------------------------------------------------------

seed_size=0.05


#----------------------------------------------------------------------------
#                           assign design variables.
#----------------------------------------------------------------------------
lenght= 3.6
radius_2= 0.3
radius_4= 4.0
alpha= 0.4
beta= 0.9
#----------------------------------------------------------------------------
#                        modify design variables's values.
#----------------------------------------------------------------------------
p = mdb.models['Model-1'].parts['Ark_stent']
s = p.features['Solid extrude-1'].sketch
mdb.models['Model-1'].ConstrainedSketch(name='__edit__', objectToCopy=s)
s1 = mdb.models['Model-1'].sketches['__edit__']
g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
s1.setPrimaryObject(option=SUPERIMPOSE)
p.projectReferencesOntoSketch(sketch=s1, 
    upToFeature=p.features['Solid extrude-1'], filter=COPLANAR_EDGES)
d[4].setValues(value=alpha*radius_2, )
d[3].setValues(value=radius_2, )
d[8].setValues(value=radius_4, )
d[9].setValues(value=beta*radius_4, )
d[7].setValues(value=lenght, )
d[5].setValues(value=lenght, )
s1.unsetPrimaryObject()
p = mdb.models['Model-1'].parts['Ark_stent']
p.features['Solid extrude-1'].setValues(sketch=s1)
del mdb.models['Model-1'].sketches['__edit__']
p = mdb.models['Model-1'].parts['Ark_stent']
p.regenerate()

#----------------------------------------------------------------------------
#                                       remesh.
#----------------------------------------------------------------------------

p = mdb.models[model_name].parts[part_name]
p.seedPart(size=seed_size, deviationFactor=0.1, minSizeFactor=0.1)
p = mdb.models[model_name].parts[part_name]
p.generateMesh()
a = mdb.models[model_name].rootAssembly
a.regenerate()

#----------------------------------------------------------------------------
#                                 job execution.
#----------------------------------------------------------------------------

#try:
mdb.jobs[job_name].submit(consistencyChecking=OFF)
mdb.jobs[job_name].waitForCompletion()

 #----------------------------------------------------------------------------
#                               post process odb.
#----------------------------------------------------------------------------

o1 = session.openOdb(name=odb_name)
odb = session.odbs[odb_name]

last_frame = odb.steps[step_name].frames[-1]


#Von Mises max
stress_field = last_frame.fieldOutputs['S'].values


max_mises = 0.0
i = 0
                    
for v in stress_field:
    if v.mises > max_mises:
        i = v.elementLabel
        max_mises = max(v.mises, max_mises)


        
#Displacement max
displacement_field = last_frame.fieldOutputs['U'].values

max_displacement = 0.0
i = 0

for v in displacement_field:
        if v.magnitude > max_displacement:
            i = v.elementLabel
            max_displacement = max(v.magnitude, max_displacement)

minus_max_displacement = -max_displacement

#----------------------------------------------------------------------------
#                               Writting output file.
#----------------------------------------------------------------------------		

file = open(output_file, 'w')
file.write('max_mises \n')
file.write('%10f \n' % (max_mises))
file.write('minus_max_displacement \n')
file.write('%10f \n' % (minus_max_displacement))
file.close()

#except AbaqusException, e:
    #handling error