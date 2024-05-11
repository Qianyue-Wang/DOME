prompt_template_name={'storyline','completion_plan','storyline_struct_cn'}
PROMPT_TEMPLATE_WRITE={
    'generate_setting':'''
    
    '''
    ,
    'rouge_storyline':"""
    ## Promise:
    {promise}
    """
    
    ,

    
    'chapter_outline':"""
    You are an expert in novel creation.
    Novel creation is a step-by-step process. And one volume contain two chapters.
    In order to complete the chapter outline of the current vloume, \n
    we need to comprehensively consider: 
    the overall summary of the novel, 
    the current volume outline, 
    the full content of the previous chapters,
    and the history of the full story.\n
    ## Hint
    1. The chapter outline should be concise and clear, only describe how the story unfolds rather than the complete story content.\n
    2. You have to generate two chapter outlines at once, which must have a developmental relationship and not be duplicated, giving full consideration to the given volume outline.\n
    ## Input
    the overall summary of the novel:{premise},\n
    the current volume outline:{volume_outline},\n
    the full content of the previous chapters:{last_chapter},\n
    and the history of the full story:{history}\n
    ## Output Format \n
    Please follow the output format strictly to ensure the consistency of the generated detailed chapter outline.\n
    Following the format below:\n
    - Chapter Outline 1: \n
    - Chapter Outline 2: \n
    """
    ,
    'write_en':'''
    You are an expert in novel creation.
    Novel creation is a step-by-step process. 
    In order to complete the story of the current chapter, 
    we need to comprehensively consider: 
    the overall summary of the novel, 
    the current volume outline, 
    the current chapter outline,
    the full content of the previous chapters,
    and the history of the full story.\n
    ## Hint
    1. Your story should add more details, including language description, psychological description, and environmental description.\n
    2. The content of the story should be consistent with the outline and logically coherent with the historical content.\n
    ## Input
    the overall summary of the novel:{premise},
    the current volume outline:{volume_outline},
    the current chapter outline:{chapter_outline},
    the full content of the previous chapters:{last_chapter},
    and the history of the full story:{history}\n
    ## Output Format \n
    Please follow the output format strictly to ensure the consistency of the generated detailed chapter outline.\n
    Following the format below:\n
    - Story: \n
    '''

}
