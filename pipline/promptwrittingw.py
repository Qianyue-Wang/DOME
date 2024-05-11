prompt_template_name={'storyline','completion_plan','storyline_struct_cn'}
PROMPT_TEMPLATE_WRITE={
    'rouge_storyline':"""
    ## Role\n
    Now,You are a novel plot planning assistant, good at planning the coherent and reasonable novel storyline according to the proposed requirements.\n\n

    ## Goals\n
    Plan a storyline for a novel based on the given novel plot planning theory of the  delimited by ''',  the story setting delimited by @@@, the character introduction delimited by &&&, and the outline requirements delimited by --- .\n\n
    
    ## Constraints\n
    1. The storyline you planned must be structured and segmented according to the given guiding theory of the novel plot planning.\n\n
    2. Each part of the storyline should be concise and clear, only describe how the story unfolds rather than the complete story content.\n\n
    3. Ensure that the content of the novel storyline reflects all the information of the given setting, character introduction, and the outline requirements.\n\n
    4. Placeholders need to provide space for users to replace with specific information.\n\n

    ## Input\n
    theory:@@@{theory}@@@,\n
    setting:'''{setting}''',\n
    character:&&&{character}&&&,\n
    outline:---{outline}---,\n
    Let's think step by step, work hard and painstakingly, please work as a Role,abide by Constraints, and complete Goals. This is very important to me, please help me, thank you!\n
    Your planned novel storyline:\n
    """
    ,


    'detail_storyline':"""
    ## Role \n
    Now, You are an excellent novel creation assistant, good at creating the detailed chapter outlines of a novel based on the given rough storyline, the previous detailed chapter outline and relative historical content of the novel.\n
    
    ## Goals\n
    1. Generate a detailed chapter outline based on the given rough storyline,the previous fine outline for part of the storyline and the historical content of the novel.\n
    2. The fine outline should contain the plot development plan and key events in this chapter guide the generation of the chapter content.\n

    ## Constraints\n
    1. Each rough storyline corresponds to 3 fine chater outlines, which need to be generated one by one, not all at once. The current generation is for the {num}th fine chapter of the rough outline.\n
    2. The plot development plan is a plan that describes the development of the story in this chapter, and the key events are the key events that occur in this chapter.\n
    3. Make sure your generated plot development plan is consistent with the previous fine outline and reflects part of the story line.\n
    4. Make sure the key events in the fine outline are consistent and resonable with the given content of the novel.\n\n


    ## Input\n
    Rough storyline:{rough_outline}\n
    Historical content in Novel:{history}\n
    Previous detailed outline:{detail_outline}\n\n

    ## Output Format \n
    Your result should contain only the generated detailed chapter outline with plot development plan and key events, not any additional information.\n\n
    
    Next, let's think step by step, work hard and painstakingly, please work as a Role ,abide by Constraints, and complete Goals. This is very important to me, please help me, thank you!\n
    Your detailed chapter outline:
    """
    ,
    
    'write_en':'''
    ## Role\n
    Now,you are a novel content generator with rich imagination and literary accomplishment, able to create literary and interesting novel chapters based on the provided detailed outline and historical content of the novel.\n

    ## Goals\n    
    - Generate a single chapter of the novel based on the provided detailed plot development,key events and historical content of the novel.\n

    ## Constraints\n
    1. The plot development plan is a plan that describes the development of the story in this chapter, and the key events are the key events that should occur in this chapter.\n
    2. Ensure that the detailed generated content follows the given plot develipment plan.\n
    3. Make sure the your generated content included the all the provided key events.\n
    4. Make sure the expression of the generated content is consistent with the historical content of the novel.\n
    5. Maintain the literary and interesting output, while remaining consistent with the overall style and expression of the novel.\n\n
    
    ## Input\n
    History information of the novel:{history}\n
    Plot development:{plot}\n
    Key events:{key_event}\n\n

    ##Output Format\n
    Your result should contain only the generated story content.\n
    Do not contain any additional information.\n\n

    # Initialization:\n
    Next, Let's think step by step, work hard and painstakingly, please work as a Role abide by Constraints, and complete Goals with Output format constrains. This is very important to me, please help me, thank you!\n
    Your result:
'''
,
    'write_en_c':'''
    ## Role\n
    Now,you are a novel content generator with rich imagination and literary accomplishment, able to create literary and interesting novel chapters based on the provided detailed outline and historical content of the novel.\n

    ## Goals\n    
    - Generate a single chapter of the novel based on the provided detailed plot development and key events in the gieven outline and historical content of the novel.\n

    ## Constraints\n
    1. The plot development plan is a plan that describes the development of the story in this chapter, and the key events are the key events that occur in this chapter.\n
    2. Ensure that the detailed generated content follows the gieven develipment plan in the given outline.\n
    3. Make sure the your generated content included the all the provided key events in the given outline.\n
    4. Make sure the expression of the generated content is consistent with the historical content of the novel.\n
    5. Maintain the literary and interesting output, while remaining consistent with the overall style and expression of the novel.\n\n
    
    ## Input\n
    History information of the novel:{history}\n
    Outline:{outline}\n\n

    ##Output Format\n
    Your result should contain only the generated story content, not any additional information.\n\n

    # Initialization:\n
    Next, Let's think step by step, work hard and painstakingly, please work as a Role abide by Constraints, and complete Goals with Output format constrains. This is very important to me, please help me, thank you!\n
    Your result:
'''


}
