import pytest

from family_tree import gen_digraph, unique_couple_name, parse_line


@pytest.mark.parametrize(
    "test_input,expected",
    [("A,0,B,C", ("A", 0, "B", "C")), ("0,0,B,C", ("0", 0, "B", "C"))],
)
def test_parse_line_pass(test_input, expected):
    assert parse_line(test_input) == expected


@pytest.mark.parametrize(
    "invalid_string, excp",
    [
        ("3+5", "not enough values to unpack (expected 4, got 1)"),
        ("A,B,C,D", "invalid literal for int() with base 10: 'B'"),
        ("A,B,C", "not enough values to unpack (expected 4, got 3)"),
    ],
)
def test_parse_line_fail(invalid_string, excp):
    with pytest.raises(Exception) as e_info:
        parse_line(invalid_string)
    assert excp in str(e_info)


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (("A", "B", set(["A", "B"]), set()), "A_B0"),
        (("A", "B", set(["A", "B"]), set(["A_B0", "A_B1"])), "A_B2"),
    ],
)
def test_unique_couple_name_pass(test_input, expected):
    assert unique_couple_name(*test_input) == expected


@pytest.mark.parametrize(
    "test_input, excp",
    [
        (("A", "B", set([]), set()), "Expected father A to be in people"),
        (
            ("A", "B", set(["X", "Y", "A"]), set(["A_B0"])),
            "Expected mother B to be in people",
        ),
    ],
)
def test_unique_couple_name_fail(test_input, excp):
    with pytest.raises(Exception) as e_info:
        unique_couple_name(*test_input)
    assert excp in str(e_info)


@pytest.mark.parametrize(
    "invalid_string, excp",
    [
        (
            "A,0,B,C; P,0,B,C; D,1,B,C; RR,1,D,RRR; B,1,X,Y; 0,0,A,M;",
            "D expected to be male(0) in  RR,1,D,RRR, but that contradicts previous line  D,1,B,C",
        ),
        (
            "A,0,B,C; P,0,B,C; D,1,B,C; RR,1,D,RRR; 0,0,A,M;",
            "D expected to be male(0) in  RR,1,D,RRR, but that contradicts previous line  D,1,B,C",
        ),
        (
            "A,0,B,C; P,0,B,C; D,1,B,C; RR,1,RRR,D; B,0,X,Y; 0,0,A,M; A,0,MM,NN;",
            "Redefining parents for A in  A,0,MM,NN, who was already defined in A,0,B,C",
        ),
    ],
)
def test_gen_digraph_fail(invalid_string, excp):
    with pytest.raises(Exception) as e_info:
        gen_digraph(invalid_string)
    assert excp in str(e_info)


gr1 = """# just graph set-up
digraph family_tree {
ratio = "auto"
mincross = 2.0"B_C0" [shape=diamond,style=filled,label="",height=.1,width=.1] ;
"B"   [shape=box, regular=1, color="blue"] ;
"C"   [shape=box, regular=1, color="pink"] ;
"A"     [shape=box, regular=1, color="blue"] ;
"B"      -> "B_C0" [dir=none, weight=1] ;
"C"      -> "B_C0" [dir=none, weight=1] ;
"B_C0" -> "A"        [weight=2] ;
"P"     [shape=box, regular=1, color="blue"] ;
"B_C0" -> "P"        [weight=2] ;
"D"     [shape=box, regular=1, color="pink"] ;
"B_C0" -> "D"        [weight=2] ;
"RRR_D0" [shape=diamond,style=filled,label="",height=.1,width=.1] ;
"RRR"   [shape=box, regular=1, color="blue"] ;
"RR"     [shape=box, regular=1, color="pink"] ;
"RRR"      -> "RRR_D0" [dir=none, weight=1] ;
"D"      -> "RRR_D0" [dir=none, weight=1] ;
"RRR_D0" -> "RR"        [weight=2] ;
"X_Y0" [shape=diamond,style=filled,label="",height=.1,width=.1] ;
"X"   [shape=box, regular=1, color="blue"] ;
"Y"   [shape=box, regular=1, color="pink"] ;
"X"      -> "X_Y0" [dir=none, weight=1] ;
"Y"      -> "X_Y0" [dir=none, weight=1] ;
"X_Y0" -> "B"        [weight=2] ;
"A_M0" [shape=diamond,style=filled,label="",height=.1,width=.1] ;
"M"   [shape=box, regular=1, color="pink"] ;
"A"      -> "A_M0" [dir=none, weight=1] ;
"M"      -> "A_M0" [dir=none, weight=1] ;

}"""


@pytest.mark.parametrize(
    "test_input,expected",
    [("A,0,B,C; P,0,B,C; D,1,B,C; RR,1,RRR,D; B,0,X,Y; 0,0,A,M", gr1)],
)
def test_gen_digraph_pass(test_input, expected):
    # import pdb; pdb.set_trace()
    assert gen_digraph(test_input) == expected
