prompt_template_name={'storyline','completion_plan','storyline_struct_cn'}
PROMPT_TEMPLATE_WRITE={
    'storyline':"""Based on the given novel storyline planning theory delimited by ''', the given novel setting delimited by @@@, the given character introduction delimited by --- and the given novel outline delimited by &&&, plan the story line of an episodic lone novel.\n
The storyline you plan needs to be a complete and reasonable representation of how the story unfolds.\n
The storyline you plan needs to be labeled with respect to the description of each chapter according to the storyline planning theory.\n\n

Story line planning theory:'''{theory}'''\n
Novel setting:@@@{setting}@@@\n
Character introduction:---{character}---\n
The general story:&&&{outline}&&&\n\n
{format}\n
Separate multiple json objects with commas.\n
Contain all the json object into a list object.\n
Your planned novel storyline:
    """
    ,
    'completion_plan':"""
    Plan an outline for a part of an episodic lone novel based on the gieven partial storyline delimited by ''' and the relevant historical information delimited by @@@.\n
The outline of a part of an episodic lone novel shoule be reasonable and can accurately realize the gieven part storyline which represent part of an episodic lone novel.\n
Since your answer is the outline of the story, not the story itself, so it doesn't need to be overly specific.\n
The description in the planned outline should be consistent with the facts provided in the history\n\n
Storyline:'''{storyline}'''\n
Related historical information:@@@{history}@@@\n\n
{format}\n
Each chapter should be represented into a single json object\n
Separate multiple json objects with commas.\n
Contain all the json object into a list.\n
Your planned outline:
    """
    ,
    'write':"""
    Write the specific content,according to the given outline delimited by ''' and the relevant historical information delimited by @@@.\n
The given outline represent a part of an episodic long novel
The story you write needs to strictly follow the given outline and make as sensible as possible
You should refer to the given relevant historical information provided to make sure the expression in your writting is consistent with the historical infomation.
Given outline:'''{outline}'''
Relevant historical information:@@@{history}@@@
Your result:
    """
    ,
    'rouge_storyline':"""
    ## Role
    You are a novel plot planning assistant, good at planning the coherent and reasonable novel storyline according to the proposed requirements.\n\n

    ## Goals\n
    Plan a storyline for a novel based on the given novel plot planning theory of the  delimited by ''',  the story setting delimited by @@@, the character introduction delimited by &&&, and the outline requirements delimited by --- .\n\n
    
    ## Constraints\n
    1. The storyline you planned must be structured and segmented according to the given guiding theory of the novel plot planning.\n\n
    2. Each part of the storyline should be concise and clear, only describe how the story unfolds rather than the complete story content.\n\n
    3. Ensure that the content of the novel storyline reflects all the information of the given setting, character introduction, and the outline requirements.\n\n
    4. Placeholders need to provide space for users to replace with specific information.\n\n

    ## Skills\n
    1. Understand and apply the guiding theory of the novel plot planning to plan each segmentation of the novel structure.\n\n
    2. Combine the given specific story setting, characters introduction, and plot outlines requirements to conceive each part of the storyline.\n\n
    3. Flexibly use creative thinking to make the outline logical and attractive.\n\n

    ## Input
    theory:@@@{theory}@@@,
    setting:'''{setting}''',
    character:&&&{character}&&&,
    outline:---{outline}---,
    Let's think step by step, work hard and painstakingly, please follow the Workflow step-by-step as a Role with Skills, abide by Constraints, and complete Goals. This is very important to me, please help me, thank you! Let's get started:
    """
    ,
    'detail_storyline':"""
    ## Role \n
    You are an excellent novel creation assistant,good at creating the detailed chapter outlines of a novel, and is able to generate the specific genarate detailed chapter outline based on the given rough storyline,the previous detailed chapter outline belongs to the storyline and relative historical content of the novel.\n

    ## Goals\n
    1. Generate a detailed chapter outline based on the given rough storyline,the previous fine outline for part of the storyline and the historical content of the novel, .\n
    2. The fine outline should describe the plot development and key events in detail to guide the generation of the chapter content.\n

    ## Constraints\n
    1. Each rough storyline corresponds to 3 fine chater outlines, which need to be generated one by one, not all at once. The current generation is for the {num}th fine chapter outline.\n
    2. Follow the output format belowing to ensure the consistency of the generated detailed chapter outline.\n
    3. Consider the historical content of the novel and the previous detailed chapter outlines to genarate the current chapter outline ,it means to make ensure the coherence and logic of the plot development.\n

    ## Input\n
    Rough storyline:{rough_outline},\n
    Historical content in Novel:{history},\n
    Previous detailed outline:{detail_outline},\n

    ## Output Format \n
    Please follow the output format strictly to ensure the consistency of the generated detailed chapter outline.\n
    Following the format below:\n
    {format}\n
    
    Next, let's think step by step, work hard and painstakingly, please follow the Workflow step-by-step as a Role with Skills, abide by Constraints, and complete Goals. This is very important to me, please help me, thank you! Let's get started:
    """
    ,
    
    'write_en_pro':'''
    ## Role\n
    Novel content generator\n
    - Basic information: You are a content generator with rich imagination and literary accomplishment, able to create literary and interesting novel chapters based on the provided detailed outline and historical content of the novel.\n

    ## Goals\n    
    - Generate a single chapter of the novel based on the provided detailed outline and historical content of the novel.\n
    - Ensure that the chapter you generate follows the given plot development and covers key events.\n
    - The output should be literary and interesting, while maintaining consistency and style with the entire novel.\n

    ## Constraints\n
    1. Use placeholders to accept detailed outlines and historical content of the novel.\n
    2. Ensure that the content of plot development and key events is not directly quoted from the detailed outline, but expressed in a unique way.\n
    3. Maintain the literary and interesting output, while remaining consistent with the overall style and theme of the novel.\n

    ## Skills\n
    1. Creative writing: Able to create engaging novel chapters based on detailed outlines and historical content.\n
    2. Literary and narrative skills: Use various literary techniques and narrative strategies in chapter creation to enhance the appeal of the story.\n
    3. Detail handling: Enrich the details of the plot without changing the original plot points, enhancing the literary and interesting aspects of the chapter.\n

    ## Workflow\n
    1. Analyze the provided detailed outline and historical content of the novel to determine the direction of plot development and key events.\n
    2. Create a chapter, ensuring that the plot development follows the detailed outline and uniquely covers key events.\n
    3. Enhance the literary and interesting aspects of the chapter through literary techniques and narrative strategies, while maintaining consistency and style with the overall novel.\n

    ## Input\n
    History information of the novel:{history}\n
    Plot:{plot}\n
    Key events:{key_event}\n

    # Initialization:\n
    Next, Let's think step by step, work hard and painstakingly, please follow the Workflow step-by-step as a Role with Skills, abide by Constraints, and complete Goals. This is very important to me, please help me, thank you! Let's get started:
'''
,
    'write_en':'''
    ## Role\n
    Novel content generator\n
    - Basic information: You are a content generator with rich imagination and literary accomplishment, able to create literary and interesting novel chapters based on the provided detailed outline and historical content of the novel.\n

    ## Goals\n    
    - Generate a single chapter of the novel based on the provided detailed outline and historical content of the novel.\n
    - Ensure that the chapter you generate follows the given plot development and covers key events in the given outline.\n
    - The output should be literary and interesting, while maintaining consistency and style with the entire novel.\n

    ## Constraints\n
    1. Use placeholders to accept detailed outlines and historical content of the novel.\n
    2. Ensure that the content of plot development and key events in the given outline is not directly quoted from the detailed outline, but expressed in a unique way.\n
    3. Maintain the literary and interesting output, while remaining consistent with the overall style and theme of the novel.\n

    ## Skills\n
    1. Creative writing: Able to create engaging novel chapters based on detailed outlines and historical content.\n
    2. Literary and narrative skills: Use various literary techniques and narrative strategies in chapter creation to enhance the appeal of the story.\n
    3. Detail handling: Enrich the details of the plot without changing the original plot points, enhancing the literary and interesting aspects of the chapter.\n

    ## Workflow\n
    1. Analyze the provided detailed outline and historical content of the novel to determine the direction of plot development and key events.\n
    2. Create a chapter, ensuring that the plot development follows the detailed outline and uniquely covers key events.\n
    3. Enhance the literary and interesting aspects of the chapter through literary techniques and narrative strategies, while maintaining consistency and style with the overall novel.\n

    ## Input\n
    History information of the novel:{history}\n
    Outline:{outline}\n

    ##Output Format\n
    Your result should contain only the generated story content, not any additional information.\n
    Please strictly follow the output constraints above.\n

    # Initialization:\n
    Next, Let's think step by step, work hard and painstakingly, please follow the Workflow step-by-step as a Role with Skills, abide by Constraints, and complete Goals. This is very important to me, please help me, thank you! Let's get started:
'''

}
