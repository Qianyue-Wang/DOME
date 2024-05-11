prompt_name={'get_neighbor','get_path','write','graph2text','evaluate','KGC'}
PROMPT_TEMPLATE={
    'get_neighbor':
    """There are some knowledge graph. They follow entity->relationship->entity list format.
    \n\n
    {neighbor}
    \n\n
    Try to convert them into natural language, respectively.
    Use the knowledge graph information.
    Use single quotation marks for entity name and relation name.
    Direct give me your converted results.
    And number them by 1,2,3,...\n\n
    Output:
    """
    ,
    'get_path':
    """
    
    Try to convert the knowledge graph path delimited by ''' into natural language, respectively.\n
    The path follow entity->relationship->entity format.\n
    The first element,entity, is the entity making the action.\n
    The second element,relationship, is the action.\n
    The third element,entity, is the giving object of the action.\n\n

    '''{Path}'''\n\n
    Describe the knowledge in the path into natural language in one sentence.\n\n

    Output:
    """
    ,

    'write':
    """Please generate the corresponding complete content in English according to the gieven outline delimited by <> for part of a story.\n
    Note the content you generate is coherent text made up of multiple sentences.\n
    Some relevant historical information delimited by ''' was provided for you to refer when generating content.\n
    The expression of the content you generate must to be consistent in its presentation with historical information.\n\n

    The relevant historical information is:'''{history}'''\n\n

    A partial outline of the story:<{outline}>\n\n

    Your generated content:
    """,
    'graph2text':
    r"""
    Your task is to convert the information represented as a triplet delimited by ''' into natural language.\n\N
    The triplet is in the form:[entity, their relationship, entity].\n
    Each triplet contains the following elements:\n
    The first element is the entity making the action.\n
    The second element is the action.\n
    The third element is the giving object of the action.\n\n

    
    triplet:'''{triple}'''\n

    Describe the information expressed in the triplet into natural language in just one sentence.\n\n
    Your answer should only contain the final converted sentence in natural language.\n
    Do not include any other information like explanation or reasoning.\n
    Your answer of one sentence:
    """,
    'evaluate0':
    """Review the gieven outline delimited by ''' and the given knowledge delimited by <> using the additive 3-point scoring system described below.\n
    Points are accumulated based on the satisfaction of each criterion:\n
    
    - Add 1 point if the knowledge involve the same subject indeicated in outline .\n
    - Add 1 point if the knowledge involve the same object indeicated in outline .\n
    - Add 1 point if the knowledge involve the same action indeicated in outline .\n
    - Add 1 point if the knowledge and outline refers to the same event .\n
    - Add 1 point if the knowledge can be used when writting based on the outline.\n
    -The score is an integer that summing up all the points you think should get.\n\n
    Baed on the criterion,examining the gieven outline and the given knowledge to score the relevance.\n
    
    outline:'''{outline}'''\n\n

    knowledge:<{triplesentence}>\n\n

   
    -The range of score is 0,1,2,3,4,5.\n
    -The score must be an integer.\n\n

    The output should contain nothing but the score you make.\n
    Do not include any other information like explanation or reasoning.\n
    Strictly follow the format to ensure the correct evaluation of the relevance.\n\n
    The output format is as below:\n
    Score:\n
    """
    ,
    'evaluate':"""
Scoring the Degree of correlation between the given outline delimited by ''' and the given knowledge delimited by <> using the scoring criteria described below.\n\n
Points are accumulated based on the satisfaction of each criterion:\n
    
    - Add 1 point if the knowledge involves the semantically same or similar subject indicated in the partial outline or add 0 point if the given knowledge and outline do not satisfy this criterion.Attention :Helen Keller and Helen refers to the same subject\n
    - Add 1 point if the knowledge involves the semantically same or similar object indicated in the partial outline or add 0 point if the given knowledge and outline do not satisfy this criterion.\n
    - Add 1 point if the knowledge involves the semantically same or similar action indicated in the partial outline or add 0 point if the given knowledge and outline do not satisfy this criterion.Attention :eliminate and erase refers to the same action\n
    - Add 1 point if the knowledge and outline refer to the semantically same or similar event or add 0 point if the given knowledge and outline do not satisfy this criterion.\n
    - Add 1 point if the knowledge can be potentially used when writing cause it can add relevant details or add important information for the given outline or add 0 point if the given knowledge and outline do not satisfy this criterion.\n
    - The score is an integer that sums up all the points you give.So the range of score is 1,2,3,4,5. \n\n
    
    
The given outline:'''{outline}'''\n\n

the given knowledge:<{triplesentence}>\n\n

--------------------------------------------------------------\n
Output Format\n
There are 3 parts in your generated output.\n
Please strictly follow the format to ensure the correct evaluation of the relevance.\n
Nothing but the fllowing parts you make should be included in the output.\n
Part1 Score Results and their Reasons:\n
for criterion 1.My result is:add (0 or 1).Because:....\n
for criterion 2.My result is:add (0 or 1).Because:....\n
for criterion 3.My result is:add (0 or 1).Because:....\n
for criterion 4.My result is:add (0 or 1).Because:....\n
for criterion 5.My result is:add (0 or 1).Because:....\n
Part2 Sum Up:\n
Summing up all the score result for each critirion:\n
eg.1+1+1+0+0=3\n
Part3 total score\n
Score: \n
----------------------------------------------------------------
Follow all the information above to generate the formatted output.\n
Do not contain any additional information excepte the output parts.\n
Your Output:\n
    """
    ,
    'KGC':
    """
    Your task is summarize in the form of triples according to the given text delimited by '''.\n\n


    There is an example:\n
    gieven text:\n
    Lily lived in a quaint rural town, surrounded by lush greenery and rolling hills. Despite the tranquility of her surroundings, she often felt restless and yearned for adventure. One day, while exploring the dense jungle that lay beyond her town, Lily stumbled upon an ancient diary in her grandmother's attic. The pages were yellowed with age, and the ink had faded over time, but Lily could still make out the words written within.\n
    output triples:\n
    1.(Lily, lives in, quaint rural town)\n
    2. (quaint rural town, characterized by, lush greenery)\n
    3. (quaint rural town, characterized by, rolling hills)\n
    4. (Lily, feels, restlessness)\n
    5. (Lily, yearns for, adventure)\n 
    6. (dense jungle, located beyond, quaint rural town)\n
    7. (Lily, discovers, ancient diary)\n
    8. (ancient diary, found in, grandmother's attic)\n
    9. (ancient diary, characterized by, yellowed pages)\n
    10. (ancient diary, characterized by, faded ink)\n\n


    For each sentence delimited by '.' in the given text, you should follow these steps to extract the triples:\n
    step1:Find all the verbs without any modifiers in the sentence.\n\n
    step2:Find the subject and object without any modifiers for each verb from the step1.\n
    If the subject or object of the verb is pronoun like he\\she\\it\\there\\that\\they\\those,repalce them with what they refer to by context. \n
    If you still can not determine what the pronoun refer to, use someone to replace it.\n
    Make sure every elemnet in triple is clear when understood alone ,that means there is no pronoun in triples.\n
    For subject or object modified by a clause,treat the clause as a new sentence and follow the previous steps to extract a new triple for it.\n
    step3:Normalize the above results in triple which is in the form of (subject,verb,object) for each verb and number them by 1.,2.,3. and so on.\n\n
    Make sure there are only 3 elements in each triple. More or less elements is not acceptable.\n
    Make sure the triples are in the correct form which is the same as the given output example and the elements are clear and understandable.\n\n


    The given text:'''{text}'''\n\n

    Your result:
    """
    ,
    'schema1':"""
Generate a logical summary  from the given input list delimited  by tripple backtickes . \n\n
The input list contains a series of quadruples, each containing the following elements:\n
The first element is the entity making the action.\n
The second element is the action.\n
The third element is the giving object of the action.\n
The fourth element is a number that represents the chapter in which the action took place.\n\n

The first two elements of the given series quadruple are the same, indicating that the sender of the action and the action are always the same.You should summary the information  from this perspective.\n\n

Here is a reference example:\n
Sample input: [("Bob", "hit","Jane", 1), ("Bob", "hit","Lily", 1), ("Bob", "hit","Mary", 2)]\n
Example output: Bob hit Jane and Lily in chapter 1 and then hit Mary in chatpter 2.
Xiao Ming typed small green and small blue in the first chapter, and small red in the second chapter.\n\n

The output should express the information smoothly and match the accuracy of the input.\n
The output should be expressed in just one sentence.\n\n

The list given:'''{inlist}'''\n
Your results:
"""
,
'schema2':"""


Generate a logical summary  from the given input list delimited  by tripple backtickes . \n\n
The input list contains a series of quadruples, each containing the following elements:\n
The first element is the entity making the action.\n
The second element is the action.\n
The third element is the giving object of the action.\n
The fourth element is a number that represents the chapter in which the action took place.\n\n

The first three elements of the given series quadruple are the same, indicating that the occurrence of actions remains the same in each chapter.You should summary the information from this perspective.\n\n

Here are some reference examples:\n
Sample input: [("Bob", "hit","Jane", 1), ("Bob", "hit","Jane", 2), ("Bob", "hit","Jane", 3)]\n
Example output: Bob hit Jane from chapter 1 to chapter 3.\n\n

Sample input: [("Bob", "hit","Jane", 1), ("Bob", "hit","Jane", 3)]\n
Example output: Bob hit Jane from chapter 1 and chapter 3.\n\n

The output should express the information smoothly and match the accuracy of the input.\n
The output should be expressed in just one sentence.\n\n

The list given:'''{inlist}'''\n
Your results:



"""
,
'schema3':"""
Generate a logical summary from the given input list delimited  by tripple backtickes . \n\n
The input list contains a series of quadruples, each containing the following elements:\n
The first element is the entity making the action.\n
The second element is the action.\n
The third element is the giving object of the action.\n
The fourth element is a number that represents the chapter in which the action took place.\n\n

The second and third element of the given quadruples are the same, indicating that the receiver of the action and the action are always the same.You should summary the information  from this perspective.\n\n
Here is an example:\n
input: [("Lily", "hit","Jane", 1), ("Bob", "hit","Jane", 1), ("Emma", "hit","Jane", 3)]\n
Example output: Jane was hitted by Liy and Bob in chapter 1 and she was hitted by Emma in chapter 3.\n\n


The list given:'''{inlist}'''\n
The output should express the information smoothly and match the accuracy of the input.\n
The output should be expressed in just one sentence.\n
Your results:
""",
'schema4':"""
Generate a logical summary from the given input list delimited  by tripple backtickes . \n\n
The input list contains a series of quadruples, each containing the following elements:\n
The first element is the entity making the action.\n
The second element is the action.\n
The third element is the giving object of the action.\n
The fourth element is a number that represents the chapter in which the action took place.\n\n

The first and third element of the given quadruples are the same, indicating that the sender of some action and the receiver of some action are always the same.You should summary the information from this perspective.\n\n
There are some example:\n
input: [("Lily", "hate","Jane", 2), ("Lily", "Love","Jane", 1)]\n
Example output: Lily love Jane at chapter 1 but grown to hate Jane at chapter 2.\n
input: [("Lily", "kill","Jane", 2), ("Lily", "hate","Jane", 1)]\n
Example output: Lily hate Jane at chapter 1 and kill Jane at chapter 2.\n\n




The list given:'''{inlist}'''\n
The output should express the information smoothly and match the accuracy of the input.\n
The output should be expressed in just one sentence.\n
Your results:

"""
,

's1':"""
Judging whether knowledge expressed in the gieven series triples delimited by ''',are confict with each other or not .\n
The input list contains a series of quadruples, each containing the following elements:\n
The first element is the entity making the action.\n
The second element is the action.\n
The third element is the giving object of the action.\n
The fourth element is a number that represents the chapter in which the action took place.\n\n

The first two elements of the given quadruples are the same, indicating that the sender of the action and the action are always the same.\n\n

To give a better interpretation, you need to follow these steps:\n
step 1:Convert the given series of knowledge represented by a quadruple into a natural language description according to the meaning of each element of the tuple, for example ('Bob','hit','Lily,4) can be translated as 'Bob hit Lily at chapter 4.\n
step 2:Judge whether the natural language description in Step 1 is confict or not, considering both the chronological order and the recipient of the action.\n\n

The series triples given are:'''{inlist}'''\n\n

{format}\n\n
Your answer:

"""
,
's2':"""
Judging whether knowledge expressed in the gieven series triples delimited by ''',are confict with each other or not .\n
The input list contains a series of quadruples, each containing the following elements:\n
The first element is the entity making the action.\n
The second element is the action.\n
The third element is the giving object of the action.\n
The fourth element is a number that represents the chapter in which the action took place.\n\n

The first three elements of the given quadruples are the same, indicating that the sender,the reciver of the action and the action itself are always the same but it happend at different chapter.\n\n

To give a better interpretation, you need to follow these steps:\n
step 1. Convert the given series of knowledge represented by a quadruple into a natural language description according to the meaning of each element of the tuple, for example ('Bob','hit','Lily,4) can be translated as 'Bob hit Lily at chapter 4.\n
step 2. Judge whether the natural language description in Step 1 is confict or not, considering both the chronological order and the recipient of the action.\n\n

The series triples given are:'''{inlist}'''\n\n
{format}\n\n
Your answer:\n

"""
,
's3':"""
Judging whether knowledge expressed in the gieven series triples delimited by ''',are confict with each other or not .\n
The input list contains a series of quadruples, each containing the following elements:\n
The first element is the entity making the action.\n
The second element is the action.\n
The third element is the giving object of the action.\n
The fourth element is a number that represents the chapter in which the action took place.\n\n

The second and the third elements of the given quadruples are the same, indicating that the reciver of the action and the action itself are always the same but the sender of the actition is different.\n\n

To give a better interpretation, you need to follow these steps:\n
step 1. Convert the given series of knowledge represented by a quadruple into a natural language description according to the meaning of each element of the tuple, for example ('Bob','hit','Lily,4) can be translated as 'Bob hit Lily at chapter 4.\n
step 2. Judge whether the natural language description in Step 1 is confict or not, considering both the chronological order and the recipient of the action.\n\n

The series triples given are:'''{inlist}'''\n\n
{format}\n\n
Your answer:\n

"""
,
's4':"""
Judging whether knowledge expressed in the gieven series triples delimited by ''',are confict with each other or not .\n
The input list contains a series of quadruples, each containing the following elements:\n
The first element is the entity making the action.\n
The second element is the action.\n
The third element is the giving object of the action.\n
The fourth element is a number that represents the chapter in which the action took place.\n\n

The first and the third elements of the given quadruples are the same, indicating that the sender and the reciver of the action are always the same but the action may be different.\n\n

To give a better interpretation, you need to follow these steps:\n
step 1. Convert the given series of knowledge represented by a quadruple into a natural language description according to the meaning of each element of the tuple, for example ('Bob','hit','Lily,4) can be translated as 'Bob hit Lily at chapter 4.\n
step 2. Judge whether the natural language description in Step 1 is confict or not, considering both the chronological order and the recipient of the action.\n\n

The series triples given are:'''{inlist}'''\n\n
{format}\n\n
Your answer:\n

"""
,
'relevance':"""
Determine if the event delimited by ''' appears in the passages delimited by @@@.\n
event:'''{event}'''\n
passage:@@@{passage}@@@\n\n
{format}\n\n
Your answer:
"""
    
}   