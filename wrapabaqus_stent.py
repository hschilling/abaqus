from openmdao.lib.datatypes.api import Float
from os import system
from openmdao.lib.components.api import ExternalCode
from openmdao.main.api import FileMetadata
from openmdao.util.filewrap import InputFileGenerator, FileParser

class WrapAbaqus_stent(ExternalCode):


    #-------------------------------------------------------------------------------
    #                                   Variables definition
    #-------------------------------------------------------------------------------


    lenght=Float(3.7, iotype='in', desc='position of the center of the first circle')
    radius_2=Float(0.4, iotype='in', desc='external radius of the top')
    radius_4=Float(4.0, iotype='in', desc='external radius of the side')
    alpha=Float(0.4, iotype='in', desc='radius_1=alpha*radius_2')
    beta=Float(1.05, iotype='in', desc= 'radius_3=beta*radius_4')

    max_mises=Float(0.0, iotype='out', desc='the maximal Von Mises stress at integration point')
    minus_max_displacement=Float(0.0, iotype='out', desc='minus the maximal displacement')


    #-------------------------------------------------------------------------------
    #                                   Component initialisation
    #-------------------------------------------------------------------------------


    def __init__(self):
        
        super(WrapAbaqus_stent,self).__init__()
        
        self.input_file = 'ark_stent.py'
        self.output_file = 'output.txt'
        self.command= ['C:/Users/tbrosse/.openmdao/gui/projects/Stent/launcher.bat'] 
            
        self.external_files = [FileMetadata(path=self.input_file, input=True), FileMetadata(path=self.output_file), ]

    #-------------------------------------------------------------------------------
    #                                   Component execution
    #-------------------------------------------------------------------------------

            
    def execute(self):

        

        lenght=self.lenght
        radius_2=self.radius_2
        radius_4=self.radius_4
        alpha=self.alpha
        beta=self.beta
        
        
        # Prepare the input file
        
        system('del ark_stent.py')  # deletes previous input file

        parser = InputFileGenerator()
        parser.set_template_file('template.py')
        parser.set_generated_file('ark_stent.py')
        
        
        parser.reset_anchor()
        parser.mark_anchor("lenght")
        parser.transfer_var(lenght, 0, 2)
        
        parser.reset_anchor()
        parser.mark_anchor("radius_2")
        parser.transfer_var(radius_2, 0, 2)
        
        parser.reset_anchor()
        parser.mark_anchor("radius_4")
        parser.transfer_var(radius_4, 0, 2)
        
        parser.reset_anchor()
        parser.mark_anchor("alpha")
        parser.transfer_var(alpha, 0, 2)
        
        parser.reset_anchor()
        parser.mark_anchor("beta")
        parser.transfer_var(beta, 0, 2)
            
        parser.generate()
    
    
        #Run Abaqus vi External's code execute function

        super(WrapAbaqus_stent, self).execute()


        #Parse the output files from abaqus

        parser = FileParser()
        parser.set_file('output.txt')
        
        parser.reset_anchor()
        parser.mark_anchor("max_mises")
        var = parser.transfer_var(1, 1)
        self.max_mises=var
        
        parser.reset_anchor()
        parser.mark_anchor("minus_max_displacement")
        var = parser.transfer_var(1, 1)
        self.minus_max_displacement=var
        
        
        print self.return_code