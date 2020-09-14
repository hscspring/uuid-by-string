from uuid_by_string import generate_uuid
from uuid_by_string.uuid_by_string import (
    int32_to_int8,
    uint8_to_hex, uint8array_to_hex,
    string_to_char_buffer,
    md5_hash, sha1_hash,
    hash_to_uuid)


def test_pass():
    assert generate_uuid("")


def test_uuid():
    assert generate_uuid("abc") != generate_uuid("acb")


def test_uuid_string():
    assert generate_uuid("a string. 随意的，可以有表情😁")


def test_default_namespace():
    assert generate_uuid("爱", None) == generate_uuid("爱")


def test_default_namespace_is_number():
    assert generate_uuid("abc", 5) == generate_uuid("abc")


def test_namespace():
    assert generate_uuid("爱", "namespace")


def test_version():
    assert generate_uuid("a", version=3) != generate_uuid("a", version=5)


def test_default_version():
    assert generate_uuid("a", version=5) == generate_uuid("a")


def test_target_type_error():
    try:
        generate_uuid(123)
    except Exception as err:
        assert "string" in str(err)

    try:
        generate_uuid(123.0)
    except Exception as err:
        assert "string" in str(err)


def test_version_error():
    try:
        generate_uuid("", 4)
    except Exception as err:
        assert "3 or 5" in str(err)

    try:
        generate_uuid("", "xx")
    except Exception as err:
        assert "3 or 5" in str(err)


def test_int32_to_int8():
    assert int32_to_int8(256) == 0
    assert int32_to_int8(257) == 1


def test_uint8_to_hex():
    assert uint8_to_hex(10) == "0a"
    assert uint8_to_hex(255) == "ff"


def test_uint8array_to_hex():
    assert uint8array_to_hex([1, 10, 255]) == "010aff"


def test_string_to_buffer():
    assert string_to_char_buffer("a我") == [97, 17]


def test_md5_hash():
    assert md5_hash(string_to_char_buffer("a我")) == [
        116, 128, 61, 107, 74, 30, 23, 160,
        65, 29, 29, 186, 209, 226, 137, 234
    ]


def test_sha1_hash():
    assert sha1_hash(string_to_char_buffer("a我")) == [
        51, 151, 138, 184, 122, 42, 178, 7,
        209, 160, 249, 7, 133, 222, 100, 184
    ]


def test_hash_to_uuid_v3():
    assert hash_to_uuid(md5_hash(string_to_char_buffer("a我")), 3
                        ) == '74803d6b-4a1e-37a0-811d-1dbad1e289ea'


def test_hash_to_uuid_v5():
    assert hash_to_uuid(sha1_hash(string_to_char_buffer("a我")), 5
                        ) == '33978ab8-7a2a-5207-91a0-f90785de64b8'
