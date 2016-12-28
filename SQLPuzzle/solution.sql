select * from set1 
intersect
select *  from set2
minus
select * from set3
union 
select * from (select * from set3
               minus
               select * from ( select * from set1
                               union
                               select * from set2))

