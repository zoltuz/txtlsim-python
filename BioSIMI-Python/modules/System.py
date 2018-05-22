from modules.Subsystem import *

class System(object):
    def __init__(self, SystemName):
        self.SystemName = SystemName
        self.ListOfSubsystemsInThisSystem = []
        self.ListOfSharedResources = []
    
    def getSystemName(self):
        return self.SystemName

    def setSharedResources(self):
        ListOfResources = self.ListOfSharedResources
        # Create a blank document for the final connected system and the subsystem object
        final_sbml_doc = createSubsystemDoc(3,1)
        Final_subsystem = Subsystem(final_sbml_doc)
        Final_subsystem.setSystem(self)
        # The shareSubsystems member function implements Example 1-A.
        # Usage - self.shareSubsystems(ListOfSubsystems, ListOfSharedResources)
        Final_subsystem.shareSubsystems(self.ListOfSubsystemsInThisSystem, ListOfResources)
        return Final_subsystem

    def createSubsystem(self, filename, subsystemName):
    # 1. Read the SBML model
    # 2. Create an object of the Subsystem class with the SBMLDocument read in Step 1
        name = self.getSystemName()
        sbmlDoc = getFromXML(filename)
        subsystem = Subsystem(sbmlDoc)
        subsystem.setSystem(self)
        if subsystem.getSubsystemDoc().getLevel() != 3:
            print('Subsystem SBML model is not the latest. Converting to SBML level 3, version 1')
            subsystem.convertSubsystemLevelAndVersion(3,1)

        writeSBML(subsystem.getSubsystemDoc(), 'models/txtl_mod_converted_level.xml')
        subsystem.suffixAllElementIds(subsystemName)
        if sbmlDoc.getModel().getNumCompartments() > 1:
            print('More than 1 compartments in the model')
        subsystem.setSubsystemCompartments([name])
        self.ListOfSubsystemsInThisSystem.append(subsystem)
        return subsystem 

    def createNewSubsystem(self, level, version):
        newDocument = createSubsystemDoc(level,version)
        subsystem = Subsystem(newDocument)
        subsystem.setSystem(self)
        return subsystem