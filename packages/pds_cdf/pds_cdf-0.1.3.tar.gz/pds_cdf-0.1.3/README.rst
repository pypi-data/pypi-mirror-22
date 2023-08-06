This is a python script to read PDS4 compliant CDF files
without needing to install the CDF NASA library.  

Creates a CDF file variable, and then access the variable with 
the commands:

Attribute Inquiry:  attinq( attribute_name )
                    Returns a python dictionary of attribute information
                   
Get Attribute:      attget( attribute_name, entry_number )
                    Returns the value of the attribute at the entry number provided
                   
Variable Inquiry:   varinq( variable_name )
                    Returns a python dictionary of variable information 
                   
Get Variable:       varget( variable_name )
                    Returns a numpy array of all of the variable records


Sample use - 

    import pds_cdf
	
    swea_cdf_file = pds_cdf.CDF('/path/to/swea_file.cdf')
	
    x = swea_cdf_file.varget("NameOfVariable")

Author: Bryan Harter
