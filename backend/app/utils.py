def get_korean_initial(word: str) -> str:
    """한글 단어에서 초성만 추출하는 함수"""
    CHOSUNG_LIST = [
        "ㄱ", "ㄲ", "ㄴ", "ㄷ", "ㄸ", "ㄹ", "ㅁ", "ㅂ", "ㅃ", "ㅅ", "ㅆ",
        "ㅇ", "ㅈ", "ㅉ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"
    ]
    BASE_CODE, CHOSUNG, JONGSUNG = 44032, 588, 28

    if word and "가" <= word[0] <= "힣":  # 한글이면 초성 추출
        char_code = ord(word[0]) - BASE_CODE
        chosung_index = char_code // CHOSUNG
        return CHOSUNG_LIST[chosung_index]
    
    return word[0]  # 한글이 아니면 첫 글자 그대로 반환