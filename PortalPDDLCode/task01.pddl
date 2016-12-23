;;; The player has to open a portal that connects the two locations and use it 
;;;
(define (problem create-portal)
   (:domain portal)
   (:objects
      char - player
      sectorA sectorB - location
   )
   (:init
      (at char sectorA)
   )
   (:goal (and (at char sectorB)))
)
