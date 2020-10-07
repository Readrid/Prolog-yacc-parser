import main

def test_tree_simple(tmp_path, tmpdir, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('F :- f.')
    monkeypatch.chdir(tmp_path)
    main.main(['a.txt'])
    assert open('a.txt.out', 'r').read() == 'REL (ATOMEXPR (ID F)) (ID f)\n'

def test_tree_atom_scopes(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('F (cons H) p:- f.')
    monkeypatch.chdir(tmp_path)
    main.main(['a.txt'])
    assert open('a.txt.out', 'r').read() == "REL (ATOMEXPR (ATOMBODY (ID F) (ATOM ((ATOMBODY (ID cons) (ATOM (ATOMEXPR (ID H)))) ATOM (ATOMEXPR (ID p)))))) (ID f)\n"

def test_tree_atom_concat(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('F g t:- f.')
    monkeypatch.chdir(tmp_path)
    main.main(['a.txt'])
    assert open('a.txt.out', 'r').read() == 'REL (ATOMEXPR (ATOMBODY (ID F) (ATOM (ATOMEXPR (ATOMBODY (ID g) (ATOM (ATOMEXPR (ID t)))))))) (ID f)\n'

def test_tree_expr_simple(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('F :- t , j ; l.')
    monkeypatch.chdir(tmp_path)
    main.main(['a.txt'])
    assert open('a.txt.out', 'r').read() == 'REL (ATOMEXPR (ID F)) (DISJ (CONJ (ID t ID j) ID l))\n'

def test_tree_expr_scopes(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('F :- t , ((j ; l) , r).')
    monkeypatch.chdir(tmp_path)
    main.main(['a.txt'])
    assert open('a.txt.out', 'r').read() == 'REL (ATOMEXPR (ID F)) (CONJ (ID t (CONJ ((DISJ (ID j ID l)) ID r))))\n'

def test_tree_three_simple_lines(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('F :- t.\n G (p g).\n K :- t;l.')
    monkeypatch.chdir(tmp_path)
    main.main(['a.txt'])
    tree1 = "REL (ATOMEXPR (ID F)) (ID t)\n"
    tree2 = "REL (ATOMEXPR (ATOMBODY (ID G) (ATOM (ATOMBODY (ID p) (ATOM (ATOMEXPR (ID g)))))))\n"
    tree3 = "REL (ATOMEXPR (ID K)) (DISJ (ID t ID l))\n"
    assert open('a.txt.out', 'r').read() == tree1 + tree2 + tree3

def test_incorrect_without_dot(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('f.\n f')
    monkeypatch.chdir(tmp_path)
    main.main(['a.txt'])
    assert open('a.txt.out', 'r').read() == 'Syntax error: line 2\n'

def test_incorrect_without_dot_with_scope(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('f :- (w)\nf.')
    monkeypatch.chdir(tmp_path)
    main.main(['a.txt'])
    assert open('a.txt.out', 'r').read() == 'Syntax error: line 2\n'

def test_incorrect_without_dot_one_line(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('f :- (w)')
    monkeypatch.chdir(tmp_path)
    main.main(['a.txt'])
    assert open('a.txt.out', 'r').read() == 'Syntax error: line 1\n'

def test_incorrect_head(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('f.\n dwwd :- wef. \n :- f ; e')
    monkeypatch.chdir(tmp_path)
    main.main(['a.txt'])
    assert open('a.txt.out', 'r').read() == 'Syntax error: line 3\n'

def test_incorrect_body(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('foo :- .\n dwwd :- wef. \n t :- f ; e')
    monkeypatch.chdir(tmp_path)
    main.main(['a.txt'])
    assert open('a.txt.out', 'r').read() == 'Syntax error: line 1\nSyntax error: line 3\n'

def test_incorrect_conj(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('foo :- kek ; lol.\ndwwd :- def ; few , . \n t :- f ; e\n')
    monkeypatch.chdir(tmp_path)
    main.main(['a.txt'])
    assert open('a.txt.out', 'r').read() == 'Syntax error: line 2\nSyntax error: line 4\n'

def test_incorrect_scopes1(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('foo few :- kek ; lol.\ndwwd :- def ; few,fwe . \n t :- (f ; e) , ew).')
    monkeypatch.chdir(tmp_path)
    main.main(['a.txt'])
    assert open('a.txt.out', 'r').read() == 'Syntax error: line 3\n'

def test_incorrect_scopes2(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('foo :- kek ; lol.\ndwwd :- def ; few,fwe . \nt :- h, (ew)) .\nf.')
    monkeypatch.chdir(tmp_path)
    main.main(['a.txt'])
    assert open('a.txt.out', 'r').read() == 'Syntax error: line 3\n'

def test_incorrect_atom(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('foo (lol) :- kek ; lol.\ndwwd :- def ; few,fwe . \nt :- h, (ew)) .\nf.')
    monkeypatch.chdir(tmp_path)
    main.main(['a.txt'])
    assert open('a.txt.out', 'r').read() == 'Syntax error: line 1\n'

def test_incorrect_atom(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('foo :- kek ; lol.\ndwwd (f (f)):- def ; few,fwe . \nt :- h, (ew)) .\nf.')
    monkeypatch.chdir(tmp_path)
    main.main(['a.txt'])
    assert open('a.txt.out', 'r').read() == 'Syntax error: line 2\n'

def test_incorrect_atom_last(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('foo :- kek ; lol.\nf a')
    monkeypatch.chdir(tmp_path)
    main.main(['a.txt'])
    assert open('a.txt.out', 'r').read() == 'Syntax error: line 2\n'

def test_incorrect_atom(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('foo lol (fwef (few few) few) fwer ((fre) fer) :- kek ; lol.')
    monkeypatch.chdir(tmp_path)
    main.main(['a.txt'])
    assert open('a.txt.out', 'r').read() == 'Syntax error: line 1\n'
