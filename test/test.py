import re

text1 = '劳动素质教育◇23通信1,23通信2,23通信3,23通信4◇马晓丽◇2-204◇7-10,15-18☆形势与政策-1◇23通信3,23通信4◇贾超◇3-308◇11-14'
text2 = '职业通用英语1-1（分级）--版块1◇23人工智能1◇待版块分配◇7-18'

pattern = r'([^◇☆]+)◇([^◇☆]+)(?:◇([^◇☆]+))?(?:◇([^◇☆]+))?(?:◇([^◇☆]+))?(?:☆|$)'

matches1 = re.findall(pattern, text1)
matches2 = re.findall(pattern, text2)

print(matches1)
print(matches2)
