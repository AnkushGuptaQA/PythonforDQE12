import re
import string

#created a variable and assign value of provided text
text = """  tHis iz your homeWork, copy these Text to variable.



  You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.



  it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.



  last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87."""
normalized_text = '' #created variable to store normalized text
normalized_text_after_fix_iz = '' #created variable to store text after replacing "iz" with "is"
new_sentence = '' #created variable to store new sentence

formatted_text = re.split(r'(?<=\.)\s+', text.strip()) #Splitting text after "." to sentences and removing extra spaces
for i in range(len(formatted_text)): #loop to read sentences
    a = formatted_text[i].lower().capitalize() #Changing all characters to lower case and updating first character of sentence to Upper Case
    normalized_text = normalized_text+a+" " #adding updated sentences to variable
print(normalized_text) #printing normalized text

normalized_text_after_fix_iz = re.sub(r'\b iz\b', ' is', normalized_text) #replacing "iz" with "is"
print(normalized_text_after_fix_iz) #printing text after replacing "iz" with "is"

sentences = re.split(r'(?<=[.!?])\s+', normalized_text_after_fix_iz)  #Split into sentences
last_words = [sentence.rstrip('.!?').split()[-1] for sentence in sentences if sentence != ""] #picking last word of sentences
new_sentence = " ".join(last_words)+ "." #combining words to make new sentence

new_text = normalized_text_after_fix_iz  + " " + new_sentence #Adding new sentence to the end of the normalized text
print(new_text) #printing new text

#printing Number of Whitespaces in provided Text
print("Number of Whitespaces in provided text is",text.count(" ")+text.count("\n")+text.count("\t"))
#Note - I am getting count as 89. Tried multiple ways but still getting 89. If expected count is 87 then might be some extra whitespaces included while coping text from Exercise.


