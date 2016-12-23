;;; There are 4 rooms, two of them have a cube. The player has to use portals and bring the two cubes to the two other rooms.
;;;
(define (problem create-portal)
   (:domain portal)
   (:objects
      char - player
      sectorA sectorB sectorC sectorD- location
   )
   (:init
      (at char sectorA)
      (cube-at sectorC)
      (cube-at sectorD)
   )

   (:goal (and (cube-at sectorB) (cube-at sectorA)))
)
