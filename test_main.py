import main

def test_tree_simple(tmp_path, tmpdir, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('F :- f.')
    monkeypatch.chdir(tmp_path)
    main.main(['a.txt'])
    assert open('a.txt.out', 'r').read() == 'REL (ID F) (ID f)\n'

def test_tree_atom_scopes(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('F (cons H) p:- f.')
    monkeypatch.chdir(tmp_path)
    main.main(['a.txt'])
    assert open('a.txt.out', 'r').read() == "REL (ATOM (ID F) (ATOMSEQ (ATOMSEQ (ATOM (ID cons) (ATOMSEQ (ID H)))) (ATOMSEQ (ID p)))) (ID f)\n"

def test_tree_atom_concat(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('F g t:- f.')
    monkeypatch.chdir(tmp_path)
    main.main(['a.txt'])
    assert open('a.txt.out', 'r').read() == 'REL (ATOM (ID F) (ATOMSEQ (ATOM (ID g) (ATOMSEQ (ID t))))) (ID f)\n'

def test_tree_expr_simple(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('F :- t , j ; l.')
    monkeypatch.chdir(tmp_path)
    main.main(['a.txt'])
    assert open('a.txt.out', 'r').read() == 'REL (ID F) (DISJ (CONJ (ID t ID j) ID l))\n'

def test_tree_expr_scopes(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('F :- t , ((j ; l) , r).')
    monkeypatch.chdir(tmp_path)
    main.main(['a.txt'])
    assert open('a.txt.out', 'r').read() == 'REL (ID F) (CONJ (ID t (CONJ ((DISJ (ID j ID l)) ID r))))\n'

def test_tree_three_simple_lines(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('F :- t.\n G (p g).\n K :- t;l.')
    monkeypatch.chdir(tmp_path)
    main.main(['a.txt'])
    tree1 = "REL (ID F) (ID t)\n"
    tree2 = "REL (ATOM (ID G) (ATOMSEQ (ATOMSEQ (ATOM (ID p) (ATOMSEQ (ID g))))))\n"
    tree3 = "REL (ID K) (DISJ (ID t ID l))\n"
    assert open('a.txt.out', 'r').read() == tree1 + tree2 + tree3

def test_tree_three_lines_with_scopes(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('fr (b) :- f.\nreg (((b))) :- r.\nre ((a) b) :- e.\n')
    monkeypatch.chdir(tmp_path)
    main.main(['a.txt'])
    tree1 = "REL (ATOM (ID fr) (ATOMSEQ (ATOMSEQ (ID b)))) (ID f)\n"
    tree2 = "REL (ATOM (ID reg) (ATOMSEQ (ATOMSEQ (ATOMSEQ (ATOMSEQ (ID b)))))) (ID r)\n"
    tree3 = "REL (ATOM (ID re) (ATOMSEQ (ATOMSEQ (ATOMSEQ (ID a)) (ATOMSEQ (ID b))))) (ID e)\n"
    assert open('a.txt.out', 'r').read() == tree1 + tree2 + tree3

def test_incorrect_without_dot(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('f.\n f')
    monkeypatch.chdir(tmp_path)
    main.main(['a.txt'])
    assert open('a.txt.out', 'r').read() == 'Syntax error: line 2, colon EOF\n'

def test_incorrect_without_dot_with_scope(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('f :- (w)\nf.')
    monkeypatch.chdir(tmp_path)
    main.main(['a.txt'])
    assert open('a.txt.out', 'r').read() == 'Syntax error: line 2, colon 0\n'

def test_incorrect_without_dot_one_line(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('f :- (w)')
    monkeypatch.chdir(tmp_path)
    main.main(['a.txt'])
    assert open('a.txt.out', 'r').read() == 'Syntax error: line 1, colon EOF\n'

def test_incorrect_head(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('f.\n dwwd :- wef. \n :- f ; e')
    monkeypatch.chdir(tmp_path)
    main.main(['a.txt'])
    assert open('a.txt.out', 'r').read() == 'Syntax error: line 3, colon 0\n'

def test_incorrect_body(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('foo :- .\n dwwd :- wef. \n t :- f ; e')
    monkeypatch.chdir(tmp_path)
    main.main(['a.txt'])
    assert open('a.txt.out', 'r').read() == 'Syntax error: line 1, colon 7\nSyntax error: line 3, colon EOF\n'

def test_incorrect_conj(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('foo :- kek ; lol.\ndwwd :- def ; few , . \nt :- f ; e\n')
    monkeypatch.chdir(tmp_path)
    main.main(['a.txt'])
    assert open('a.txt.out', 'r').read() == 'Syntax error: line 2, colon 20\nSyntax error: line 4, colon EOF\n'

def test_incorrect_scopes1(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('foo few :- kek ; lol.\ndwwd :- def ; few,fwe . \n t :- (f ; e) , ew).')
    monkeypatch.chdir(tmp_path)
    main.main(['a.txt'])
    assert open('a.txt.out', 'r').read() == 'Syntax error: line 3, colon 18\n'

def test_incorrect_scopes2(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('foo :- kek ; lol.\ndwwd :- def ; few,fwe . \nt :- h, (ew)) .\nf.')
    monkeypatch.chdir(tmp_path)
    main.main(['a.txt'])
    assert open('a.txt.out', 'r').read() == 'Syntax error: line 3, colon 12\n'

def test_incorrect_atom(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('(b) :- g.\n t () :- g. \n(a (b a)) .')
    monkeypatch.chdir(tmp_path)
    main.main(['a.txt'])
    assert open('a.txt.out', 'r').read() == 'Syntax error: line 1, colon 0\nSyntax error: line 2, colon 4\nSyntax error: line 3, colon 0\n'
