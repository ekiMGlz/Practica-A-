(setq abierto nil)
(setq cerrado nil)

(defun string-to-list (str)
  (if (not (streamp str))
    (string-to-list (make-string-input-stream str))
      (if (listen str)
        (cons (read str) (string-to-list str))
    nil)
  )
)

(setq in (open "assets/in.txt"))
(setq start (read-line in nil))
(setq end (read-line in nil))
(setq dist (read-line in nil))
(close in)

(setq start (car(string-to-list dist)))
(setq end (car(string-to-list dist)))
(setq dist (car(string-to-list dist)))

(setq in (open "assets/connections5.txt"))
(setq neigh (read-line in))
(close in)

(setq neigh (car (string-to-list neigh)))

(defun expand (n h)
  (loop for ls in (cdr (nth n neigh)) do 
    (when (null (position (car ls) cerrado))
      (push (list (car ls) n (+ h (cadr ls)) (cadr (nth (car ls) dist))) abierto)
    )
  )
)

(defun next ()
  (let ((n -1) (m 100000)) 
    (loop for ls in abierto do 
      (when (< (+ (cadddr ls) (caddr ls)) m)
        (setq m (+ (cadddr ls) (caddr ls))) (setq n (car ls))
      )
    )
  (list n m))
)

(defun run ()
  (let ((n (car (next))) (h (cadr (next))))
    (push n cerrado)
    (setf abierto (remove n abierto :key 'first))
    (expand n h)
  )
)
