# 한국어 음절 빈도 http://nlp.kookmin.ac.kr/data/syl-2.txt
import streamlit as st
import itertools
from collections import Counter
from statistics import median
import pandas as pd 

class ANAGRAM():
    def __init__(self):
        
        self.onsets=["ㄱ","ㄲ","ㄴ","ㄷ","ㄸ","ㄹ","ㅁ","ㅂ","ㅃ","ㅅ","ㅆ","ㅇ","ㅈ","ㅉ","ㅊ","ㅋ","ㅌ","ㅍ","ㅎ"] # 19개
        self.nuclei=["ㅏ","ㅐ","ㅑ","ㅒ","ㅓ","ㅔ","ㅕ","ㅖ","ㅗ","ㅘ","ㅙ","ㅚ","ㅛ","ㅜ","ㅝ","ㅞ","ㅟ","ㅠ","ㅡ","ㅢ","ㅣ"] # 21개
        self.codas=["@","ㄱ","ㄲ","ㄳ","ㄴ","ㄵ","ㄶ","ㄷ","ㄹ","ㄺ","ㄻ","ㄼ","ㄽ","ㄾ","ㄿ","ㅀ","ㅁ","ㅂ","ㅄ","ㅅ","ㅆ","ㅇ","ㅈ","ㅊ","ㅋ","ㅌ","ㅍ","ㅎ"]  # 28개

        self.only_onsets = list((Counter(onsets) - Counter(codas)).elements())
        self.only_codas = list((Counter(codas) - Counter(onsets)).elements())   
        
        self.df = pd.read_csv('syl_freq.csv')
    
    
    def onset(self, char):
        code = ord(char)
        if 0xac00 <= code <= 0xd7b0:
            return (code - 0xac00) // 588
        return -1


    def nucleus(self, char):
        code = ord(char)
        if 0xac00 <= code <= 0xd7b0:
            x = (code - 0xac00) % 588
            return x // 28
        return -1


    def coda(self, char):
        code = ord(char)
        if 0xac00 <= code <= 0xd7b0:
            return (code - 0xac00) % 28
        return -1


    def compose(self, onset, nucleus, coda):
        return chr(0xac00 + onset * 588 + nucleus * 28 + coda)

    def decompose(self, string):
        con = []
        vow = []

        for s in string: # s는 한 음절 
            if s == ' ': # 띄어쓰기 무시 
                continue
            con.append(self.onsets[onset(s)])
            vow.append(self.nuclei[nucleus(s)])

            if coda(s) != 0: # 받침이 있으면
                con.append(self.codas[coda(s)])

        self.con = con
        self.vow = vow
        
    def syl_freq(self, string):
        scores = []
        for syl in string:
            if syl in self.df.syls.tolist():
                scores.append(int(df.query('syls==@syl').freqs.tolist()[0]))
                
        return median(scores)
        
    
    def anagram_candidate(self, string):
        self.decompose(string)
        
        word_set = set()

        # 모든 음절에 받침 없음
        if len(self.con) == len(self.vow):
            permuted_c = list(itertools.permutations(self.con))
            permuted_v = list(itertools.permutations(self.vow))

            for pc in permuted_c:
                for pv in permuted_v:
                    word = ''
                    for c,v in zip(pc, pv):
                        syl = self.compose(self.onsets.index(c),self.nuclei.index(v),0)
                        word += syl
                    word_set.add(word)


        else: 
            diff = 2*len(self.vow) - len(self.con)

            candidates = []
            candidate_onsets = list(map(list, itertools.combinations(self.con, len(self.vow))))

            for onset in candidate_onsets:
                candidates.append((onset, list((Counter(self.con) - Counter(onset)).elements())+ ['@']*diff))

            permuted_n = list(map(list, itertools.permutations(self.vow)))

            for candidate in candidates:
                onset, coda = candidate 

                # 종성으로만 쓸 수 있는 자음이 초성 리스트에 포함된 경우 
                if any(o in self.only_codas for o in onset):
                    continue
                # 초성으로만 쓸 수 있는 자음이 종성 리스트에 포함된 경우 
                if any(c in self.only_onsets for c in coda):
                    continue

                permuted_o = list(map(list, itertools.permutations(onset)))
                permuted_c = list(map(list, itertools.permutations(coda)))

                for po in permuted_o:
                    for pn in permuted_n:
                        for pc in permuted_c:
                            word = ''
                            for o,n,c in zip(po, pn, pc):
                                syl = self.compose(self.onsets.index(o), self.nuclei.index(n), self.codas.index(c))
                                word += syl
                            word_set.add(word)

        return sorted(list(word_set), key = syl_freq, reverse=True)

#EMOJI_URL = "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/microsoft/209/multiple-musical-notes_1f3b6.png"
 
# Set page title and favicon.
st.set_page_config(
    page_title="애너그램 추리반", page_icon=🕵️‍♀️,
)

# Display header.
st.markdown("<br>", unsafe_allow_html=True)
#st.image(EMOJI_URL, width=80)

# set icon and link 
"""
# 애너그램 풀기 + 만들기 
[![github](https://github.com/yeounyi/AnagramApp/blob/main/img/github.png?raw=true)](https://github.com/yeounyi/AnagramApp)
&nbsp[![linked](https://github.com/yeounyi/AnagramApp/blob/main/img/linkedin.png?raw=true)](https://in.linkedin.com/in/yeoun-yi-989360166/)


"""
st.markdown("<br>", unsafe_allow_html=True)

"""
애너그램 문제 혹은 답을 입력하세요. 해당 자모음으로 생성할 수 있는 모든 단어들을 음절의 빈도수대로 정렬하여 보여줍니다.
* 예시 
- 후살맘 -> [하삼물, 물삼하, ..., 사물함, ...]
- 헐생징 -> [햇정일, 일햇정, ..., 행정실, ...]
"""

st.markdown("<span style='color:white'>래해새자장</span>", unsafe_allow_html=True)

user_input = st.text_input("애너그램 문제 혹은 답을 입력하세요: ")

with st.spinner('🤯 컴퓨터가 고민하고 있어요...같이 고민해봐요..'):
    a = ANAGRAM()
    a.anagram_candidate(user_input)
