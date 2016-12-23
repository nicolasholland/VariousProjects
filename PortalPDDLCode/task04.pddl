;;; There are three rooms A, B and C. The player has to use portals and take a cube from room C to room B before returning to room A.
;;;
(define (problem create-portal)
   (:domain portal)
   (:objects
      char - player
      sectorA sectorB sectorC- location
   )
   (:init
      (at char sectorA)
      (cube-at sectorC)

   )
   (:goal (and (cube-at sectorB) (at char sectorA)))
)
