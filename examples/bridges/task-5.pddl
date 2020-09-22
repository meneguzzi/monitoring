(define (problem bridges)
    (:domain Bridges)

    (:init (at_x3) (at_y4))

    (:goal
     (and
      (holding_treasure_1)
      (holding_treasure_2)
      (holding_treasure_3)
     )
    )
)