import random

random_number_list = [] #Creating blank List

for i in range(100): # For loop to run 100 times
  random_number_list.append(random.randrange(1,1000)) #Adding 100 random numbers in List

temp = 0 #Declaring variable to store value during interchanging of numbers in loop
for i in range(len(random_number_list)): #Outer For loop to Iterate List
    for j in range(len(random_number_list)): #Inner For loop to Iterate List
        if random_number_list[i] < random_number_list[j]: #Checking if List number is smaller than other numbers
            temp=random_number_list[i] #assigning List number to temp variable
            random_number_list[i]=random_number_list[j] #Intechanging List number with Other
            random_number_list[j]=temp #Interchanging other List number with temp variable

even_numbers_count = 0 #Declaring variable to store even numbers count
even_numbers_sum = 0 #Declaring variable to store even numbers sum
even_numbers_avg = 0 #Declaring variable to store even numbers average
odd_numbers_count = 0 #Declaring variable to store odd numbers count
odd_numbers_sum = 0 #Declaring variable to store odd numbers sum
odd_numbers_avg = 0 #Declaring variable to store odd numbers average

for num in random_number_list: #For loop to Iterate List
    if num%2==0: #remainder of number divide by 2 is 0 or not. If remainder is 0 then its even number
        even_numbers_count = even_numbers_count+1 #incrementing even number count by 1
        even_numbers_sum = even_numbers_sum+num #adding even numbers
    else: #remainder is not 0 then its odd number
        odd_numbers_count = odd_numbers_count + 1 #incrementing even number count by 1
        odd_numbers_sum = odd_numbers_sum + num #adding odd numbers

even_numbers_avg = even_numbers_sum/even_numbers_count #average of even numbers
odd_numbers_avg = odd_numbers_sum/odd_numbers_count #average of odd numbers
print("Average of even numbers is",even_numbers_avg) #printing average of even numbers
print("Average of even numbers is",odd_numbers_avg) #printing average of odd numbers



