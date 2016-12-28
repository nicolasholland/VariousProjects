select * from set1 
intersect
select *  from (select * from set2
                union
                select * from set3)

