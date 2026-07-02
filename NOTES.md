day 1:
  ###Tema #1
  Linia 1 este data rularii:
  pentru "78_5overall_FCOV.txt" : "[2026-06-15 10:41:11 UTC] vcs -full64 -licqueue '-timescale=1ns/1ns' '+vcs+flush+all' '+warn=all' '-sverilog' design.sv testbench.sv  && ./simv +vcs+lic+wait"
  
  Procentajele(general si indiv. coverpoint) apar dupa:
  "=========== Functional Coverage ==========="
  
  Sunt 4 feluri de tabele:
  1. cp_vec:
            "vec[ 0]  0000 : hits=2           HIT"
  2. cp_pop:
            "none(0) : hits=2           HIT"
  3. cp_en/cp_vote:
            "en=0   : hits=4           HIT"
            "vote=0 : hits=12           HIT"
  4. x_en_vote:
            "x_en_vote[ 0]  0000 : hits=2           HIT"
  
  O linia HIT se destinge fiind faptu ca daca
  hits este > 0 in timpul simularii
  iar MISS fiind # de hits = 0
  
  ###Tema #2
  Pentru "78_5overall_FCOV.txt" in total sunt 29 de bin-uri
  si 12 miss-uri
  Sa respecta regula ca daca hits > 0 atunci HIT
day 3:
  DB-First approach este util cand este necesara ca database-ul sa fie modificabil la orice limbaj de programare/framework, pe cand code-first permite dor un libmaj/framework sa il modifice.
  Ca exemplu, daca o corporatie are 3 instrumente de limbaj complet diferite unu fata de alta, daca db era scris de 1-a, atunci a 2-lea si a 3-lea nu pot sa fac modificari la db.
  De asta se utilizeaza conceptul de db-first.
  La db-first, DBA scrie o schema, iar fiecare limbaj/framework isi adapteaza dupa el codul.
