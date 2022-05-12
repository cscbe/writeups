flag = "csc{But_What_Is_The_Ultimate_Question_1c7b9f803e8664351980b277d289c7d8}"
solution = "Puppies! And Pizza."

method = """
public void m{} () {{

    this.vault[{}] = {};
}}
"""

method2 = """
public void k{} () {{

    this.sol[{}] = {};
}}
"""

cl = """
package be.dauntless.theultimatequestion;

public class Vault
{{
    byte[] vault = new byte[71];
    byte[] sol = new byte[19];

    public String checkAnswer(String answer){{
        if(answer.equals(new String(this.sol))){{
            return new String(this.vault);
        }}
        return "No, that's not right...";

    }}
    public Vault()
    {{
        {}
    }} 

    {}
}}
"""
methods = ""
calls = ""
for i in range(0, 71):
    m = method.format(i, i, ord(flag[i]))
    methods += m
    calls +="this.m{}();\n".format(i)

for i in range(0, 19):
    m = method2.format(i, i, ord(solution[i]))
    methods += m
    calls +="this.k{}();\n".format(i)

print(cl.format(calls, methods))