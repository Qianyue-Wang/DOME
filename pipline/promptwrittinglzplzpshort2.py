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
    the current volume outline:{volume_outline},\n
    the full content of the previous chapters:{last_chapter},\n
    and the history of the full story:{history}\n
    ## Output Format \n
    Please follow the output format strictly to ensure the consistency of the generated detailed chapter outline.\n
    Nothing but only the chapter outline should be included in the output.\n
    There are two chapter outlines in total. Following the format below:\n
    - Chapter Outline 1: \n
    - Chapter Outline 2: \n
    Your result:
    """
    ,
    'write_en':'''
    Your task is to write a story based on the given inputed information\n
    Your story should have more details, including language description, psychological description, and environmental description.\n
    The content of the story should be consistent with the outline and logically coherent with the historical content like the last chapter content and the relevant history content.\n
    ## Input\n
    the current volume outline:{volume_outline},\n
    the current chapter outline:{chapter_outline},\n
    the full content of the previous chapters:{last_chapter},\n
    and the history of the full story:{history}\n\n
    
    ## Output Format \n
    Nothing but only the generated content ,which is composed by a series of sentences, should be included in the output.\n
    Strictly follow the format below:\n
    - Story: \n
    Your generated content:
    '''

}
