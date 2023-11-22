def unique_couple_name(father, mother, people, couple_names):
    assert father in people, f"Expected father {father} to be in people"
    assert mother in people, f"Expected mother {mother} to be in people"
    cnt = 0
    while True:
        couple_name = father + "_" + mother + str(cnt)
        if couple_name in people or couple_name in couple_names:
            cnt += 1
        else:
            break
    return couple_name


def parse_line(ln):
    child, child_gender, father, mother = [k.strip() for k in ln.split(",")]
    child_gender = int(child_gender)
    return child, child_gender, father, mother


def gen_digraph(defn_str):
    defn_str = defn_str.strip().strip(";")
    digraph_str = """# just graph set-up
digraph family_tree {
ratio = "auto"
mincross = 2.0"""
    reln = {}
    people_names = set()
    couple_names = set()
    inferred_gender = {}  # for type checking
    parents_defined = {}
    for ln in defn_str.split(";"):
        child, child_gender, father, mother = parse_line(ln)
        assert (
            child == "0" or child not in parents_defined
        ), f"Redefining parents for {child} in {ln}, who was already defined in {parents_defined[child]}"
        if child != "0":
            parents_defined[child] = ln
        if father not in inferred_gender:
            inferred_gender[father] = (0, ln)
        if mother not in inferred_gender:
            inferred_gender[mother] = (1, ln)
        if child not in inferred_gender:
            inferred_gender[child] = (child_gender, ln)
        x, y = inferred_gender[mother]
        assert (
            x == 1
        ), f"{mother} expected to be female(1) in {ln}, but that contradicts previous line {y}"
        x, y = inferred_gender[father]
        assert (
            x == 0
        ), f"{father} expected to be male(0) in {ln}, but that contradicts previous line {y}"
        x, y = inferred_gender[child]
        assert (
            x == child_gender
        ), f'{child} expected to be {("male","female")[inferred_gender[child]]}({inferred_gender[child]}) in {ln}, but that contradicts previous line {y}'
        reln[(father, mother)] = reln.get((father, mother), []) + [
            (child, child_gender)
        ]
        people_names.update([child, father, mother])
    people_nodes_drawn = set()
    edges_drawn = set()
    for couple in reln:
        father, mother = couple
        couple_name = unique_couple_name(father, mother, people_names, couple_names)
        couple_names.update([couple_name])
        digraph_str += f'"{couple_name}" [shape=diamond,style=filled,label="",height=.1,width=.1] ;\n'
        children = reln[couple]
        for child, child_gender in children:
            if father not in people_nodes_drawn:
                digraph_str += f'"{father}"   [shape=box, regular=1, color="blue"] ;\n'
                people_nodes_drawn.update([father])
            if mother not in people_nodes_drawn:
                digraph_str += f'"{mother}"   [shape=box, regular=1, color="pink"] ;\n'
                people_nodes_drawn.update([mother])
            if child not in people_nodes_drawn and child != "0":
                child_col = ("blue", "pink")[child_gender]
                digraph_str += (
                    f'"{child}"     [shape=box, regular=1, color="{child_col}"] ;\n'
                )
                people_nodes_drawn.update([child])
            if (father, couple_name) not in edges_drawn:
                digraph_str += (
                    f'"{father}"      -> "{couple_name}" [dir=none, weight=1] ;\n'
                )
                edges_drawn.update([(father, couple_name)])
            if (mother, couple_name) not in edges_drawn:
                digraph_str += (
                    f'"{mother}"      -> "{couple_name}" [dir=none, weight=1] ;\n'
                )
                edges_drawn.update([(mother, couple_name)])
            if child != "0":
                digraph_str += f'"{couple_name}" -> "{child}"        [weight=2] ;\n'

    digraph_str += "\n}"
    return digraph_str

if __name__ == '__main__':
    import sys
    print(gen_digraph(sys.argv[1]))