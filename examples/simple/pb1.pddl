(define (problem pb1)
  (:domain simple)
  (:init
    (garbage)
    (clean)
    (quiet)
  )
  (:goal (and
    (dinner)
    (present)
    (not (garbage))
  ))
)