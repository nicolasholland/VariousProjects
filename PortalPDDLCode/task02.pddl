;;; The player has to open a portal between to locations and move a cube through
;;;
(define (problem create-portal)
   (:domain portal)
   (:objects
      char - player
      sectorA sectorB - location
   )
   (:init
      (at char sectorA)
      (cube-at sectorA)

   )
   (:goal (and (cube-at sectorB)))
)
