(define (problem bridges)
    (:domain Bridges)

    (:init (at_x2) (at_y2))

    (:goal
     (and
      (holding_treasure_1)
      (holding_treasure_2)
      (holding_treasure_3)
     )
    )
)