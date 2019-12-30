takes(john, math1).
takes(john, gym1).

takes(pete, math2).
takes(pete, gym2).

gives(q, math1).
gives(q, math2).

gives(r, gym1).
gives(r, gym2).

takes(S, C, T) :-
    

?- forall((gives(X, Y), between(0, 5, Class)), asserta(gives(X, Y, Z))).

