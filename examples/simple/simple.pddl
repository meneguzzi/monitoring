; This is a comment line
(define (domain simple) ; There is no block comment like
  (:requirements :strips)
  (:predicates
    (p)
    (q)
    (r)
  )
  (:action a
    :parameters ()
    :precondition (and
      (p)
    )
    :effect (and
      (q)
    )
  )
  (:action b
    :parameters ()
    :precondition (and
      (q)
    )
    :effect (and
      (not (q))
    )
  )
  (:action c
    :parameters ()
    :precondition (and
      (q)
    )
    :effect (and
      (r)
      (not (q))
    )
  )
  (:action d
    :parameters ()
    :precondition (and
      (r)
    )
    :effect (and
      (p)
      (not (q))
    )
  )
)