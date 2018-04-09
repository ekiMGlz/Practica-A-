;;Formato de nodos en abierto: (ID IDPAPA x y h g f)
;;Formato de nodos en cerrado: (ID IDPAPA)
;;g es cto de moverse del origen al nodo, h es distancia al origen y f = g+h
;;Nombre de endino: end

(defun abiertoInsert(obj l)
  (cond
    ((Null l) (cons obj l))
    ((< (car (last obj)) (car (last (car l)))) (cons obj (remove (car obj) l :key #'first)))
    ((= (car obj) (caar l)) l)
    (t (cons (car l) (abiertoInsert obj (cdr l))))
    )
)

;;Si current es global se puede quitar como parametro
(defun contorno(node)
  (setq df1 (sqrt (+ (expt (- (third node) (third current)) 2) (expt (- (fourth node) (fourth current)) 2 ))) 
    df2 (sqrt (+ (expt (- (third node) (third end))  2) (expt (- (fourth node) (fourth end)) 2 ))) )
  (<= (+ df1 df2) (* 2 a))
)

;Lista de conexiones: neigh
;Lista de nodos: dist
(defun expand()
    (setq c ( / (sqrt (+ (expt  (- (third current) (third end)) 2) (expt (-(fourth current) (fourth end)) 2))) 2 ) 
        a (* (sqrt 2) c)
        hijos (cdr (find (car current) neigh :key #'car)))
    (loop for aux in hijos do
        (cond 
            ((find (car aux) cerrado :key #'car))
            (t
                (setq node (find (car aux) dist :key #'car))
                (push (car current) (cdr node))
                (setq node (append node (list (+ (cadr aux) (sixth current)))))
                (setq node (append node (list (+ (fifth node) (sixth node)))))
                (if (contorno node) (setq abierto (abiertoInsert node abierto)))
            )
        )
    )
)

;;Nodo actual: current
(defun next()
    (setq current (pop abierto))
    (push (list (car current) (cadr current)) cerrado)
    (cond 
        ((= (car current) (car end)) (backtrackCerrado (car current)) nil)
        (t (expand) t)
    )
)

(defun backtrackCerrado(son)
  (cond
    ((Null son))
    (t (push son final) (backtrackCerrado (cadr (find son cerrado :key #'car))))
    )
)

(defun string-to-list (str)
    (if (not (streamp str))
        (string-to-list (make-string-input-stream str))
        (if (listen str)
        (cons (read str) (string-to-list str))
        nil)
    )
)
    
(defun init()
    (setq abierto nil)
    (setq cerrado nil)
    (setq final nil)

    (setq in (open "data/in.txt"))
    (setq start (read-line in))
    (setq end (read-line in))
    (setq dist (read-line in))
    (close in)

    (setq start (car(string-to-list start)))
    (setq end (car(string-to-list end)))
    (setq dist (car(string-to-list dist)))

    (setq in (open "data/connections5.txt"))
    (setq neigh (read-line in))
    (close in)

    (setq neigh (car (string-to-list neigh)))
    
    (push start abierto)
)
