;;; Portal pddl domain
(define (domain portal)
   (:requirements :strips :typing)
   (:types player location)

   ;;; walk through portal
   (:action use-portal
      :parameters (?p - player ?l1 - location ?l2 - location)
      :precondition (and (at ?p ?l1) (portal ?l1 ?l2))
      :effect (and (at ?p ?l2) (not (at ?p ?l1)))
   )

   ;;; connect two locations with a portal
   (:action create-portal
      :parameters (?l1 - location ?l2 - location)
      :precondition (not (portal ?l1 ?l2))
      :effect (and (portal ?l1 ?l2))
   )

   ;;; take a cube through a portal
   (:action move-cube-through-portal
     :parameters (?p - player ?l1 - location ?l2 - location)
     :precondition (and (cube-at ?l1) (portal ?l1 ?l2) (at ?p ?l1))
     :effect (and (cube-at ?l2) (at ?p ?l2) (not (cube-at ?l1)) (not (at ?p ?l1)))
   )
)
