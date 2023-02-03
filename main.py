from AbstractionConstructor import epa_constructor

 

print("Contract to analyze")
path = input()
print("Desired path to output")
output = input()

epaC = epa_constructor(path,output)
epaC.construct_abstraction()