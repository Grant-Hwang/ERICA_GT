from   __future__ import division, print_function
from   itertools  import permutations, combinations, product, \
                         chain
from   pprint     import pprint as pp
from   fractions  import Fraction as F
import random, ast, re
import sys
 
if sys.version_info[0] < 3:
    input = raw_input
    from itertools import izip_longest as zip_longest
else:
    from itertools import zip_longest
 
 
def choose4():
    return [str(random.randint(1,9)) for i in range(4)]
 
def ask4():
    digits = ''
    while len(digits) != 4 or not all(d in '123456789' for d in digits):
        digits = input('Enter the digits to solve for: ')
        digits = ''.join(digits.strip().split())
    return list(digits)
 
def welcome(digits):
    print (__doc__)
    print ("Your four digits: " + ' '.join(digits))
 
def check(answer, digits):
    allowed = set('() +-*/\t'+''.join(digits))
    ok = all(ch in allowed for ch in answer) and \
         all(digits.count(dig) == answer.count(dig) for dig in set(digits)) \
         and not re.search('\d\d', answer)
    if ok:
        try:
            ast.parse(answer)
        except:
            ok = False
    return ok
 
def solve(digits):
    digilen = len(digits)
    exprlen = 2 * digilen - 1
    digiperm = sorted(set(permutations(digits)))
    opcomb   = list(product('+-*/', repeat=digilen-1))
    brackets = ( [()] + [(x,y)
                         for x in range(0, exprlen, 2)
                         for y in range(x+4, exprlen+2, 2)
                         if (x,y) != (0,exprlen+1)]
                 + [(0, 3+1, 4+2, 7+3)] )
    for d in digiperm:
        for ops in opcomb:
            if '/' in ops:
                d2 = [('F(%s)' % i) for i in d]
            else:
                d2 = d
            ex = list(chain.from_iterable(zip_longest(d2, ops, fillvalue='')))
            for b in brackets:
                exp = ex[::]
                for insertpoint, bracket in zip(b, '()'*(len(b)//2)):
                    exp.insert(insertpoint, bracket)
                txt = ''.join(exp)
                try:
                    num = eval(txt)
                except ZeroDivisionError:
                    continue
                if num == 24:
                    if '/' in ops:
                        exp = [ (term if not term.startswith('F(') else term[2])
                               for term in exp ]
                    ans = ' '.join(exp).rstrip()
                    print ("Solution found:",ans)
                    return ans
    print ("No solution found for:", ' '.join(digits))            
    return '!'
 
def main():    
    digits = choose4()
    welcome(digits)
    trial = 0
    out = 0
    answer = ''
    chk = ans = False
    while (True):
        trial +=1
        answer = input("Expression %i: " % trial)
        chk = check(answer, digits)
        if trial == 3:
            answer = '?'
            if out > 2:
                print("3 outs. You lost!")
                break
        if answer == '?':
            solve(digits)
            answer = '!'
            out+=1
            if out > 2:
                print("3 outs. You lost!")
                break
        if answer.lower() == 'q':
            break
        if answer == '!':
            digits = choose4()
            trial = 0
            print ("\nNew digits:", ' '.join(digits))
            continue
        if answer == '!!':
            digits = ask4()
            trial = 0
            print ("\nNew digits:", ' '.join(digits))
            continue
        if not chk:
            print ("Wrong answer: '%s'. Try again!" % answer)
        else:
            if '/' in answer:
                answer = ''.join( (('F(%s)' % char) if char in '123456789' else char)
                                  for char in answer )
            ans = eval(answer)
            print (" = ", ans)
            if ans == 24:
                print ("Thats right!")
    print ("Thank you and goodbye")   
 
main()
