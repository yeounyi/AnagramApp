import streamlit as st
import itertools
from collections import Counter
from statistics import median
import pandas as pd 

# Set page title and favicon.
st.set_page_config(
    page_title="애너그램 추리반",
)

# Display header.
st.markdown("<br>", unsafe_allow_html=True)
#st.image(EMOJI_URL, width=80)


df = pd.read_csv('syl_freq.csv')


def onset(char):
    code = ord(char)
    if 0xac00 <= code <= 0xd7b0:
        return (code - 0xac00) // 588
    return -1


def nucleus(char):
    code = ord(char)
    if 0xac00 <= code <= 0xd7b0:
        x = (code - 0xac00) % 588
        return x // 28
    return -1


def coda(char):
    code = ord(char)
    if 0xac00 <= code <= 0xd7b0:
        return (code - 0xac00) % 28
    return -1


def compose(onset, nucleus, coda):
    return chr(0xac00 + onset * 588 + nucleus * 28 + coda)

onsets=["ㄱ","ㄲ","ㄴ","ㄷ","ㄸ","ㄹ","ㅁ","ㅂ","ㅃ","ㅅ","ㅆ","ㅇ","ㅈ","ㅉ","ㅊ","ㅋ","ㅌ","ㅍ","ㅎ"] # 19개
nuclei=["ㅏ","ㅐ","ㅑ","ㅒ","ㅓ","ㅔ","ㅕ","ㅖ","ㅗ","ㅘ","ㅙ","ㅚ","ㅛ","ㅜ","ㅝ","ㅞ","ㅟ","ㅠ","ㅡ","ㅢ","ㅣ"] # 21개
codas=["@","ㄱ","ㄲ","ㄳ","ㄴ","ㄵ","ㄶ","ㄷ","ㄹ","ㄺ","ㄻ","ㄼ","ㄽ","ㄾ","ㄿ","ㅀ","ㅁ","ㅂ","ㅄ","ㅅ","ㅆ","ㅇ","ㅈ","ㅊ","ㅋ","ㅌ","ㅍ","ㅎ"]  # 28개

only_onsets = list((Counter(onsets) - Counter(codas)).elements())
only_codas = list((Counter(codas) - Counter(onsets)).elements())

def decompose(string):
    con = []
    vow = []
    
    for s in string: # s는 한 음절 
        if s == ' ': # 
            continue
        con.append(onsets[onset(s)])
        vow.append(nuclei[nucleus(s)])
        
        if coda(s) != 0: # 받침이 있으면
            con.append(codas[coda(s)])
    
    return (con, vow)

# 한국어 음절 빈도 http://nlp.kookmin.ac.kr/data/syl-2.txt
def syl_freq(string):
    score = 0
    for syl in string:
        if syl in df.syls.tolist():
            score += int(df.query('syls==@syl').freqs.tolist()[0])
    return score

def anagram_candidate(con, vow):
    only_onsets = list((Counter(onsets) - Counter(codas)).elements())
    only_codas = list((Counter(codas) - Counter(onsets)).elements())
    word_set = set()
    
    # 모든 음절에 받침 없음
    if len(con) == len(vow):
        permuted_c = list(itertools.permutations(con))
        permuted_v = list(itertools.permutations(vow))
        
        for pc in permuted_c:
            for pv in permuted_v:
                word = ''
                for c,v in zip(pc, pv):
                    syl = compose(onsets.index(c), nuclei.index(v),0)
                    word += syl
                word_set.add(word)
    

    else: 
        diff = 2*len(vow) - len(con)
        
        candidates = []
        candidate_onsets = list(map(list, itertools.combinations(con, len(vow))))
        
        for onset in candidate_onsets:
            candidates.append((onset, list((Counter(con) - Counter(onset)).elements())+ ['@']*diff))
            
        permuted_n = list(map(list, itertools.permutations(vow)))
        
        for candidate in candidates:
            onset, coda = candidate 
            
            # 종성으로만 쓸 수 있는 자음이 초성 리스트에 포함된 경우 
            if any(o in only_codas for o in onset):
                continue
            # 초성으로만 쓸 수 있는 자음이 종성 리스트에 포함된 경우 
            if any(c in only_onsets for c in coda):
                continue

            permuted_o = list(map(list, itertools.permutations(onset)))
            permuted_c = list(map(list, itertools.permutations(coda)))

            for po in permuted_o:
                for pn in permuted_n:
                    for pc in permuted_c:
                        word = ''
                        for o,n,c in zip(po, pn, pc):
                            syl = compose(onsets.index(o), nuclei.index(n), codas.index(c))
                            word += syl
                        word_set.add(word)
                        
    def syl_freq(string):
        score = 0
        for syl in string:
            if syl in df.syls.tolist():
                score += int(df.query('syls==@syl').freqs.tolist()[0])
        return score                    
    
    return sorted(list(word_set), key = syl_freq, reverse=True)



# set icon and link 
"""
# 애너그램 추리반 🕵️‍♀️
[![github](https://github.com/yeounyi/AnagramApp/blob/main/img/github.png?raw=true)](https://github.com/yeounyi/AnagramApp)
&nbsp[![linked](https://github.com/yeounyi/AnagramApp/blob/main/img/linkedin.png?raw=true)](https://in.linkedin.com/in/yeoun-yi-989360166/)


"""
st.markdown("<br>", unsafe_allow_html=True)

"""
애너그램 문제 혹은 답을 입력하세요. 
주어진 단어의 자모음을 해체한 후, 모든 가능한 조합을 구합니다. 이후 한국어 음절 빈도에 따라 정렬합니다.
* 예시 
    - 후살맘 → ```[하삼물, 물삼하, ..., 사물함, ...]```
    - 헐생징 → ```[햇정일, 일햇정, ..., 행정실, ...]```
"""

st.markdown("<span style='color:white'>래해새자장</span>", unsafe_allow_html=True)

user_input = st.text_input("애너그램 문제 혹은 답을 입력하세요: ")

if len(user_input) == 1:
    st.error('한 글자는 의미가 없어요!')

for syl in user_input:
    if not ord('가') <= ord(syl) <= ord('힣'):
        st.error('한글만 입력해주세요!')

with st.spinner('🤯 컴퓨터가 고민하고 있어요...같이 고민해봐요..'):
    
    con, vow = decompose(user_input)
    st.write(anagram_candidate(con, vow))

