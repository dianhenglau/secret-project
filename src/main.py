from step_functions import main_menu
from helpers import print_breadcrumb

print('''
    dMMMMMP dMMMMMP dMMMMb  dMMMMb  dMP dMP                        
   dMP     dMP     dMP.dMP dMP.dMP dMP.dMP                         
  dMMMP   dMMMP   dMMMMK" dMMMMK"  VMMMMP                          
 dMP     dMP     dMP"AMF dMP"AMF dA .dMP                           
dMP     dMMMMMP dMP dMP dMP dMP  VMMMP"                            
                                                                   
 dMMMMMMP dMP .aMMMb  dMP dMP dMMMMMP dMMMMMMP dMP dMMMMb  .aMMMMP 
   dMP   amr dMP"VMP dMP.dM" dMP        dMP   amr dMP dMP dMP"     
  dMP   dMP dMP     dMMMK"  dMMMP      dMP   dMP dMP dMP dMP MMP"  
 dMP   dMP dMP.aMP dMP"AM" dMP        dMP   dMP dMP dMP dMP.dMP    
dMP   dMP  VMMMP" dMP dMP dMMMMMP    dMP   dMP dMP dMP  VMMMP"     
                                                                   
   .dMMMb  dMP dMP .dMMMb dMMMMMMP dMMMMMP dMMMMMMMMb              
  dMP" VP dMP.dMP dMP" VP   dMP   dMP     dMP"dMP"dMP              
  VMMMb   VMMMMP  VMMMb    dMP   dMMMP   dMP dMP dMP               
dP .dMP dA .dMP dP .dMP   dMP   dMP     dMP dMP dMP                
VMMMP"  VMMMP"  VMMMP"   dMP   dMMMMMP dMP dMP dMP                 
''')

context = {}
steps = [main_menu]

i = 0
while i >= 0:
    if isinstance(steps[i], str) or steps[i].title:
        print_breadcrumb(steps[:i + 1])

    result = steps[i](context, steps)

    if result == 'B' or result == 'back':
        while True:
            i -= 1
            if callable(steps[i]):
                break
    elif result == 'R' or result == 'return':
        i = 0
    else:
        while True:
            i += 1
            if callable(steps[i]):
                break

print('''
 dMMMMMMP dMP dMP .aMMMb  dMMMMb  dMP dMP     dMP dMP .aMMMb  dMP dMP 
   dMP   dMP dMP dMP"dMP dMP dMP dMP.dM"     dMP.dMP dMP"dMP dMP dMP  
  dMP   dMMMMMP dMMMMMP dMP dMP dMMMK"       VMMMMP dMP dMP dMP dMP   
 dMP   dMP dMP dMP dMP dMP dMP dMP"AM"     dA .dMP dMP.aMP dMP.aMP    
dMP   dMP dMP dMP dMP dMP dMP dMP dMP      VMMMP"  VMMMP"  VMMMP"     
''')
