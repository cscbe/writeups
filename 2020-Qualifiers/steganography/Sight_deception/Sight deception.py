# We never know if this could come in handy
import string  					 	
   		  		
# The string to write		  		
mystring = "What are you looking for?"			  		
   	 					
# Will hold the result		    
out = "   \n"			 	  
   	 					
#This loop will generate out character by character			  	 
for c in mystring[::-1]:		  		
    # First, what type?		  	  
    out += "   "			  	 
    	      
    # It's easier if it's a number		 	   
    i = ord(c)	 					
    		 			 
    # From here the magic takes place		  		
    # We convert our beautiful number into a binary string			 		 
    out += "{0:b}\n".format(i)		  		
    	 					
    # Now we just have to translate the binary			  		
    # First the ones			 	  
    out = out.replace('1', '	')	   	
    # Then the zeros...				 		
    out = out.replace('0', ' ')	    		
    # That was pretty easy, right?	 	  		
   	    		
# Ok,Now to finish...!

# End!
	
out+="""
  
 
 
	 	
	
  
 


  	



"""

# Let's now get the result!
open("result.txt", "w").write(out)