import pytest
from modules.parsing.filename_parser import parse_filename

# 정상 케이스 테스트
def test_parse_valid_filename_with_two_digit_number():
    filename = "중학수학1-상_01_12_B03.png"
    result = parse_filename(filename)
    assert result == {
        "book": "중학수학1-상",
        "chapter": "01",
        "page": "12",
        "type": "B",
        "number": "03"
    }

def test_parse_valid_filename_with_single_digit_type_and_number():
    filename = "중학수학2-하_03_24_Z7.png"
    result = parse_filename(filename)
    assert result == {
        "book": "중학수학2-하",
        "chapter": "03",
        "page": "24",
        "type": "Z",
        "number": "7"
    }

# 실패 케이스 테스트
def test_parse_filename_with_missing_underscore():
    filename = "중학수학1-상_01_12B03.png"
    result = parse_filename(filename)
    assert result == {}

def test_parse_filename_with_invalid_type_number():
    filename = "중학수학1-상_01_12_03.png"  # 문자 없는 type_number
    result = parse_filename(filename)
    assert result == {}

def test_parse_filename_with_extra_parts():
    filename = "중학수학1-상_01_12_B03_extra.png"
    result = parse_filename(filename)
    assert result == {}

def test_parse_filename_with_too_few_parts():
    filename = "중학수학1-상_01_B03.png"
    result = parse_filename(filename)
    assert result == {}

# 경계 테스트
def test_parse_filename_with_no_extension():
    filename = "중학수학1-상_01_12_B03"
    result = parse_filename(filename)
    assert result == {
        "book": "중학수학1-상",
        "chapter": "01",
        "page": "12",
        "type": "B",
        "number": "03"
    }
