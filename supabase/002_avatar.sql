-- صورة شخصية صغيرة (data URL مضغوطة من المتصفح) مخزنة مع الحساب
alter table public.dawami_accounts add column if not exists avatar text not null default ''
  check (avatar = '' or (avatar like 'data:image/%;base64,%' and char_length(avatar) <= 300000));

create or replace function public.dawami_set_avatar(p_key text, p_avatar text) returns boolean
language plpgsql security definer set search_path = '' as $$
declare v uuid := public.dawami_account(p_key);
begin
  update public.dawami_accounts set avatar = coalesce(p_avatar, ''), updated_at = now() where id = v;
  return true;
end $$;

create or replace function public.dawami_load(p_key text) returns jsonb
language plpgsql stable security definer set search_path = '' as $$
declare v uuid := public.dawami_account(p_key);
begin
  return jsonb_build_object(
    'settings', (select settings from public.dawami_accounts where id = v),
    'avatar', (select avatar from public.dawami_accounts where id = v),
    'records', coalesce((select jsonb_object_agg(to_char(day,'YYYY-MM-DD'), jsonb_build_object('in', check_in, 'out', check_out)) from public.dawami_records where account_id = v), '{}'::jsonb),
    'exceptions', coalesce((select jsonb_object_agg(to_char(day,'YYYY-MM-DD'), kind) from public.dawami_exceptions where account_id = v), '{}'::jsonb)
  );
end $$;

create or replace function public.dawami_wipe(p_key text) returns boolean
language plpgsql security definer set search_path = '' as $$
declare v uuid := public.dawami_account(p_key);
begin
  delete from public.dawami_records where account_id = v;
  delete from public.dawami_exceptions where account_id = v;
  update public.dawami_accounts set settings = '{}'::jsonb, avatar = '', updated_at = now() where id = v;
  return true;
end $$;

revoke all on function public.dawami_set_avatar(text, text) from public;
grant execute on function public.dawami_set_avatar(text, text) to anon, authenticated;
