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
    'chapter_outline':"""
    You are an expert in novel creation.
    Novel creation is a step-by-step process. And one volume contain two chapters.
    In order to complete the chapter outline of the current volume, \n
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
