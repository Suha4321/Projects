
##############################################################################################################
# Import required module
##############################################################################################################
import os
import sys
import csv
from csv import reader
import time
from decimal import *



##############################################################################################################
# Test Functions
##############################################################################################################
# store the product file name in the variable
my_path_prod =str(sys.argv[2])

# store the product_order file in the variable
my_path_prod_orders = str(sys.argv[1])


# Define a function to test for empty file
def empty_file(my_path ):
    # if the path exists and if getsize method raises error then we note a empty file
    if os.path.exists(my_path) and os.path.getsize(my_path) > 0:
        pass
    else:
        filename = (os.path.basename(my_path))
        print("the file " + filename +" is empty")



# Check for empty product file using empty_file function
empty_file(my_path_prod)

# check for empty product order file using empty_file function
empty_file(my_path_prod_orders)


##############################################################################################################
# Read files
##############################################################################################################

# Create a function to get the specified columns from the product data set.
# The funciton returns a dictionary object with dept_id as key and products a value list.
    # parameters :
            #- fine_name = name of the file
            #- - num1 = the column index that provides dictionary key
            #- -num2 = the column index that provides the dictionary value
            #- header + optional parameter; True when the file has header and False otherwise
def read_dataset_to_dict(file_name, num1, num2 , header=True):
    # define the dictionary for storing read data
    data = {}
    # oprn the file
    with open(file_name) as opened_file:
        # read the file
        read_file = reader(opened_file)
        # skip to next line if the file has header else pass
        if header==True:
            next(read_file, None)
        else:
            pass

        # for each line in the read file, if the specified columns are not null, then add then to the dictionary named data
        for rows in read_file:
            if rows[num1] != '' :
                if rows[num2] != '':
                    try:
                        # the method return the key and appends the value to the key in each iteration
                        data.setdefault(rows[num1], []).append(rows[num2])
                    except:
                        continue
        #  retun the required dictionary
        return data


# Create a function to get the specified column from the product_order data set.
# The funciton returns a list object with product_ids that were ordered for first time
    # parameter :
        # - fine_name = name of the file
        # - num1 = the column index that provides product_ids
        # -num2 = the column index that flags products ordered for the first time
        # header + optional parameter; True when the file has header and False otherwise
def read_dataset_to_list(file_name, num1, num2 , header=True):
    # deifne list for storing the read data
    req_list = []
    # open the file
    with open(file_name) as opened_file:
        # read the file
        read_file = reader(opened_file)
        # skip to next line if the file has header else pass
        if header==True:
            next(read_file, None)
        else:
            pass

        # for each row in the read file, if the product is ordered for the first time
        # and if the product_id is not null, it will be appended to the list
        for rows in read_file:
            if rows[num2]=='0':
                if rows[num1] != '':
                    try:
                        some_list = rows[num1]
                        # this method appends the product_id value
                        req_list.append(some_list)
                    except:
                        continue

    #  retun the required list
    return req_list


#Using the two functions defined above, we will read in both product and product_order files

#read product file and store the dictionary of with department_id and corresponding product_id in prod_list
prod_list = read_dataset_to_dict(file_name = my_path_prod, num1 = 3,  num2 = 0, header = True)

# read the product_order file and store the product_id ordered for the first time in prodict_first_order variable
product_first_order = read_dataset_to_list(file_name = my_path_prod_orders,  num1 = 1 , num2 = 3, header = True)

##############################################################################################################
# Analysis
# Look up the department ids for the products ordered for the first time (product_first order list )  in the product_list data dictionary .
# The result will be stored in the first_order_dict
##############################################################################################################
# create a dict for first time products
first_order_dict = {}

# for the key, list of values pair in the prod_list dictionary
for key,value in prod_list.items():
    # for each element in the list of values
    for element in value:
        # if the element is in the list of products ordered for the first time, then obtain the key and append the product as value
        if element in product_first_order:
            first_order_dict.setdefault(key, []).append(element)

##############################################################################################################
# Analysis
# we will use -
    # - product_list dictionary; that has department_id as key and corresponding porduct_ids as a list of values
    # -  first_order_dict ; that has dpertment id  as key and product id as value for the products ordered for the first time
##############################################################################################################

result = []
# set precision value for the Decimal funcitons used in this block
getcontext().prec = 3

# for each of the key, value pair in product_list
for key,value in prod_list.items():
    # total order will be count the values
    total_order = sum(1 for v in value if v)
    # if the count of the values is more than 0
    if total_order > 0:
        # if the key is contained in first_order_dict
        if key in first_order_dict.keys():
            # for the key, value pait in first_order_dict
            for k,v in first_order_dict.items():
                # the count of items in value is the total of first order
                first_order = sum(1 for element in v if element)
        # for the keys that are not contained in first_order_dict
        else:
            # the count of products ordered for the first time is
            first_order = 0
        # ratio is the ratio of count of products ordered for the first time to the total numbe of products ordered
        ratio = str(round(Decimal(first_order/total_order),2))

        # Adding the variables calulated above to a list
        # try to convert the depatment_id to list to enable sorting
        try:
            some_list = [int(key), total_order , first_order, ratio ]
        # if the conversiont int raises and error, print the error
        except ValueError as e:
            print(e)
            continue
    # appending the list to the result list
    result.append(some_list)
# sorting the list to get the ascending value of the departments
result.sort()

##############################################################################################################
# Write to outputfile
    # We will write the result list obetained in the above step into a csv file.
##############################################################################################################

# open the output file
with open(str(sys.argv[3]), mode='w', newline='') as myfile:
    # get a wirter object into the my_writer variable
    my_writer = csv.writer(myfile , delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL )
    # write the header values in the csv
    my_writer.writerow(['department_id','number_of_orders','number_of_first_orders','percentage'])
    # iterate throgh each line of result list and write it in the output file
    for row in result:
            my_writer.writerow(row)
