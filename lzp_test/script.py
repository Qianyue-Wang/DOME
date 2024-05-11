import re

# 假定的文本，可能包括一些无意义的空行或其他字符
text = """
- Story:

Diane found herself standing at a crossroads, the echoes of the confrontation still reverberating in her mind. She couldn't shake the image of Mark's face, the betrayal etched into every line. As the aftermath settled around them like a heavy fog, Diane retreated into the confines of her thoughts.

In the quiet solitude of her room, she grappled with the realization that her world had shifted irrevocably. The trust she once held so dear was fractured, splintered by the harsh truth she had been forced to confront. How could Mark have strayed into the arms of another, casting aside the bond they had painstakingly built?

Meanwhile, Mark buried himself in his work, seeking refuge in the monotonous hum of his daily routine. Each keystroke, each phone call was a distraction from the turmoil churning within him. He wrestled with guilt and confusion, the weight of Diane's accusation heavy on his conscience.

As days turned into nights, the silence between Diane and Mark grew palpable, a living entity that filled the spaces between them. Yet, beneath the surface, a flicker of hope remained. They tentatively reached out to each other, words unspoken but understood, as they embarked on the precarious path towards reconciliation.

Against the backdrop of the bustling inner city, their story unfolded, raw and unfiltered. Streets lined with neon lights mirrored the complexity of their emotions, adding depth to their journey through the aftermath. Each step forward was a step away from the darkness that threatened to engulf them.

And so, slowly but surely, Diane and Mark began to navigate the treacherous terrain of healing. Their scars ran deep, but in their shared pain, they found a fragile connection. As the tension eased and understanding bloomed, they stood at the precipice of a new chapter, hearts heavy with the weight of what had been lost and what still remained.
"""

# 正则表达式来提取相关信息
pattern = "Story:\s*\n(.*?)(?=\s*$)"

# 在文本中搜索匹配的部分
match = re.search(pattern, text, re.DOTALL)

if match:
    # 输出提取到的内容
    print(match.group(1))
else:
    print("No matching text found.")