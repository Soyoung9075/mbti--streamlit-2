# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
import pandas as pd
import numpy as np
import requests
from io import BytesIO
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="MBTI 궁합",
        page_icon="💑",
    )

    st.write("# MBTI별 궁합 알아보기 💑")

    url = "https://github.com/Soyoung9075/mbti--streamlit/raw/main/MBTI_MATCHING.xlsx"
    response = requests.get(url)
    response.raise_for_status()

    data = pd.read_excel(BytesIO(response.content), index_col= 0, sheet_name= "Sheet1")
    mbti_compatibility = data.to_dict()
  
    coworkers = {
    'ISTP': ['정진용'],
    'ESTP': ['주하나', '이수지'],
    'ESFJ': ['임정훈', '김익형', '임욱빈', '박소연A'],
    'ISTJ': ['김충만', '이소영', '조완영', '이준희', '노왕현'],
    'ESTJ': ['이대의', '이강욱', '최인', '김채원'],
    'ENFP': ['박경원', '박소연B'],
    'INFJ': ['김소미', '이세원', '한소영'],
    'ENFJ': ['김윤현', '김진호', '박희정', '권성애', '이태민'],
    'INTJ': ['조성현'],
    'INTP': ['김준희'],
    'ENTP': ['전주은', '남지호'],
    'INFP': ['김윤석'],
    'ISFP': ['장성환']
    }

    # User selects their MBTI type
    user_mbti = st.selectbox('Select your MBTI type:', sorted(mbti_compatibility.keys()))

    def display_compatibility(compat_level):
      displayed = False
      filtered_types = {k: v for k, v in mbti_compatibility[user_mbti].items() if v == compat_level}
      if filtered_types:
          for type, compat in filtered_types.items():
              names = ', '.join(coworkers.get(type, []))
              container.write(f'{type} : {names}')
      else:
          if not displayed:
              container.write("없어용!😥")
              displayed = True
    
    if st.button('궁합 보기'):

      container = st.container(border = True)
  
      container.subheader("천생연분💗")
      display_compatibility('천생연분')
    
      container.subheader("쿵짝짝💚")
      display_compatibility('쿵짝짝')

      container.subheader("무난💛")
      display_compatibility('무난')

      container.subheader("개선가능💡")
      display_compatibility('개선가능')

      container.subheader("최악💣")
      display_compatibility('최악')

if __name__ == "__main__":
    run()

