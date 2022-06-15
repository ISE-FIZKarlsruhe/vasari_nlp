import re
regex = "(anno\sM{0,4}(CM|CD|D?C){0,3}(XC|XL|L?X{0,3})(IX|IV|V?I{0,4}))(\s|$)"

txt = "lorem ipsum"
matches = re.findall(regex, txt, re.IGNORECASE)
if len(matches)>0:
    print(matches[0], "\n", txt)