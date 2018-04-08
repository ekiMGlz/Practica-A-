(Load 'funciones.cl)
(init)
(setq flag T)
(loop while flag do
    (setq flag (next))
)
(print final)
(with-open-file (str "data/out.txt"
                     :direction :output
                     :if-exists :supersede
                     :if-does-not-exist :create)
  (format str (write-to-string final)))
