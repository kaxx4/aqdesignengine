-- READ-ONLY queries for the campaign data. Run each against the Shikshaq project with the Supabase connector's execute_sql,
-- save each result as JSON in campaign/import/ (names below), then:  node campaign/wire-data.mjs
-- Nothing here writes. Reviews are other people's words and are quoted exactly. Keep every `id` so a quote can be traced.

-- import/counts.json   (one row)
select * from public.site_counts();

-- import/reviews.json  (approved, named-or-not, a readable length, the teacher's subject for the colour)
select c.id, c.comment, c.rating, c.is_anonymous, c.created_at,
       t.subjects as subject, t.classes as classes, p.full_name
from public.teacher_comments c
join public.teachers_list t on t.id = c.teacher_id
left join public.profiles p on p.id = c.user_id
where c.approved = true
  and c.comment is not null
  and length(c.comment) between 60 and 260
order by c.rating desc nulls last, length(c.comment) desc, c.created_at desc
limit 40;

-- import/areas.json  (where tutors are, for the FAQ about areas)
select location, count(*) as n
from public.teachers_list
where location is not null and btrim(location) <> ''
group by location
order by n desc
limit 30;

-- import/tutor-candidates.json  (look people up by name; the owner supplies the approved quotes and photos)
select name, slug, subjects, classes, location, image_url
from public.teachers_list
where name ilike any (array['%PUT NAME 1%', '%PUT NAME 2%', '%PUT NAME 3%']);
